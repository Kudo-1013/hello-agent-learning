"""离线模拟，不调用真实模型；用于观察程序如何执行工具。"""


def add(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b


def mock_model(messages: list[dict]) -> dict:
    if messages[-1]["role"] == "tool":
        return {"answer": f"计算结果是 {messages[-1]['content']}"}
    return {"tool": "multiply", "arguments": {"a": 12, "b": 8}}


def run_demo(max_steps: int = 3) -> str:
    messages = [{"role": "user", "content": "帮我计算 12 乘 8"}]
    tools = {
        "add": add,
        "multiply": multiply
        }
    for step in range(max_steps):
        response = mock_model(messages)
        print(f"第 {step + 1} 轮模拟输出：{response}")
        if "answer" in response:
            return response["answer"]
        tool_name = response["tool"]
        if tool_name not in tools:
            raise ValueError(f"未知工具：{tool_name}")
        result = tools[tool_name](**response["arguments"])
        print(f"程序执行工具，得到：{result}")
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "tool", "content": result})
    raise RuntimeError("达到循环上限，尚未得到最终回答")


if __name__ == "__main__":
    print("注意：离线模拟，不是真实模型调用。")
    answer = run_demo()
    assert answer == "计算结果是 96"
    print(answer)

