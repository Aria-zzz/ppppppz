"""
Agent 定义模块

定义多 Agent 协作旅行规划系统中的所有 Agent。
每个 Agent 有明确的角色、目标和背景故事。
"""
import os
from crewai import Agent, LLM

from tools import search_web


def _create_llm() -> LLM:
    """创建通义千问 LLM 实例"""
    return LLM(
        model=os.getenv("LLM_MODEL", "qwen-plus"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )


# ---------------------------------------------------------------------------
# 搜索研究员
# 负责搜索目的地的景点、美食、文化活动等信息
# ---------------------------------------------------------------------------
researcher = Agent(
    role="搜索研究员",
    goal="搜索目的地的景点、美食、文化活动等旅游信息",
    backstory=(
        "你是一名专业的旅游情报研究员，擅长从互联网上收集并整理"
        "目的地的各种旅游信息，包括必去景点、当地美食、特色活动等。"
        "你的信息是后续规划的基础。"
    ),
    tools=[search_web],
    llm=_create_llm(),
    verbose=True,
    allow_delegation=False,
)

# ---------------------------------------------------------------------------
# 住宿规划员
# 负责搜索并推荐目的地的住宿方案
# ---------------------------------------------------------------------------
hotel_planner = Agent(
    role="住宿规划员",
    goal="搜索并推荐目的地的住宿方案",
    backstory=(
        "你是一名住宿规划专家，熟悉各类酒店、民宿、青旅等住宿类型。"
        "你能根据预算、位置偏好和旅行风格推荐最合适的住宿选项。"
    ),
    tools=[search_web],
    llm=_create_llm(),
    verbose=True,
    allow_delegation=False,
)

# ---------------------------------------------------------------------------
# 交通规划员
# 负责规划城市间及目的地的市内交通
# ---------------------------------------------------------------------------
transport_planner = Agent(
    role="交通规划员",
    goal="规划前往目的地以及当地的交通方案",
    backstory=(
        "你是一位交通规划分析师，擅长规划飞机、高铁、地铁等交通方式。"
        "你能够综合考虑时间、成本和便利性，给出最优交通建议。"
    ),
    tools=[search_web],
    llm=_create_llm(),
    verbose=True,
    allow_delegation=False,
)

# ---------------------------------------------------------------------------
# 行程整合师
# 将景点、住宿、交通等信息整合为完整的行程计划
# ---------------------------------------------------------------------------
itinerary_planner = Agent(
    role="行程整合师",
    goal="综合所有信息，制定详细的每日行程和预算",
    backstory=(
        "你是一名行程整合专家，擅长将景点、住宿、交通等各种碎片化信息"
        "整合成一份合理的每日行程计划，并附上清晰的预算估算。"
        "你确保行程劳逸结合、路线顺畅。"
    ),
    tools=[search_web],
    llm=_create_llm(),
    verbose=True,
    allow_delegation=False,
)

# ---------------------------------------------------------------------------
# 预算分析师
# 根据用户预算，参考其他 Agent 的输出，制定预算分配方案
# ---------------------------------------------------------------------------
budget_analyst = Agent(
    role="预算分析师",
    goal="根据用户预算，参考其他专家的输出，制定详细的预算分配方案",
    backstory=(
        "你是一名精明的旅行预算分析师，擅长将有限的资金合理分配到"
        "交通、住宿、餐饮、门票、购物等各个类别。"
        "你总是能给出最经济实惠的建议，在预算范围内最大化旅行体验。"
    ),
    llm=_create_llm(),
    verbose=True,
    allow_delegation=False,
)

# 导出所有 Agent
__all__ = [
    "researcher",
    "hotel_planner",
    "transport_planner",
    "itinerary_planner",
    "budget_analyst",
]
