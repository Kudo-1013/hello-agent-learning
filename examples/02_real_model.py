"""调用真实模型：本节只验证模型对话，下一节再加入工具。"""

import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()

    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL_ID")
    if not api_key or not base_url or not model:
        raise RuntimeError("请先在项目根目录的 .env 中填写模型配置")

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个简洁、准确的助手。"},
            {"role": "user", "content": "只回答计算结果：12 乘 8 等于多少？"},
        ],
        temperature=0,
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
