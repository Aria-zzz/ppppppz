"""
多 Agent 协作智能旅行规划系统 —— Streamlit Web 界面

用法：
    streamlit run src/app.py
"""
import sys
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))

load_dotenv()

# ── 页面配置 ─────────────────────────────────────────────
st.set_page_config(
    page_title="智能旅行规划系统",
    page_icon="✈️",
    layout="wide",
)

PLACEHOLDER_VALUES = {
    "DASHSCOPE_API_KEY": "your_dashscope_api_key_here",
    "TAVILY_API_KEY": "your_tavily_api_key_here",
}


def env_ok() -> bool:
    """检查环境变量是否已配置"""
    for var in ["DASHSCOPE_API_KEY", "TAVILY_API_KEY"]:
        val = os.getenv(var)
        if not val or val == PLACEHOLDER_VALUES.get(var):
            return False
    return True


# ── 侧边栏 - 输入参数 ──────────────────────────────────
st.sidebar.title("✈️ 旅行参数")

destination = st.sidebar.text_input("目的地", value="东京")
days = st.sidebar.number_input("旅行天数", min_value=1, max_value=30, value=7)
departure = st.sidebar.text_input("出发城市", value="北京")
budget = st.sidebar.number_input(
    "总预算（元）", min_value=500, max_value=100000, value=10000, step=500
)

run_btn = st.sidebar.button("🚀 开始规划", type="primary", use_container_width=True)

# ── 主区域 ──────────────────────────────────────────────
st.title("🌏 智能旅行规划系统")
st.markdown("多 Agent 协作，为你定制专属旅行方案")

if not env_ok():
    st.error(
        "⚠️ 环境变量未配置！请先在 `.env` 文件中填入 "
        "`DASHSCOPE_API_KEY` 和 `TAVILY_API_KEY`"
    )
    if st.button("查看 .env.example"):
        with open(".env.example") as f:
            st.code(f.read())
    st.stop()

from crew import create_travel_crew

# ── 会话状态初始化 ────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

# ── 运行规划 ──────────────────────────────────────────
if run_btn:
    with st.spinner("🧠 Agent 团队正在工作中…\n（搜索研究员 → 住宿规划员 → 交通规划员 → 行程整合师 → 预算分析师）"):
        crew = create_travel_crew()
        inputs = {
            "destination": destination,
            "days": str(days),
            "departure": departure,
            "budget": str(budget),
        }
        st.session_state.result = crew.kickoff(inputs=inputs)

# ── 显示结果 ──────────────────────────────────────────
if st.session_state.result:
    st.markdown("---")
    st.subheader("📋 旅行规划方案")
    st.markdown(st.session_state.result)

    st.markdown("---")
    if st.button("💾 保存方案", type="primary"):
        filename = f"travel_plan_{destination}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {destination} 旅行规划\n\n")
            f.write(st.session_state.result)
        st.success(f"方案已保存到 {filename}")

# ── 页脚信息 ──────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption("基于 CrewAI + 通义千问 + Tavily 构建")
