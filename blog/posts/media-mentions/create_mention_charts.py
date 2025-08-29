import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import statsmodels.api as sm
import matplotlib.dates as mdates
import hashlib

plt.style.use("https://github.com/aeturrell/python4DS/raw/main/plot_style.txt")

import matplotlib.font_manager as fm

print("Warning: you need to install the relevant fonts for this to work properly\n\nWarning you need to download and save the data file from GDELT for this to work.")

font_dirs = ["~/Library/Fonts/"]  # The path to the custom font file
font_files = fm.findSystemFonts(fontpaths=font_dirs)

for font_file in font_files:
    if("Lato" in font_file):
        fm.fontManager.addfont(font_file)

plt.rcParams['font.family'] = 'Lato'


df = pd.read_csv('bquxjob_4fb8a1e_198e8216aa4.csv')
df = df.loc[~df['Person_Mentioned'].isin(['Keir Starmer'])].copy()

data_type_map = {
    "Year": "int64",
    "Month": "int64",
    "Truncated_URL": "string",
    "Person_Mentioned": "category",
    "Mentions": "int64"
}

df = df.astype(data_type_map)

# first turn year and month into a datetime
df['datetime'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
df = df.sort_values(['datetime'])

# Count mentions by month and person mentioned
xf = df.set_index("datetime").groupby([pd.Grouper(freq="ME"), "Person_Mentioned"], observed=False)['Mentions'].sum().reset_index().set_index("datetime").sort_index()

# Use official party colours
# https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Politics_of_the_United_Kingdom/Index_of_United_Kingdom_political_parties_meta_attributes
party_colours_map = {"Nigel Farage": "#12B6CF", "Ed Davey": "#FAA61A", "Kemi Badenoch": "#0087DC"}


# Cut for BBC only version
df["BBC"] = df["Truncated_URL"].str.lower().str.contains("bbc.co.uk")
xfbbc = df.loc[df["BBC"], :].copy()
xfbbc_pro = xfbbc.set_index("datetime").groupby([pd.Grouper(freq="ME"), "Person_Mentioned"], observed=False)['Mentions'].sum().reset_index().set_index("datetime").sort_index()



def mention_plot(xf: pd.DataFrame, suptitle: str, max_mention: int):
    fig, ax = plt.subplots(figsize=(9, 5))
    for person in xf['Person_Mentioned'].unique():
        xgf = xf[xf['Person_Mentioned'] == person]
        
        smoothed = sm.nonparametric.lowess(xgf["Mentions"], xgf.index, frac=0.3, return_sorted=False, it=300)
        ax.scatter(xgf.index, xgf["Mentions"], label=person, alpha=0.6, lw=0, s=30, color=party_colours_map[person])
        ax.plot(xgf.index, smoothed, lw=3, alpha=0.6, color=party_colours_map[person])
        ax.annotate(person, xy=(xgf.index[-1], smoothed[-1]), xytext=(5, 0), 
                    textcoords='offset points', va='center', fontsize=12)
    ax.set_ylabel(None)
    ax.set_title("Mentions", fontsize=14, y=1.04, x=1.07, ha="right", fontstyle="italic")
    ax.set_ylim(0, max_mention)
    ax.set_xlim(pd.Timestamp("2024-01-31"), pd.Timestamp("2025-12-31"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1, interval=6))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    plt.suptitle(suptitle, fontsize=18, ha="left", va="top", x=0.03, y=0.9)
    for key, spine in ax.spines.items():
        spine.set_visible(False)
    ax.tick_params(axis="y", which="both", length=0)
    ax.tick_params(axis="x", which="both", color=[1, 0, 0, 0.5])
    ax.grid(which="major", axis="y", lw=0.2)
    ax.yaxis.tick_right()
    ax.axvline(pd.Timestamp("2024-07-04"), lw=0.2, color="black", alpha=0.3, zorder=0, ls="--")
    ax.annotate("General election", xy=(pd.Timestamp("2024-06-29"), 0.5*max_mention), ha="center", fontsize=9, rotation=90)
    ax.annotate("www.aeturrell.com\nSource: GDELT", xy=(0.95, -0.1), xycoords="axes fraction", fontsize=7, alpha=0.3)
    plt.tight_layout()
    save_name = "mentions_chart_" + hashlib.sha256(suptitle.encode()).hexdigest()[:5] + ".svg"
    plt.savefig(save_name, dpi=400)
    plt.show()


suptitle_one = "Nigel Farage receives more media mentions than other opposition party\nleaders, despite having fewer MPs"

suptitle_two = "Relative to opposition leaders, Farage dominates bbc.co.uk coverage"

mention_plot(xf, suptitle_one, 8e3)
mention_plot(xfbbc_pro, suptitle_two, 25)
