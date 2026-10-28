import streamlit as st
import pandas as pd
import os
import sqlite3

st.set_page_config(page_title="CMD 输出汇总列表", layout="wide")
st.title("🗄️ Linux shell CMD输出汇总展示 (SQLite 数据库方案)")

DB_FILE = "cmd_output.db"

if os.path.exists(DB_FILE):
    try:
        # 1. 建立数据库连接并读取数据
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql("SELECT * FROM cmd_output_sql", conn)
        conn.close()
        
        # 2. [倒序排列] 将最新数据置顶
        df = df[::-1].reset_index(drop=True)
        
        # 如果存在自增 ID 列则将其移除
        if "ID" in df.columns:
            df = df.drop(columns=["ID"])

        # 🔍 3. 全局关键词搜索框
        search_query = st.text_input("🔍 输入关键词进行全局实时检索（支持任意文字）:", "")
        
        if search_query:
            # 所有列转为字符串并进行不区分大小写的模糊匹配
            search_mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            df = df[search_mask]

        # 4. 动态扫描列配置
        column_main_config = {}
        for column_name in df.columns:
            if "JSON" in str(column_name) or column_name == "原始JSON数据树":
                column_main_config[column_name] = st.column_config.JsonColumn(column_name)
            else:
                column_main_config[column_name] = st.column_config.TextColumn(column_name)

        # 5. 数据表格渲染
        st.subheader(f"📂 正在实时读取数据库当前表: `{DB_FILE}`")
        st.dataframe(
            df, 
            hide_index=True,
            column_config=column_main_config,
            width='content'
        )
        st.caption(f"💡 提示：当前展示了 {len(df)} 条状态记录，最新生成的数据已优先置顶。")

    except Exception as e:
        st.error(f"读取 SQLite 数据库失败: {e}")
else:
    st.warning(f"⚠️ 尚未生成数据库文件。请先运行 `python capture_cmd.py` 初始化数据库。")
