#!/usr/bin/env python3
"""最终系统验证"""

import requests
import json

print("=" * 70)
print("🎯 最终系统验证")
print("=" * 70)

# 1. 后端健康检查
print("\n【1/3】后端健康检查")
try:
    response = requests.get("http://localhost:8000/", timeout=5)
    print(f"✅ 状态: {response.json()['status']}")
    print(f"   版本: {response.json()['version']}")
except Exception as e:
    print(f"❌ 错误: {e}")
    exit(1)

# 2. 环境变量检查
print("\n【2/3】环境变量检查")
from dotenv import load_dotenv
import os
load_dotenv()

env_vars = {
    "AMAP_API_KEY": os.getenv("AMAP_API_KEY"),
    "AMAP_MAPS_API_KEY": os.getenv("AMAP_MAPS_API_KEY"),
    "LLM_API_KEY": os.getenv("LLM_API_KEY"),
    "LLM_MODEL_ID": os.getenv("LLM_MODEL_ID")
}

for key, value in env_vars.items():
    status = "✅" if value else "❌"
    display_value = value[:15] + "..." if value and len(value) > 15 else value
    print(f"{status} {key}: {display_value}")

# 3. MCP工具检查
print("\n【3/3】MCP工具检查")
try:
    from hello_agents.tools import MCPTool
    from app.config import get_settings

    settings = get_settings()
    tool = MCPTool(
        name="amap",
        server_command=["uvx", "amap-mcp-server"],
        env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
        auto_expand=True
    )

    tools = tool.get_expanded_tools()
    print(f"✅ MCP连接成功")
    print(f"   可用工具: {len(tools)}个")

    # 显示部分工具名称
    tool_names = [getattr(t, 'name', 'unknown') for t in tools[:5]]
    print(f"   示例: {', '.join(tool_names)}...")

except Exception as e:
    print(f"❌ MCP错误: {e}")
    exit(1)

print("\n" + "=" * 70)
print("✅ 所有验证通过！系统就绪")
print("=" * 70)
print("\n📝 下一步:")
print("   1. 前端: cd ../frontend && npm run dev")
print("   2. 访问: http://localhost:5173")
print("   3. API文档: http://localhost:8000/docs")
print("\n⏱️  提示: 首次生成旅行计划可能需要30-90秒")
