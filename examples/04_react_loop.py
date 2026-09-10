"""多轮 Agent 循环：模型决策，Python 执行工具，结果回传模型。"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI


def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


available_tools = {"add": add, "multiply": multiply}

tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个整数的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "计算两个整数的乘积",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
]


def run_agent(client: OpenAI, model: str, question: str, max_steps: int = 5) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "你是计算助手。必须使用工具完成计算；多步问题每次只执行当前一步，"
                "得到全部工具结果后再回答。"
            ),
        },
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0,
        )
        message = response.choices[0].message
        if message.content is None:
            message.content = ""
        messages.append(message)

        print(f"第 {step + 1} 轮模型输出：{message.content or message.tool_calls}")

        # 通过判断 message.tool_calls 列表中是否还有内容，来决定是需要下一轮调用工具直接返回 message.content 结果
        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name

            # 异常兜底
            try:
                tool_function = available_tools[tool_name]
                arguments = json.loads(tool_call.function.arguments)
                result = tool_function(**arguments)
            except (KeyError, TypeError, ValueError) as error:
                # 错误转换成工具结果
                result = f"工具执行失败：{error}"

            print(f"Python 执行 {tool_name}，结果：{result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    raise RuntimeError("达到循环上限，仍未获得最终回答")


def main() -> None:
    load_dotenv()
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL_ID")
    if not api_key or not base_url or not model:
        raise RuntimeError("请先在项目根目录的 .env 中填写模型配置")

    client = OpenAI(api_key=api_key, base_url=base_url)
    answer = run_agent(client, model, "先计算 12 加 8，再把结果乘以 3。")
    print("最终回答：", answer)


if __name__ == "__main__":
    main()
