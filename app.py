import json
import numpy as np
import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output
from dash.dash_table import DataTable

# LOAD DATA
df = pd.read_csv("Main raw file last.csv")
df["Region"] = df["Region"].str.strip()

METRICS = {
    "income": "State budget income",
    "expense": "State budget expenditure",
    "grp": "Gross Regional Product",
    "grp_pc": "Gross Regional Product per Capita",
    "debt": "Public Debt",
}

region_options = sorted(df["Region"].dropna().unique())
years = sorted(df["Year"].dropna().astype(int).unique())
default_year = years[-1]

REGION_MAP = {
    "Andijon": "Andijan region",
    "Buxoro": "Bukhara region",
    "Farg'ona": "Fergana region",
    "Jizzax": "Jizzakh region",
    "Namangan": "Namangan region",
    "Navoiy": "Navoi region",
    "Qashqadaryo": "Kashkadarya region",
    "Qoraqalpog'iston": "Republic of Karakalpakstan",
    "Qaraqalpaqstan": "Republic of Karakalpakstan",
    "Samarqand": "Samarkand region",
    "Sirdaryo": "Syrdarya region",
    "Surxondaryo": "Surkhandarya region",
    "Toshkent": "Tashkent region",
    "ToshkentShahri": "Tashkent city",
    "Xorazm": "Khorezm region",
}

with open("uzbekistan_regions.geojson.json", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

for feat in geojson_data["features"]:
    name = feat["properties"].get("NAME_1")
    if name in REGION_MAP:
        feat["properties"]["NAME_1"] = REGION_MAP[name]

# APP

app = Dash(__name__)
server = app.server
app.title = "Uzbekistan Macroeconomic Insights"

def build_debt_trend_figure():
    d = df[df["Metric"] == METRICS["debt"]].copy()
    debt_by_year = d.groupby("Year", as_index=False)["Value"].sum().sort_values("Year")
    fig = px.line(
        debt_by_year,
        x="Year", y="Value", markers=True,
        title="Public Debt — Trend Over Time, measured in millions of USD",
        labels={"Year": "Year", "Value": "Millions of USD"})
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor="white",
        margin=dict(l=60, r=40, t=70, b=50),
        xaxis=dict(
        showline=True,   # show line along x-axis
        linewidth=1,
        linecolor='gray',  # color of x-axis line
        mirror=False        # draw axis lines on both sides
    ),
        yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='gray',
        mirror=False
        ),)
    fig.update_xaxes(type="category")
    return fig

# LAYOUT

app.layout = html.Div([
    # === DASHBOARD HEADER ===
    html.Div(
        [html.Div([
                    html.H1("Uzbekistan Macroeconomic Insights",
                    style={
                        "margin": "8px 8px 8px",
                        "fontSize": "30px",
                        "fontWeight": "bold",
                        "color": "#0b3954"}),
                    html.P("An interactive data app exploring fiscal metrics of the Republic of Uzbekistan within its regions and sectors from 2020–2024.",
                    style={
                        "fontSize": "17px",
                        "maxWidth": "700px",
                        "margin": "8px 8px 8px"}),
                    ],
                    style={
                        "display": "flex", 
                        "flexDirection": "column", 
                        "justifyContent": "center"},
                    ),
            html.Img(src="https://www.imv.uz/_nuxt/img/logo-en.6ef2880.png",style={"height": "85px", "marginLeft": "25px", "borderRadius": "8px"}),
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "padding": "8px 8px",
            "backgroundColor": "#f5f7fa",
            "borderBottom": "5px solid #ddd",
            "marginBottom": "20px",
            "borderRadius": "8px",},
    ),

    # KPI SECTION
    html.H2("Main Macroeconomic Indicators", className="section-title"),
    html.Div(
        [html.Label("Select Year:", className="dropdown-label1"),
            dcc.Dropdown(
                id="kpi-year",
                options=[{"label": int(y), "value": int(y)} for y in years],
                value=default_year,
                clearable=False,
                className="year-dropdown1"),
        ],
        className="dropdown-row1",
    ),
    
    html.Div(
        [html.Div(
                [
                    html.Div("Budget Income", className="kpi-title"),
                    html.Div(id="kpi-income", className="kpi-value"),
                    html.Div("Measured in billions of UZS", className="kpi-sub"),
                ],
                className="kpi-card accent-green",
            ),
            html.Div(
                [
                    html.Div("Budget Expenditure", className="kpi-title"),
                    html.Div(id="kpi-expense", className="kpi-value"),
                    html.Div("Measured in billions of UZS", className="kpi-sub"),
                ],
                className="kpi-card accent-red",
            ),
            html.Div(
                [
                    html.Div("Net Balance", className="kpi-title"),
                    html.Div(id="kpi-net", className="kpi-value"),
                    html.Div("Measured in billions of UZS", className="kpi-sub"),
                ],
                className="kpi-card accent-blue",
            ),
            html.Div(
                [
                    html.Div("Average GRP", className="kpi-title"),
                    html.Div(id="kpi-grp", className="kpi-value"),
                    html.Div("Measured in billions of UZS", className="kpi-sub"),
                ],
                className="kpi-card accent-indigo",
            ),
            html.Div(
                [
                    html.Div("GRP per Capita", className="kpi-title"),
                    html.Div(id="kpi-grppc", className="kpi-value"),
                    html.Div("Measured in thousands of UZS", className="kpi-sub"),
                ],
                className="kpi-card accent-teal",
            ),
            html.Div(
                [
                    html.Div("Public Debt", className="kpi-title"),
                    html.Div(id="kpi-debt", className="kpi-value"),
                    html.Div("Measured in millions of USD", className="kpi-sub"),
                ],
                className="kpi-card accent-amber",
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            "paddingBottom": "6px",
        },
    ),
    html.Hr(style={"border": "1px solid #ccc", "marginTop": "22px"}),





    # LINE & AREA CHARTS
    html.Div(
        [
            html.Div(
                [
                    html.H2(
                        "Trend of Budget Income and Budget Expenditure",
                        className="section-title",
                    ),
                    dcc.Graph(id="line-chart", style={"height": "80vh", "width": "100%",}),
                    html.Div(
                        [
                            html.Label("Select Year Range:", className="dropdown-label1"),
                            html.Div(
                                dcc.RangeSlider(
                                    id="year-range",
                                    min=int(min(years)),
                                    max=int(max(years)),
                                    step=1,
                                    value=[int(min(years)), int(max(years))],
                                    marks={int(y): {"label": str(y)} for y in years},
                                    allowCross=False,
                                    updatemode="mouseup",
                                ),
                                className="control-input",
                                style={"width": "100%"},
                            ),
                        ],
                        className="chart-control control-column",
                        style={"width": "100%"},
                    ),
                ],
                className="chart-panel",
            ),







            #Area Chart by Region
            html.Div(
                [
                    html.H2(
                        "State Budget Income and Budget Expenditure by Region",
                        className="section-title",
                    ),
                    dcc.Graph(id="region-area-chart", style={"height": "80vh", "width": "100%"}),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Select Region(s):", className="dropdown-label1"),
                                    dcc.Dropdown(
                                        id="region-dropdown",
                                        options=[{"label": r, "value": r} for r in region_options],
                                        value=[],
                                        placeholder="Select region(s) or leave empty for all",
                                        multi=True,
                                        clearable=True,
                                        className="year-dropdown1",
                                    ),
                                ],
                                className="dropdown-row1",
                            ),
                            html.Div(
                                [
                                    html.Label("Select Year:", className="dropdown-label1"),
                                    dcc.Dropdown(
                                        id="year-dropdown",
                                        options=[{"label": y, "value": y} for y in years],
                                        value=years[-1] if years else None,
                                        clearable=False,
                                        className="year-dropdown1",
                                    ),
                                ],
                                className="dropdown-row1",
                            ),
                        ],
                        className="chart-control control-column",
                    ),
                ],
                className="chart-panel",
            ),
        ],
        className="side-by-side-section",
    ),html.Hr(className="section-divider"),

    
    
    
    
    
   # === State External Debt ===
html.H2("State External Debt Information", className="section-title"),

html.Div([
    # Left: Trend chart
    html.Div(
        dcc.Graph(
            id="debt-trend",
            figure=build_debt_trend_figure(),
            style={"height": "500px", "width": "100%"},
        ),
        style={"flex": "1"},
    ),

    # Right: Top creditors (filter + table)
    html.Div([
        html.Div([
            html.Label("Select Year:", className="dropdown-label1"),
            dcc.Dropdown(
                id="debt-year",
                options=[
                    {"label": int(y), "value": int(y)}
                    for y in sorted(
                        df.loc[df["Metric"] == METRICS["debt"], "Year"]
                          .dropna().astype(int).unique()
                    )
                ],
                value=int(
                    sorted(
                        df.loc[df["Metric"] == METRICS["debt"], "Year"]
                          .dropna().astype(int).unique()
                    )[-1]
                ),
                clearable=False,
                className="year-dropdown1",
            ),
        ], className="dropdown-row1"),

        DataTable(
            id="debt-by-creditor",
            columns=[
                {"name": "Top 10 Debt Providers", "id": "Creditor"},
                {"name": "Amount in millions of USD", "id": "Value"},
            ],
            data=[],
            style_table={"overflowX": "auto"},
            style_cell={
                "padding": "10px",
                "fontSize": "15px",
                "fontFamily": "Arial, sans-serif",
                "border": "1px solid #ddd",
            },
            style_cell_conditional=[
                {"if": {"column_id": "Creditor"}, "textAlign": "left", "width": "70%"},
                {"if": {"column_id": "Value"}, "textAlign": "right", "width": "30%"},
            ],
            style_header={
                "backgroundColor": "#f8f8f8",
                "fontWeight": "bold",
                "fontSize": "16px",
                "textAlign": "center",
                "borderBottom": "2px solid #ccc",
            },
        ),
    ], style={"flex": "1"}),
],
style={
    "display": "flex",
    "flexDirection": "row",
    "alignItems": "flex-start",
    "justifyContent": "space-between",
    "gap": "8px",   
    "marginTop": "16px",
}),

html.Hr(style={"border": "1px solid #ccc", "marginTop": "24px", "marginBottom": "24px"}),

    # === MAP ===
    html.H2("Geographical View of GRP & GRP per Capita", className="section-title"),
    html.Div([
        html.Div([
            html.Label("Select Year:", className="dropdown-label1"),
            dcc.Dropdown(id="map-year", options=[{"label": int(y), "value": int(y)} for y in years],
                         value=default_year, clearable=False, className="year-dropdown1"),
        ], className="dropdown-row1"),
        dcc.RadioItems(id="map-metric",
                       options=[{"label": " GRP (Gross Regional Product)", "value": "grp"},
                                {"label": " GRP per Capita", "value": "grp_pc"}],
                       value="grp", labelStyle={"display": "inline-block", "marginRight": "16px"}),
    ]),
    dcc.Graph(id="grp-map", style={"height": "600px"})
])






# CALLBACKS

@app.callback(
    Output("line-chart", "figure"),
    Input("year-range", "value"),
)
def update_line_chart(year_range):
    start_year, end_year = map(int, year_range)

    d0 = df[df["Metric"].isin([METRICS["income"], METRICS["expense"]])]
    d0 = d0.dropna(subset=["Sector"])
    d0 = d0[(d0["Year"] >= start_year) & (d0["Year"] <= end_year)]

    d_agg = (
        d0.groupby(["Year", "Metric"], as_index=False)["Value"]
        .sum()
        .sort_values("Year")
    )

    fig = px.line(
        d_agg,
        x="Year",
        y="Value",
        color="Metric",
        markers=True,
        labels={"Value": "Billions of UZS", "Year": "Year", "Metric": "Type"},
    )
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor="white",
        legend_title="Metric",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
        ),
        xaxis=dict(
        showline=True,   # show line along x-axis
        linewidth=1,
        linecolor='gray',  # color of x-axis line
        mirror=False        # draw axis lines on both sides
    ),
        yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='gray',
        mirror=False
        ), 
        margin=dict(l=60, r=40, t=70, b=100),
    )
    fig.update_xaxes(type="category")
    return fig


@app.callback(
    Output("region-area-chart", "figure"),
    [Input("region-dropdown", "value"), Input("year-dropdown", "value")],
)
def update_area_chart(selected_regions, selected_year):
    dff = df[(df["Year"] == selected_year) & (df["Metric"].isin([METRICS["income"], METRICS["expense"]]))]
    if selected_regions:
        dff = dff[dff["Region"].isin(selected_regions)]

    dff = (
        dff.groupby(["Region", "Metric"], as_index=False)["Value"]
        .sum()
        .dropna(subset=["Region"])
        .sort_values("Region")
    )

    fig = px.area(
        dff,
        x="Region",
        y="Value",
        color="Metric",
        color_discrete_map={METRICS["income"]: "green", METRICS["expense"]: "red"},
        labels={"Value": "Billions of UZS"},
    )
    for tr in fig.data:
        tr.update(stackgroup=None, fill="tozeroy", opacity=0.35, line=dict(width=2))

    fig.update_layout(
        title_x=0.2,
        xaxis_tickangle=-30,
        plot_bgcolor="white",
        legend_title="Metric",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.7,
            xanchor="center",
            x=0.5,
        ),
        xaxis=dict(
        showline=True,   # show line along x-axis
        linewidth=1,
        linecolor='gray',  # color of x-axis line
        mirror=False        # draw axis lines on both sides
    ),
        yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='gray',
        mirror=False
        ),
        margin=dict(l=80, r=40, t=70, b=120),
    )
    return fig


@app.callback(
    Output("kpi-income", "children"),
    Output("kpi-expense", "children"),
    Output("kpi-net", "children"),
    Output("kpi-grp", "children"),
    Output("kpi-grppc", "children"),
    Output("kpi-debt", "children"),
    Input("kpi-year", "value"),
)
def update_kpis(year):
    def fmt(x):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return "—"
        return f"{x:,.0f}"

    dyear = df[df["Year"] == year]
    total_income = dyear[(dyear["Metric"] == METRICS["income"]) & dyear["Sector"].notna()]["Value"].sum()
    total_expense = dyear[(dyear["Metric"] == METRICS["expense"]) & dyear["Sector"].notna()]["Value"].sum()
    net_balance = total_income - total_expense
    avg_grp = dyear[dyear["Metric"] == METRICS["grp"]]["Value"].mean()
    avg_grppc = dyear[dyear["Metric"] == METRICS["grp_pc"]]["Value"].mean()
    debt_df = dyear[dyear["Metric"] == METRICS["debt"]]["Value"]
    public_debt = debt_df.sum() if not debt_df.empty else 0

    return (
        fmt(total_income),
        fmt(total_expense),
        fmt(net_balance),
        fmt(avg_grp),
        fmt(avg_grppc),
        fmt(public_debt),
    )


@app.callback(Output("grp-map", "figure"),
              [Input("map-year", "value"), Input("map-metric", "value")])
def update_map(year, metric):
    m = METRICS["grp"] if metric == "grp" else METRICS["grp_pc"]
    d = df[(df["Year"] == year) & (df["Metric"] == m)].dropna(subset=["Region"]).groupby("Region", as_index=False)["Value"].sum()
    fig = px.choropleth(d, geojson=geojson_data, locations="Region",
                        featureidkey="properties.NAME_1", color="Value", color_continuous_scale="YlGnBu",
                        hover_name="Region", hover_data={"Value": ":,.0f"},
                        title=f"Uzbekistan — {m} by Region ({year})")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20), paper_bgcolor="white")
    return fig


@app.callback(
    Output("debt-by-creditor", "data"),
    Input("debt-year", "value"),
)
def update_debt_by_creditor_table(year):
    d = df[(df["Metric"] == METRICS["debt"]) & (df["Year"] == year)].copy()

    if "Creditor" in d.columns:
        d = d.dropna(subset=["Creditor"])
        tbl = (
            d.groupby("Creditor", as_index=False)["Value"]
            .sum()
            .sort_values("Value", ascending=False)
            .head(10)
        )
    else:
        total = d["Value"].sum()
        tbl = pd.DataFrame([{"Creditor": "Total", "Value": total}])

    tbl["Value"] = tbl["Value"].fillna(0).round(0).map(lambda x: f"{x:,.0f}")
    return tbl.to_dict("records")


if __name__ == "__main__":
    app.run(debug=True)

