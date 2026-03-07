#!/usr/bin/env python3
"""MCP连接测试脚本"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("MCP连接诊断测试")
print("=" * 60)

# 1. 检查环境变量
print("\n1. 检查环境变量:")
print(f"   AMAP_API_KEY: {os.getenv('AMAP_API_KEY', '未设置')}")
print(f"   AMAP_MAPS_API_KEY: {os.getenv('AMAP_MAPS_API_KEY', '未设置')}")

# 2. 测试配置加载
print("\n2. 测试配置加载:")
try:
    from app.config import get_settings
    settings = get_settings()
    print(f"   ✅ 配置加载成功")
    print(f"   amap_api_key: {settings.amap_api_key}")
except Exception as e:
    print(f"   ❌ 配置加载失败: {e}")
    sys.exit(1)

# 3. 测试MCPTool导入
print("\n3. 测试MCPTool导入:")
try:
    from hello_agents.tools import MCPTool
    print(f"   ✅ MCPTool导入成功")
except Exception as e:
    print(f"   ❌ MCPTool导入失败: {e}")
    sys.exit(1)

# 4. 测试MCPTool创建
print("\n4. 测试MCPTool创建:")
try:
    amap_tool = MCPTool(
        name="amap",
        description="高德地图服务",
        server_command=["uvx", "amap-mcp-server"],
        env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
        auto_expand=True
    )
    print(f"   ✅ MCPTool创建成功")
    print(f"   工具名称: {amap_tool.name}")
    print(f"   服务器命令: {amap_tool.server_command}")
    print(f"   环境变量: {amap_tool.env}")
except Exception as e:
    print(f"   ❌ MCPTool创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. 测试MCP连接
print("\n5. 测试MCP工具展开 (这会实际启动MCP服务器):")
try:
    # 尝试展开工具
    tools = amap_tool.get_expanded_tools()
    print(f"   ✅ MCP工具展开成功")
    print(f"   可用工具数量: {len(tools)}")
    if tools:
        print(f"   前5个工具:")
        for i, tool in enumerate(tools[:5], 1):
            tool_name = getattr(tool, 'name', '未知')
            tool_desc = getattr(tool, 'description', '')[:50]
            print(f"     {i}. {tool_name} - {tool_desc}...")
except Exception as e:
    print(f"   ❌ MCP工具展开失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ 所有测试通过！MCP连接正常")
print("=" * 60)
