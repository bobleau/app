import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CMD Output Viewer", layout="wide")
st.title("📟 CMD Output 数据库查看器")

# 使用原生 sqlite3 读取数据并转换为 DataFrame
with sqlite3.connect("cmd_output.db") as conn:
    # df = pd.read_sql_query("SELECT * FROM your_table_name ORDER BY id DESC;", conn)
    df = pd.read_sql_query("SELECT * FROM cmd_output_sql ORDER BY id DESC;", conn)

# 优雅地在网页上展示数据（支持搜索、排序和全屏查看）
st.dataframe(df, use_container_width=True)
