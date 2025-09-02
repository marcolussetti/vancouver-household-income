import streamlit as st
import pandas as pd
import numpy as np
import altair as alt



def get_data():
    df = pd.read_csv("data.csv")

    df.columns = ["Location", "Avg Pretax", "Median Pretax", "Avg Aftertax", "Median Aftertax"]
    df["Avg Tax"] = df["Avg Pretax"] - df["Avg Aftertax"]
    df["Median Tax"] = df["Median Pretax"] - df["Median Aftertax"]
    df["Avg Tax Rate" ] = (df["Avg Pretax"] - df["Avg Aftertax"]) /  df["Avg Pretax"]
    df["Median Tax Rate" ] = (df["Median Pretax"] - df["Median Aftertax"]) /  df["Median Pretax"]

    df = df[["Location", "Median Pretax", "Median Aftertax", "Median Tax Rate", "Avg Pretax", "Avg Aftertax", "Avg Tax Rate"]]
    return df

def main():
    df = get_data()

    st.write("""
# Household Income in the Greater Vancouver Area""")
    
    median_or_average = st.radio(
        "",
        ["Median", "Avg"]
    )
    
    chart_data = df[["Location", f"{median_or_average} Aftertax"]].copy()
    chart_data[f"{median_or_average} Tax"] = df[f"{median_or_average} Pretax"] - df[f"{median_or_average} Aftertax"]
    
    melted_data = pd.melt(
        chart_data, 
        id_vars=['Location'], 
        value_vars=[f"{median_or_average} Aftertax", f"{median_or_average} Tax"],
        var_name='Type', 
        value_name='Amount'
    )
    
    max_scale = max(df["Avg Pretax"].max(), df["Median Pretax"].max())

    # chart = alt.Chart(melted_data).mark_bar().encode(
    #     x=alt.X('Location:N', axis=alt.Axis(labelLimit=0)),
    #     y=alt.Y('Amount:Q', scale=alt.Scale(domain=[0, max_scale])),
    #     color=alt.Color('Type:N', legend=alt.Legend(orient='top')),
    #     order=alt.Order('Type:N', sort='ascending')
    # )
    chart = alt.Chart(melted_data).mark_bar().encode(
        y=alt.Y('Location:N', axis=alt.Axis(labelLimit=0)),
        x=alt.X('Amount:Q', scale=alt.Scale(domain=[0, max_scale]), axis=alt.Axis(orient='top')),
        color=alt.Color('Type:N', legend=alt.Legend(orient='top')),
        order=alt.Order('Type:N', sort='ascending')
    )
    
    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()
