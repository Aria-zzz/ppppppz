"""
Crew 编排模块

使用 CrewAI 的 Hierarchical Process 协调所有 Agent。
支持通过 inputs 传入目的地、天数、预算等动态参数。
"""
import os
from crewai import Crew, Process, LLM

from tasks import (
    research_task,
    hotel_task,
    transport_task,
    itinerary_task,
    budget_task,
)
from agents import (
    researcher,
    hotel_planner,
    transport_planner,
    itinerary_planner,
    budget_analyst,
)


def create_travel_crew() -> Crew:
    """
    创建旅行规划 Crew。

    所有动态参数（目的地、天数、预算、反馈等）
    通过 crew.kickoff(inputs={...}) 传入。
    """
    manager_llm = LLM(
        model=os.getenv("LLM_MODEL", "qwen-plus"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    crew = Crew(
        agents=[
            researcher,
            hotel_planner,
            transport_planner,
            itinerary_planner,
            budget_analyst,
        ],
        tasks=[
            research_task,
            hotel_task,
            transport_task,
            itinerary_task,
            budget_task,
        ],
        process=Process.hierarchical,
        manager_llm=manager_llm,
        verbose=True,
    )
    return crew
