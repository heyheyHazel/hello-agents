#!/usr/bin/env python3
"""快速测试MCP工具调用"""

import sys
import time
from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import MCPTool
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("快速MCP工具调用测试")
print("=" * 60)

# 初始化LLM
print("\n1. 初始化LLM...")
llm = HelloAgentsLLM()
print(f"   ✅ LLM: {llm.provider}/{llm.model}")

# 创建MCP工具
print("\n2. 创建MCP工具...")
from app.config import get_settings
settings = get_settings()

amap_tool = MCPTool(
    name="amap",
    description="高德地图服务",
    server_command=["uvx", "amap-mcp-server"],
    env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
    auto_expand=True
)
print("   ✅ MCP工具创建成功")

# 创建Agent
print("\n3. 创建Agent...")
agent = SimpleAgent(
    name="测试助手",
    llm=llm,
    system_prompt="你是一个测试助手。请使用工具回答问题。"
)
agent.add_tool(amap_tool)
print("   ✅ Agent创建成功")

# 测试简单查询
print("\n4. 测试工具调用（查询北京天气）...")
print("   这可能需要10-30秒...")
start_time = time.time()

try:
    response = agent.run("请查询北京的天气", max_tool_iterations=1)
    elapsed = time.time() - start_time

    print(f"\n   ✅ 调用成功！耗时: {elapsed:.1f}秒")
    print(f"\n响应内容:")
    print("-" * 60)
    print(response[:500])
    if len(response) > 500:
        print("...")
    print("-" * 60)

except Exception as e:
    elapsed = time.time() - start_time
    print(f"\n   ❌ 调用失败（{elapsed:.1f}秒）: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ 测试完成！MCP工具调用正常工作")
print("=" * 60)
