"""
工具配置模块

为 Agent 提供 Tavily 网络搜索能力。
所有工具使用 @tool 装饰器包装，供 CrewAI Agent 调用。
"""
import os
import json
from crewai.tools import tool
from tavily import TavilyClient


# 全局 Tavily 客户端（从环境变量读取 API Key）
_tavily_client: TavilyClient | None = None


def _get_tavily_client() -> TavilyClient:
    """延迟初始化 Tavily 客户端"""
    global _tavily_client
    if _tavily_client is None:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY 未设置，请在 .env 文件中配置"
            )
        _tavily_client = TavilyClient(api_key=api_key)
    return _tavily_client


@tool("search_web")
def search_web(query: str) -> str:
    """
    搜索网络获取旅游相关信息。
    可用于搜索景点、美食、住宿、交通、文化活动等。
    """
    client = _get_tavily_client()
    result = client.search(
        query=query,
        search_depth="advanced",
        include_answer=True,
        max_results=5,
    )
    return json.dumps(result.model_dump(), ensure_ascii=False, indent=2)
