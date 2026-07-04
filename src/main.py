"""
多 Agent 协作智能旅行规划系统 —— CLI 入口

用法：python -m src.main
"""
import sys
import os
from pathlib import Path
import nest_asyncio
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))

nest_asyncio.apply()

load_dotenv()

PLACEHOLDER_VALUES = {
    "DASHSCOPE_API_KEY": "your_dashscope_api_key_here",
    "TAVILY_API_KEY": "your_tavily_api_key_here",
}


def validate_env() -> None:
    """验证必要的环境变量是否已配置"""
    required_vars = ["DASHSCOPE_API_KEY", "TAVILY_API_KEY"]
    missing = []
    for var in required_vars:
        val = os.getenv(var)
        if not val or val == PLACEHOLDER_VALUES.get(var):
            missing.append(var)
    if missing:
        raise EnvironmentError(
            f"缺少必要的环境变量: {', '.join(missing)}\n"
            f"请复制 .env.example 为 .env 并填入对应的 API Key"
        )


def get_input(prompt: str, default: str) -> str:
    """带默认值的输入"""
    val = input(prompt).strip()
    return val if val else default


def collect_inputs() -> dict:
    """收集用户输入的旅行参数"""
    return {
        "destination": get_input("目的地（默认 东京）: ", "东京"),
        "days": get_input("旅行天数（默认 7）: ", "7"),
        "departure": get_input("出发城市（默认 北京）: ", "北京"),
        "budget": get_input("总预算（元，默认 10000）: ", "10000"),
    }


def main() -> None:
    """主函数：启动旅行规划 Crew，单次运行"""
    print("=" * 60)
    print("  多 Agent 协作智能旅行规划系统")
    print("=" * 60)

    validate_env()
    print("[✓] 环境变量加载完成\n")

    from crew import create_travel_crew

    inputs = collect_inputs()

    print("\n▶ Agent 团队开始工作，请稍候...\n")

    crew = create_travel_crew()
    result = crew.kickoff(inputs=inputs)

    print("\n" + "=" * 60)
    print("  [规划方案]")
    print("=" * 60)
    print(result)
    print("\n感谢使用！祝你旅途愉快！")


if __name__ == "__main__":
    main()
