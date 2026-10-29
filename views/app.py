import sqlite3
import pandas as pd
import streamlit as st

# 切换到访客视图，屏蔽网页右上角开发者按钮和“Deploy”
# st.set_option("client.toolbarMode", "viewer")

st.set_page_config(page_title="CMD Output Viewer", layout="wide")
st.title("📟 CMD Output 数据库查看器")

# 使用原生 sqlite3 读取数据并转换为 DataFrame
with sqlite3.connect("cmd_output.db") as conn:
    df = pd.read_sql_query("SELECT * FROM cmd_output_sql ORDER BY id DESC;", conn) # cmd_output_sql是数据库的表格名字

# 优雅地在网页上展示数据
st.dataframe(df, width='stretch')
