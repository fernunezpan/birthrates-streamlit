import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Birthrates Over Time")

@st.cache_data
def load_data():
    return pd.read_csv("fertility_worldbank.csv")

df_all = load_data()

# creating region_weighted to elaborate regions graphs

region_weighted = (
    df_all.groupby(["region", "year"], as_index=False)
          .apply(lambda g: (g["tfr"] * g["population"]).sum() / g["population"].sum())
          .rename(columns={None: "tfr_region"})
)
df_all["region"] = df_all["region"].astype(str).str.strip()
region_weighted["region"] = region_weighted["region"].astype(str).str.strip()


# Static replica of NY Times graph

st.subheader("Static recreation (NYT-style)")

fig, ax = plt.subplots(figsize=(12, 7))

ax.set_xlim(1960, 2023)
ax.set_ylim(0.8, 7.1)

# Grid horizontal smooth (NYT-style)
ax.yaxis.grid(True, color="#E6E6E6", linewidth=1)
ax.xaxis.grid(False)

# Remove unnecesary edges
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)

ax.spines["bottom"].set_color("#333333")

# Ticks
ax.tick_params(axis="y", length=0, colors="#6E6E6E")
ax.tick_params(axis="x", colors="#6E6E6E")

ax.set_ylabel("")
ax.set_xlabel("")

context_color = "#BDBDBD"


# REGIONS

regions_to_plot = sorted(region_weighted["region"].unique())

for reg in regions_to_plot:
    sub = region_weighted[region_weighted["region"] == reg]
    ax.plot(
        sub["year"],
        sub["tfr_region"],
        color="#BDBDBD",
        linewidth=1.4,
        alpha=0.9,
        zorder=1
    )


# COUNTRIES


colors = {
    "United States": "#3B64A1",
    "France": "#E36A3B",
    "Norway": "#BC3939",
    "Canada": "#F6DD6F",
    "Mexico": "#785171",
    "Israel": "#CEB0C6",
    "Hungary": "#4F4F4F",
}

for label, color in colors.items():
    sub = df_all[df_all["name"] == label]
    ax.plot(
        sub["year"],
        sub["tfr"],
        color=color,
        linewidth=2.8,
        zorder=3
    )

# Countries label

label_positions = {
    "Mexico": 1988,
    "Israel": 2018,
    "United States": 1996,
    "France": 1974,
    "Norway": 1982,
    "Hungary": 2000,
    "Canada": 2018,
}

label_offsets = {   # offset vertical en “hijos por mujer”
    "Mexico": 0.08,
    "Israel": -0.08,
    "United States": 0.10,
    "France": 0.06,
    "Norway": -0.06,
    "Hungary": -0.10,
    "Canada": -0.06,
}

for name, year_pos in label_positions.items():
    sub = df_all[(df_all["name"] == name) & (df_all["year"] == year_pos)]
    if not sub.empty:
        y = sub["tfr"].iloc[0] + label_offsets.get(name, 0.0)
        ax.text(
            year_pos + 1, y, name,
            color=colors[name],
            fontsize=14,            # más presencia
            fontweight="medium",
            va="center", ha="left",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.6, pad=0.2)  # opcional
        )

# Regions label

region_label_year = {
    "Sub-Saharan Africa": 2012,
    "South Asia": 1984,
    "Middle East, North Africa, Afghanistan & Pakistan": 1990,
    "Latin America & Caribbean": 1976,
    "East Asia & Pacific": 1962,
    "Europe & Central Asia": 1970,
    "North America": 1961,
}

region_label_offset = {
    "Sub-Saharan Africa": 0.10,
    "South Asia": 0.06,
    "Middle East, North Africa, Afghanistan & Pakistan": 0.06,
    "Latin America & Caribbean": -0.5,
    "East Asia & Pacific": -1,
    "Europe & Central Asia": 0.06,
    "North America": -0.06,
}


for reg, year_pos in region_label_year.items():
    sub = region_weighted[(region_weighted["region"] == reg) & (region_weighted["year"] == year_pos)]
    if not sub.empty:
        y = sub["tfr_region"].iloc[0] + region_label_offset.get(reg, 0.0)
        ax.text(
            year_pos + 1, y, reg,
            color="#9E9E9E",
            fontsize=12,
            va="center", ha="left"
        )

# Details

ax.text(
    1958,    # posicion horizontal justo fuera del grafico
    7.2,     # un poquito arriba de tu límite superior del eje
    "children",
    fontsize=13,
    fontweight="bold",
    color="#333333",
    va="bottom"
)

fig.text(
    0.5,        # x desde 0 (izquierda) hasta 1 (derecha), 0.5 = centro
    0.01,       # y muy abajo
    "SOURCE: World Bank (fertility rate, population) from 1960 to 2023",
    fontsize=10,
    color="#6E6E6E",
    ha="center",
    va="bottom"
)

plt.show()



st.pyplot(fig, clear_figure=True)