# 第四课：多轮 Agent 循环

运行 `examples/04_react_loop.py`。问题需要先执行 `add`，再根据结果执行 `multiply`，最后回答。

```powershell
.\.venv\Scripts\python.exe .\examples\04_react_loop.py
```

重点观察每轮中三种可能：模型给出工具调用、Python 执行工具、模型不再调用工具并返回最终文本。

`for step in range(max_steps)` 控制最大模型请求轮数。工具名称、JSON 参数或函数参数错误时，程序把错误作为 Observation 回传，模型可以在后续轮次调整。达到上限仍没有回答时程序终止。

不要发送 `.env`；只发送终端中的每轮输出。
