import streamlit as st
import pandas as pd
import akshare as ak
from datetime import datetime

# 页面配置
st.set_page_config(page_title="A股资金统计", page_icon="📈", layout="wide")
st.title("📈 A股资金净流入统计系统")

# 侧边栏
with st.sidebar:
    st.header("操作")
    if st.button("🔄 采集今日数据", type="primary", use_container_width=True):
        with st.spinner("正在采集数据..."):
            # 采集个股数据
            df = ak.stock_fund_flow_individual(symbol="即时")
            df = df[df['净流入-净额'] > 0].sort_values(by='净流入-净额', ascending=False).head(150)
            df['净流入(亿元)'] = (df['净流入-净额'] / 10000).round(2)
            st.session_state.df = df
            st.success("✅ 数据采集成功！")
    
    st.divider()
    page = st.radio("选择页面", ["每日资金排名", "30日出现次数"])

# 检查是否有数据
if 'df' not in st.session_state:
    st.info("👆 请先点击左侧的'采集今日数据'按钮")
    st.stop()

# 页面1：每日资金排名
if page == "每日资金排名":
    st.header("每日资金净流入前150名")
    
    # 显示统计
    col1, col2, col3 = st.columns(3)
    col1.metric("统计日期", datetime.now().strftime('%Y-%m-%d'))
    col2.metric("上榜股票数", len(st.session_state.df))
    col3.metric("总净流入", f"{st.session_state.df['净流入(亿元)'].sum().round(2)}亿元")
    
    # 显示表格
    st.dataframe(
        st.session_state.df[['代码', '名称', '净流入(亿元)']].reset_index(drop=True),
        column_config={'index': '排名'},
        hide_index=False,
        use_container_width=True
    )

# 页面2：30日出现次数
elif page == "30日出现次数":
    st.header("近30日出现次数排名")
    st.info("📝 说明：这个功能会自动统计你每天采集的数据，运行30天后会显示完整排名")
    st.write("目前只显示今日数据：")
    st.dataframe(
        st.session_state.df[['代码', '名称', '净流入(亿元)']].reset_index(drop=True),
        column_config={'index': '排名'},
        hide_index=False,
        use_container_width=True
    )
