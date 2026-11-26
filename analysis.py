import pandas as pd
import matplotlib.pyplot as plt
import os

DATA = "."
IMAGES = "."

def load_csv(filename):
    path = os.path.join(DATA, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path)

def clean_year_column(df, year_col="year"):
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    if year_col not in df.columns:
        for c in df.columns:
            if "year" in c or "år" in c:
                df = df.rename(columns={c: year_col})
                break
    df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
    return df.dropna(subset=[year_col])

def save_chart(fig, name):
    path = os.path.join(IMAGES, name)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")

# 1. Population in Stavanger
population = clean_year_column(load_csv("population_stavanger.csv"))
value_col = [c for c in population.columns if c != "year"][0]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(population["year"], population[value_col], marker="o", color="#1f4e79")
ax.set_title("Population in Stavanger")
ax.set_xlabel("Year")
ax.set_ylabel("Population")
ax.grid(True)
save_chart(fig, "population_stavanger.png")

# 2. Unemployment in Rogaland
unemployment = clean_year_column(load_csv("unemployment_rogaland.csv"))
rate_col = [c for c in unemployment.columns if c != "year"][0]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(unemployment["year"], unemployment[rate_col], marker="o", color="darkred")
ax.set_title("Unemployment rate in Rogaland")
ax.set_xlabel("Year")
ax.set_ylabel("Unemployment rate (%)")
ax.grid(True)
save_chart(fig, "unemployment_rogaland.png")

# 3. Employment by sex in Rogaland
employment = clean_year_column(load_csv("employment_rogaland.csv"))
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(employment["year"], employment["men"], label="Men", color="#1f4e79")
ax.plot(employment["year"], employment["women"], label="Women", color="#d97706")
ax.plot(employment["year"], employment["total"], label="Total", color="#333333")
ax.set_title("Employment in Rogaland by sex")
ax.set_xlabel("Year")
ax.set_ylabel("Employed people")
ax.legend()
ax.grid(True)
save_chart(fig, "employment_by_sex.png")

# 4. Immigration background in Stavanger
immigration = clean_year_column(load_csv("immigration_stavanger.csv"))
if "value" in immigration.columns:
    pivot = immigration.pivot_table(index="year", columns="category", values="value", aggfunc="sum")
else:
    category_col = [c for c in immigration.columns if c != "year"][0]
    pivot = immigration.pivot_table(index="year", columns=category_col, values=category_col, aggfunc="first")
fig, ax = plt.subplots(figsize=(10, 5))
pivot.plot(ax=ax, marker="o")
ax.set_title("Population by immigration background in Stavanger")
ax.set_xlabel("Year")
ax.set_ylabel("Population")
ax.legend(title="Category")
ax.grid(True)
save_chart(fig, "immigration_stavanger.png")

# 5. Employment by industry in Rogaland
industry = clean_year_column(load_csv("employment_by_industry_rogaland.csv"))
latest_year = industry["year"].max()
latest = industry[industry["year"] == latest_year].sort_values("employment")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(latest["industry"], latest["employment"], color="#1f4e79")
ax.set_title(f"Employment by industry in Rogaland, {int(latest_year)}")
ax.set_xlabel("Employed people")
ax.grid(True, axis="x")
save_chart(fig, "employment_by_industry.png")

print("Analysis finished. Check the images folder for your charts.")
