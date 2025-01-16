import streamlit as st
import pandas as pd
# import numpy as np
import pydeck as pdk


pos_kencho = {'lat':35.856701, 'lon':139.650144}  # さいたま市浦和区高砂３丁目



st.set_page_config(
    page_title="Mapping Demo",
    page_icon="🧭"
)

st.sidebar.markdown("Mapping Demo")

st.markdown("## 世帯数マップ(2024年12月01日現在)")

# 標準正規分布に従ったランダム値(埼玉県庁のあたりを中心)  # もう使わない
# chart_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [pos_kencho['lat'], pos_kencho['lon']],
#     columns=["lat", "lon"] 
# )

# 埼玉県市町村別人口情報を読み込む(https://www.pref.saitama.lg.jp/からDL)
population_data = pd.read_excel("埼玉県市町村別人口2024.xlsx", sheet_name="12月", header=5, index_col=0)
# print(population_data.tail())

# 位置情報を読み込む(https://nlftp.mlit.go.jp/からDL)
position_data = pd.read_csv("緯度経度.csv", encoding="shift-jis")
grouped_position_data = position_data.groupby("市区町村コード").first()
grouped_position_data['名称'] = grouped_position_data['市区町村名'].str.replace(r'さいたま市|北足立郡|入間郡|比企郡|秩父郡|児玉郡|大里郡|南埼玉郡|北葛飾郡', '', regex=True)
grouped_position_data.index = grouped_position_data["名称"]

# 人口情報と位置情報を結合
merged_data = pd.concat([grouped_position_data.loc[:, ['緯度', '経度']], population_data.loc[:, ['Households', 'Total']]], axis=1)
merged_data.dropna(inplace=True)  # 位置情報がない市町村(○○郡など)を除外
merged_data.reset_index(names="市町村名", inplace=True)

# 地図を描画
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude= pos_kencho['lat'],
            longitude= pos_kencho['lon'],
            zoom=8,
            pitch=50
        ),
        layers=[pdk.Layer(
            "ColumnLayer",
            # data=chart_data,  # こちらはランダムデータ
            data=merged_data,
            get_position="[経度, 緯度]",
            radius=3000,
            get_elevation="Households",
            elevation_scale=0.3,  # 棒の高さの倍率
            get_fill_color="[255, 140, 0, 140]",
            auto_highlight=True,  # マウスオーバーでハイライト
            pickable=True, # マウスオーバーで情報表示
            extruded=True  # 立体表示
        )],
        tooltip={"text": "{市町村名}:{Households}世帯"}
    )
)

