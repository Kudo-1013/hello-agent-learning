"""真实 Function Calling：模型选择工具，Python 执行并回传结果。"""

import os
import json

from dotenv import load_dotenv
from openai import OpenAI

def multiply(a: int, b: int) -> int:
    return a * b

def add(a: int, b: int) -> int:
    return a + b

available_tools = {
    "multiply":multiply,
    "add": add,
}

# Python 函数：由程序实际执行任务
# tools 说明：帮助模型选择工具、填写参数

tools = [
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "计算两个整数的乘积",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个整数"},
                    "b": {"type": "integer", "description": "第二个整数"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },{
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个整数的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个整数"},
                    "b": {"type": "integer", "description": "第二个整数"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
        }
]


def main() -> None:
    # 读取模型配置
    load_dotenv()
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL_ID")
    if not api_key or not base_url or not model:
        raise RuntimeError("请先在项目根目录的 .env 中填写模型配置")

    client = OpenAI(api_key=api_key, base_url=base_url)

    messages=[
                {
                    "role": "system",
                    "content": "你是计算助手。遇到算术问题时，必须调用合适的工具计算。"
                },
                {
                    "role": "user",
                    "content": "请调用工具计算 12 加 8，不要直接口算。",
                }
            ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0,
    )
    print("第一次调用 Token: ", response.usage)

    message = response.choices[0].message
    print("模型文本：", message.content)
    print("工具调用请求：", message.tool_calls)
    if not message.tool_calls:
        raise RuntimeError("模型没有选择工具，请重新运行一次")
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)

    tool_name = tool_call.function.name

    if tool_name not in available_tools:
        raise ValueError(f"未知工具：{tool_name}")

    tool_function = available_tools[tool_name]
    result = tool_function(**arguments)
    if message.content is None:
        message.content = ""

    messages.append(message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        }
    )

    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        temperature=0,
    )
    print("第二次效用 Token: ", final_response.usage)

    print("模型最终回答：", final_response.choices[0].message.content)


if __name__ == "__main__":
    main()
