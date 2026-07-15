import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("onsen_seikei.csv")

df["評価数値"] = (
    df["評価"]
    .astype(str)
    .str.extract(r"(\d+\.\d+)")[0]
    .astype(float)
)

st.title("福井県 温泉・サウナ検索")

st.write("評価や地域から、福井県の温泉施設を探せるアプリです。")

min_score = st.slider(
    "評価の下限",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)

areas = ["すべて"] + sorted(df["地域"].dropna().unique().tolist())
selected_area = st.selectbox("地域を選択", areas)

filtered_df = df[df["評価数値"] >= min_score].copy()

if selected_area != "すべて":
    filtered_df = filtered_df[filtered_df["地域"] == selected_area]

st.subheader("検索結果")

st.dataframe(
    filtered_df[
        ["温泉名", "地域", "評価", "日帰り", "タイトルURL"]
    ],
    use_container_width=True
)

fig = px.bar(
    filtered_df,
    x="温泉名",
    y="評価数値",
    title="温泉施設ごとの評価",
    hover_data=["地域", "評価", "日帰り"]
)

st.plotly_chart(fig, use_container_width=True)