#!/usr/bin/env python3
"""
uk_triple_lock_data.py
======================

Build a single, tidy, annual CSV describing the UK "triple lock" and its two
varying components.

Columns produced
----------------
    year                                  Calendar year (int; 2011 == FY 2011/12)
    state_pension_expenditure_gbp_million State Pension spending, nominal £m  (ABSOLUTE)
    state_pension_expenditure_real_gbp_million  Same, real £m (constant prices)
    state_pension_expenditure_pct_gdp     State Pension spending as % of GDP
    state_pension_caseload_thousands      Recipients, thousands
    state_pension_real_per_pensioner_gbp  Real spending per recipient, £
    state_pension_expenditure_basis       "Outturn" or "Forecast"
    avg_earnings_growth_pct               AWE total-pay growth, May-Jul, %    (COMPONENT 1)
    cpi_inflation_pct                     CPI annual rate, September, %       (COMPONENT 2)
    triple_lock_uprating_pct              max(earnings, CPI, 2.5), % (THE LOCK)
    expected_state_pension_exp_triple_lock          Counterfactual spending, £m
    expected_state_pension_exp_triple_lock_real     Counterfactual, real £m
    expected_state_pension_exp_triple_lock_pct_gdp  Counterfactual, % of GDP

The real-terms columns are DWP's own constant-price series (the workbook states
its price base; the script logs it), NOT a deflator applied here. Reading the
nominal, real and % of GDP columns together is the point: they can tell different
stories, because they differ in what they hold constant. Per-pensioner separates
the value of the pension from the number of people drawing it.

The triple lock uprates the State Pension by the highest of: average earnings
growth, CPI inflation, or 2.5%. Only the first two vary year to year, which is
why just those two are pulled here. Coverage runs from the policy's introduction
(2011/12) to the latest available year.

The three derived columns isolate the lock from everything else that moves the
bill. `triple_lock_uprating_pct` is the rise applied that April; the two
`expected_*` columns take actual 2011/12 spending and compound that rise onto it,
so they show what the State Pension would cost if the lock were the ONLY thing
driving it. They hold the caseload fixed, so the gap against the actual columns
is pensioner numbers, not generosity. Both are derived FROM the uprating column,
so the three are consistent by construction.

Note the two components are the specific readings the uprating decision is made
on, not calendar-year averages: earnings growth for May-July, and CPI in the year
to September. Both are published in the autumn and determine the following
April's rise, so the value on row `year` is what set the April `year`+1 uprating.

Data sources
------------
1. ONS time series JSON (open, no API key required):
       https://www.ons.gov.uk/{theme}/timeseries/{cdid}/{dataset}/data
   - CPI annual rate, all items ....... CDID = D7G7, dataset = MM23  (September)
   - AWE total pay, GB, % YoY (3m avg)  CDID = KAC3, dataset = LMS   (July, i.e.
     the May-July average)
   Both are read from the "months" block. The old api.ons.gov.uk host now 404s,
   and KAC3 has no annual series to fall back on.

   CAVEAT: these are the LIVE series, so they carry every revision ONS has made
   since. Each uprating was legislated on the vintage available that autumn, and
   AWE in particular gets revised, so the earnings column will not always equal
   the rise that was actually paid. May-July 2024 now reads 4.4% here; the April
   2025 uprating was set at 4.1%. Quote the legislated figure, not this column,
   if the post states what pensioners received.

2. DWP "Benefit expenditure and caseload tables" (spreadsheet on GOV.UK):
   There is NO REST API for State Pension spending, so this script downloads and
   parses DWP's outturn-and-forecast workbook (Spring Forecast 2026 by default;
   override with --spending-file for a newer edition or a local copy). Two sheets
   are used:
     - "State Pension": the `Total` row of the "£ million, nominal terms" block,
       which is total State Pension spending by financial year. The block's
       header row also marks each year as Outturn or Forecast, and that flag is
       carried into the CSV — the workbook runs several years past the last
       outturn, so the later rows are projections, not history.
     - "GB welfare": the ONS-sourced `GDP denominator` row (also £m). The
       workbook publishes % of GDP only by claimant group, never per benefit, so
       the % of GDP column is computed as nominal spending / GDP denominator,
       i.e. on DWP's own denominator.
   If parsing fails, the CSV is still written from the two ONS components with
   the spending columns left blank, and the reason is logged.

Usage
-----
    python uk_triple_lock_data.py                       # writes the CSV next to this post
    python uk_triple_lock_data.py --output-dir ~/data
    python uk_triple_lock_data.py --spending-file dwp_tables.xlsx

Dependencies
------------
    pip install requests pandas openpyxl
    #   odfpy is needed only if you point --spending-file at an .ods edition
"""

from __future__ import annotations

import argparse
import io
import logging
import re
import sys
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# --- Output ---------------------------------------------------------------- #
# The output directory. Overridable on the command line with --output-dir.
DEFAULT_OUTPUT_DIR = Path("blog/posts/politically-realistic-reform-triple-lock")
OUTPUT_FILENAME = "uk_triple_lock.csv"

# --- Coverage -------------------------------------------------------------- #
TRIPLE_LOCK_START_YEAR = 2011  # 2011/12 was the first year of the triple lock

# --- Triple lock ------------------------------------------------------------ #
TRIPLE_LOCK_FLOOR_PCT = 2.5  # the third lock: the fixed floor under the uprating

# --- ONS Time Series API --------------------------------------------------- #
# api.ons.gov.uk no longer serves these (404s); the site's own JSON does, but it
# requires the series' full theme path rather than a bare CDID.
ONS_TS_URL = "https://www.ons.gov.uk/{theme}/timeseries/{cdid}/{dataset}/data"

INFLATION_THEME = "economy/inflationandpriceindices"
EARNINGS_THEME = "employmentandlabourmarket/peopleinwork/earningsandworkinghours"

# (theme, cdid, dataset, month). Browse a series at the same URL minus the "/data".
#
# The month matters: the triple lock is not settled on calendar-year averages, it
# is settled on two specific readings taken in the autumn before the April
# uprating. Both series are therefore sampled at the month whose figure is the
# one Parliament actually acts on.
ONS_SERIES = {
    # CPI annual rate, all items: the September reading (published October).
    "cpi_inflation_pct": (INFLATION_THEME, "d7g7", "mm23", "September"),
    # AWE total pay, GB, % YoY: the July reading IS the May-July three-month
    # average growth, i.e. the earnings figure published each September.
    "avg_earnings_growth_pct": (EARNINGS_THEME, "kac3", "lms", "July"),
}

# --- DWP State Pension expenditure spreadsheet ----------------------------- #
# No API exists. This is DWP's "Benefit expenditure and caseload tables"
# (Spring Forecast 2026). The URL changes with each publication, so pass a newer
# workbook — or a local copy — via --spending-file when one lands.
DWP_SPENDING_URL: Optional[str] = (
    "https://assets.publishing.service.gov.uk/media/69dcdc8c6b695d635c34dcc4/"
    "outturn-and-forecast-tables-spring-forecast-2026.xlsx"
)

# Where to look inside the workbook. Layouts shift between editions, so sheets
# and rows are matched on substrings rather than fixed positions.
DWP_SPENDING_SHEET_HINT = "state pension"  # per-benefit sheet
DWP_NOMINAL_BLOCK_HINT = "nominal terms"  # the cash £m block
DWP_REAL_BLOCK_HINT = "real terms"  # the constant-price £m block
DWP_TOTAL_ROW_LABEL = "total"  # total spending row within either block
DWP_CASELOAD_ROW_LABEL = "total state pension caseload"  # recipients, thousands

DWP_GDP_SHEET_HINT = "gb welfare"  # sheet carrying the ONS denominators
DWP_GDP_ROW_LABEL = "gdp denominator"  # nominal GDP, £m

# Financial-year label, e.g. "2011/12" -> calendar year 2011.
FY_PATTERN = r"^((?:19|20)\d\d)/\d\d"

# Cells that are years rather than labels: the financial years across the top,
# and the bare edition year DWP prints down the left-hand banner column.
YEAR_LIKE_PATTERN = r"^(?:19|20)\d\d(?:/\d\d)?$"

REQUEST_TIMEOUT = 30  # seconds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("triple_lock")


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #


def _session() -> requests.Session:
    """A requests session with sensible retry/back-off behaviour."""
    s = requests.Session()
    retries = Retry(
        total=4,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.headers.update({"User-Agent": "uk-triple-lock-fetcher/1.0"})
    return s


# --------------------------------------------------------------------------- #
# ONS component fetchers (earnings growth, CPI)
# --------------------------------------------------------------------------- #


def fetch_ons_uprating_month(
    theme: str, cdid: str, dataset: str, month: str, session: requests.Session
) -> pd.Series:
    """
    Fetch an ONS time series and return one reading per year — the value for
    `month` — as a Series indexed by integer year.

    The monthly block is used rather than the annual one because that is where
    the triple lock's inputs live: neither series is uprating-relevant as a
    calendar-year average, and KAC3 publishes no annual figure at all.
    """
    url = ONS_TS_URL.format(theme=theme, cdid=cdid, dataset=dataset)
    log.info("Fetching ONS series %s/%s (%s reading)", cdid, dataset, month)
    resp = session.get(url, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()

    records: dict[int, float] = {}
    for row in payload.get("months", []):
        if str(row.get("month", "")).strip().lower() != month.lower():
            continue
        year, value = row.get("year"), row.get("value")
        if year and value not in (None, ""):
            try:
                records[int(year)] = float(value)
            except (TypeError, ValueError):
                continue

    if not records:
        raise ValueError(f"No {month} data returned for {cdid}/{dataset}")

    return pd.Series(records, name=cdid).sort_index()


def build_components(session: requests.Session) -> pd.DataFrame:
    """Assemble the two ONS-sourced triple-lock components into a DataFrame."""
    series = {}
    for column, (theme, cdid, dataset, month) in ONS_SERIES.items():
        series[column] = fetch_ons_uprating_month(theme, cdid, dataset, month, session)
    df = pd.DataFrame(series)
    df.index.name = "year"
    return df


# --------------------------------------------------------------------------- #
# DWP State Pension expenditure (spreadsheet, no API)
# --------------------------------------------------------------------------- #


def _read_dwp_workbook(
    source: str, session: requests.Session
) -> dict[str, pd.DataFrame]:
    """Read every sheet of a DWP workbook from a local path or a URL."""
    engine = "odf" if source.lower().endswith(".ods") else None

    if source.startswith(("http://", "https://")):
        log.info("Downloading DWP spreadsheet: %s", source)
        resp = session.get(source, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        handle: object = io.BytesIO(resp.content)
    else:
        handle = Path(source).expanduser()

    return pd.read_excel(handle, sheet_name=None, header=None, engine=engine)


def _find_sheet(sheets: dict[str, pd.DataFrame], hint: str) -> tuple[str, pd.DataFrame]:
    """Return the first sheet whose name contains `hint` (case-insensitive)."""
    name = next((n for n in sheets if hint.lower() in n.lower().strip()), None)
    if name is None:
        raise KeyError(f"No sheet matching {hint!r}. Sheets: {list(sheets)}")
    return name, sheets[name]


def _row_label(row: pd.Series) -> str:
    """
    The row's leading text cell, lower-cased; '' if the row has no label.

    Year-like cells are skipped: DWP prints the edition year ("2026") in the
    banner column to the left of the labels, so the first populated cell is not
    always the label.
    """
    text = row.dropna().astype(str).str.strip()
    text = text[~text.str.match(YEAR_LIKE_PATTERN)]
    return text.iloc[0].lower() if text.size else ""


def _year_columns(header: pd.Series) -> dict[Any, int]:
    """Map each column holding a financial-year label to its starting year."""
    found = header.astype(str).str.strip().str.extract(FY_PATTERN, expand=False)
    return {col: int(yr) for col, yr in found.dropna().items()}


def _series_by_year(row: pd.Series, year_cols: dict[Any, int]) -> pd.Series:
    """Pull a data row into a year-indexed Series, dropping blanks and text."""
    values = {
        year: pd.to_numeric(row[col], errors="coerce")
        for col, year in year_cols.items()
    }
    return pd.Series(values).dropna().sort_index()


def _year_header_above(frame: pd.DataFrame, row_idx: int) -> dict[Any, int]:
    """
    The financial-year header governing `row_idx`: the nearest row above it that
    carries year labels.

    The 'State Pension' sheet stacks several blocks (nominal £m, real £m,
    caseloads), each re-declaring its own year header, so a data row's columns
    only mean something relative to the header immediately above it.
    """
    for i in range(row_idx - 1, -1, -1):
        year_cols = _year_columns(frame.iloc[i])
        if year_cols:
            return year_cols
    raise KeyError(f"No financial-year header above row {row_idx}")


def _find_row(frame: pd.DataFrame, label: str, start: int = 0) -> int:
    """Index of the first row at or after `start` whose label is exactly `label`."""
    idx = next(
        (i for i in range(start, len(frame)) if _row_label(frame.iloc[i]) == label),
        None,
    )
    if idx is None:
        raise KeyError(f"No {label!r} row found")
    return idx


def _find_block(frame: pd.DataFrame, hint: str) -> int:
    """Index of the subtitle row naming a block, e.g. '£ million, nominal terms'."""
    idx = next(
        (i for i in range(1, len(frame)) if hint in _row_label(frame.iloc[i])), None
    )
    if idx is None:
        raise KeyError(f"No {hint!r} block found")
    return idx


def _extract_state_pension(sheets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    From the 'State Pension' sheet, pull total spending in nominal and real terms,
    the caseload, and the Outturn/Forecast flag DWP stamps on each column.

    Each block is found by its subtitle ("... nominal terms", "... real terms"),
    with the "Total" row beneath it holding the series. The nominal subtitle row
    doubles as the Outturn/Forecast marker row. The caseload block has no such
    subtitle, so its total row is matched by name directly.
    """
    name, frame = _find_sheet(sheets, DWP_SPENDING_SHEET_HINT)

    nominal_block = _find_block(frame, DWP_NOMINAL_BLOCK_HINT)
    nominal_idx = _find_row(frame, DWP_TOTAL_ROW_LABEL, start=nominal_block + 1)
    nominal_years = _year_header_above(frame, nominal_idx)
    nominal = _series_by_year(frame.iloc[nominal_idx], nominal_years)

    real_block = _find_block(frame, DWP_REAL_BLOCK_HINT)
    real_idx = _find_row(frame, DWP_TOTAL_ROW_LABEL, start=real_block + 1)
    real = _series_by_year(frame.iloc[real_idx], _year_header_above(frame, real_idx))

    caseload_idx = _find_row(frame, DWP_CASELOAD_ROW_LABEL)
    caseload = _series_by_year(
        frame.iloc[caseload_idx], _year_header_above(frame, caseload_idx)
    )

    basis = pd.Series(
        {
            year: str(frame.iloc[nominal_block][col]).strip()
            for col, year in nominal_years.items()
        }
    ).reindex(nominal.index)

    price_base = re.search(
        r"(20\d\d/\d\d)\s+prices", _row_label(frame.iloc[real_block])
    )
    log.info(
        "State Pension: %d years (%d–%d) from sheet %r; real terms in %s prices",
        len(nominal),
        nominal.index.min(),
        nominal.index.max(),
        name,
        price_base.group(1) if price_base else "unknown",
    )

    return pd.DataFrame(
        {
            "state_pension_expenditure_gbp_million": nominal,
            "state_pension_expenditure_real_gbp_million": real,
            "state_pension_caseload_thousands": caseload,
            "state_pension_expenditure_basis": basis,
        }
    )


def _extract_gdp(sheets: dict[str, pd.DataFrame]) -> pd.Series:
    """Nominal GDP (£m) by year, from the ONS denominator row DWP publishes."""
    name, frame = _find_sheet(sheets, DWP_GDP_SHEET_HINT)

    year_cols = _year_columns(frame.iloc[1])
    if not year_cols:
        raise KeyError(f"No financial-year header in sheet {name!r}")

    gdp_idx = next(
        (
            i
            for i in range(len(frame))
            if _row_label(frame.iloc[i]) == DWP_GDP_ROW_LABEL
        ),
        None,
    )
    if gdp_idx is None:
        raise KeyError(f"No {DWP_GDP_ROW_LABEL!r} row in sheet {name!r}")

    gdp = _series_by_year(frame.iloc[gdp_idx], year_cols)
    log.info(
        "GDP denominator: %d years (%d–%d) from sheet %r",
        len(gdp),
        gdp.index.min(),
        gdp.index.max(),
        name,
    )
    return gdp


def fetch_state_pension_spending(
    source: Optional[str], session: requests.Session
) -> pd.DataFrame:
    """
    Return a DataFrame indexed by year with columns:
        state_pension_expenditure_gbp_million
        state_pension_expenditure_real_gbp_million
        state_pension_expenditure_pct_gdp
        state_pension_caseload_thousands
        state_pension_real_per_pensioner_gbp
        state_pension_expenditure_basis

    DWP tabulates % of GDP only by claimant group, never per benefit, so the
    share is computed here from their own nominal GDP denominator. Real spending
    per pensioner is likewise derived: the real total over the caseload.

    Degrades gracefully: on any failure it returns an empty frame and logs how
    to fix it, so the CSV is still produced from the ONS components.
    """
    columns = [
        "state_pension_expenditure_gbp_million",
        "state_pension_expenditure_real_gbp_million",
        "state_pension_expenditure_pct_gdp",
        "state_pension_caseload_thousands",
        "state_pension_real_per_pensioner_gbp",
        "state_pension_expenditure_basis",
    ]
    empty = pd.DataFrame(columns=columns)
    if not source:
        log.warning(
            "No DWP spending source. Pass --spending-file <workbook> or set "
            "DWP_SPENDING_URL to include State Pension expenditure. "
            "Continuing with ONS components only."
        )
        return empty

    try:
        sheets = _read_dwp_workbook(source, session)
        df = _extract_state_pension(sheets)
        df["state_pension_expenditure_pct_gdp"] = (
            df["state_pension_expenditure_gbp_million"] / _extract_gdp(sheets) * 100
        )
        # £m over thousands of people -> £ per pensioner.
        df["state_pension_real_per_pensioner_gbp"] = (
            df["state_pension_expenditure_real_gbp_million"] * 1e6
        ) / (df["state_pension_caseload_thousands"] * 1e3)
        df.index.name = "year"
        return df.reindex(columns=columns)
    except Exception as exc:  # noqa: BLE001 - degrade gracefully, report clearly
        log.error(
            "Could not parse DWP spending from %s (%s). "
            "Check the sheet/row hints near the top of this script against the "
            "workbook's layout. Continuing with ONS components only.",
            source,
            exc,
        )
        return empty


# --------------------------------------------------------------------------- #
# Assembly
# --------------------------------------------------------------------------- #


def assemble(components: pd.DataFrame, spending: pd.DataFrame) -> pd.DataFrame:
    """Join everything into one tidy, year-indexed, filtered, ordered frame."""
    df = components.join(spending, how="outer")
    df = df[df.index >= TRIPLE_LOCK_START_YEAR].sort_index()

    ordered = [
        "state_pension_expenditure_gbp_million",
        "state_pension_expenditure_real_gbp_million",
        "state_pension_expenditure_pct_gdp",
        "state_pension_caseload_thousands",
        "state_pension_real_per_pensioner_gbp",
        "state_pension_expenditure_basis",
        "avg_earnings_growth_pct",
        "cpi_inflation_pct",
    ]
    df = df.reindex(columns=ordered)
    return df.reset_index()


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    p.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for the CSV (default: {DEFAULT_OUTPUT_DIR}).",
    )
    p.add_argument(
        "--spending-file",
        type=str,
        default=DWP_SPENDING_URL,
        help="Path or URL to the DWP benefit expenditure workbook (.ods/.xlsx).",
    )
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    session = _session()

    try:
        components = build_components(session)
    except Exception as exc:  # noqa: BLE001
        log.error("Failed to fetch ONS components: %s", exc)
        return 1

    spending = fetch_state_pension_spending(args.spending_file, session)
    result = assemble(components, spending)

    output_dir: Path = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / OUTPUT_FILENAME
    result.to_csv(output_path, index=False, float_format="%.2f")

    log.info(
        "Wrote %d rows (%d–%d) to %s",
        len(result),
        int(result["year"].min()),
        int(result["year"].max()),
        output_path,
    )

    forecast = result.loc[
        result["state_pension_expenditure_basis"]
        .str.lower()
        .eq("forecast")
        .fillna(False),
        "year",
    ]
    if not forecast.empty:
        log.info(
            "Spending from %d onwards is DWP forecast, not outturn.",
            int(forecast.min()),
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
