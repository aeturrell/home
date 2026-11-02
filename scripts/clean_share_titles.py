"""Remove the site name from the titles used in link previews.

Quarto appends " – <site title>" to og:title and twitter:title, and the site
title is also sent as og:site_name, so previews would show the name twice.
Browser tab titles are left as they are.
"""

import os
import re
from pathlib import Path

SUFFIX = " – Arthur Turrell"
PATTERN = re.compile(
    r'(<meta (?:property="og:title"|name="twitter:title") content="[^"]*?)'
    + re.escape(SUFFIX)
    + r'"'
)

output_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))

for page in output_dir.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    cleaned = PATTERN.sub(r'\1"', html)
    if cleaned != html:
        page.write_text(cleaned, encoding="utf-8")
