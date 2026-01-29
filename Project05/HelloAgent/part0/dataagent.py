# main_agent.py
import sys
import os

# 1. 获取当前脚本的绝对路径 (D:\...\part0)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 向前回退 3 层，找到根目录 MYAGENT
# part0 -> HelloAgent -> Project05 -> MYAGENT
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))

# 3. 把根目录加到 Python 的搜索路径中
if project_root not in sys.path:
    sys.path.append(project_root)



from llmconfig.llm_wrapper import FreeLLMAdapter
import datetime
import re

# 1. 定义工具：一个真正的 Python 计算器
def calculate(expression):
    try:
        # 这是一个危险函数，仅做演示用
        return str(eval(expression))
    except Exception as exc:
        return f"计算出错: {exc}"


def fallback_calculate_from_question(question: str) -> str:
    """粗略把中文问题转成表达式做兜底。"""
    expr = question
    replacements = {
        "乘以": "*",
        "乘": "*",
        "加上": "+",
        "加": "+",
        "减去": "-",
        "减": "-",
        "除以": "/",
        "除": "/",
    }
    for k, v in replacements.items():
        expr = expr.replace(k, f" {v} ")
    expr = re.sub(r"[等于是多少\?？]", " ", expr)
    expr = re.sub(r"[^0-9+\-*/(). ]", " ", expr)
    expr = " ".join(expr.split())
    if not expr:
        return ""
    try:
        return str(eval(expr))
    except Exception as exc:
        return f"无法从问题解析表达式: {exc}"
# 2. 定义核心 Agent 逻辑
def run_agent(question):
    llm = FreeLLMAdapter()
    
 # 2. 修改 Prompt：这次我们看模型能不能自己判断出来“我算不准，我要用计算器”
    prompt_template = f"""
你是一个计算助手。只允许使用以下工具：
- calculator: 传入数学表达式字符串，返回计算结果，例如 calculator("3+5")。

规则（务必严格遵守）：
- 只能输出 Action: calculator 或 Action: None；禁止使用 shell/其他工具/JSON。
- 如果用工具，先输出 Thought 和 Action，等待 Observation 后再给 Final Answer。
- 如果不需要工具，直接 Final Answer 给结果（Action: None）。

回答模板：
Question: <用户问题>
Thought: <思考>
Action: <工具名或 None>
Observation: <工具结果>
Final Answer: <答案>

Question: {question}
"""
    
    print(f"--- ❓ 问题: {question} ---")
    response_1 = llm.chat(prompt_template)
    print(f"🤖 模型第一轮想法:\n{response_1}")

    # 提取 Action 行
    action_match = re.search(r"Action:\s*([^\n]+)", response_1, re.IGNORECASE)
    action_raw = action_match.group(1).strip() if action_match else ""
    action_norm = action_raw.lower()

    # 安全兜底：过滤掉非法工具（如 shell）
    if action_norm.startswith("shell") or action_norm.startswith("python"):
        print("⚠️ 拒绝非法工具调用，改用本地计算兜底。")
        fallback = fallback_calculate_from_question(question)
        print(f"✅ 兜底结果: {fallback}")
        return

    if action_norm.startswith("calculator"):
        # 尝试抓 expression
        expr_match = re.search(r'calculator\("(.*?)"\)', response_1)
        expression = expr_match.group(1) if expr_match else question
        print(f"--- 🧮 正在调用 Python 计算: {expression} ---")
        tool_result = calculate(expression)
        # 把结果喂回去
        next_prompt = f"{prompt_template}\n{response_1}\nObservation: {tool_result}\nFinal Answer:"
        response_2 = llm.chat(next_prompt)
        print(f"✅ 最终结果: {response_2}")
    else:
        # 无动作或未识别，尝试直接用兜底算法
        fallback = fallback_calculate_from_question(question)
        if fallback:
            print(f"✅ 模型未用工具，使用兜底计算: {fallback}")
        else:
            print("💡 模型决定直接回答或未提供可解析的 Action。")

if __name__ == "__main__":
    # 测试 1: 简单的，看它是否直接回答
    run_agent("1加1等于几？")
    print("\n" + "="*30 + "\n")
    # 测试 2: 复杂的，看它是否求助工具 (如果它硬算，答案通常是错的)
    run_agent("39824 乘以 12 加上 400 等于多少？")