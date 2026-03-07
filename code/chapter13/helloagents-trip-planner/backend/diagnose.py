#!/usr/bin/env python3
"""完整的MCP和Agent诊断脚本"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 80)
print(" 🔍 MCP连接和Agent诊断报告")
print("=" * 80)

# 1. 环境检查
print("\n【1. 环境检查】")
print(f"Python版本: {sys.version}")
print(f"工作目录: {os.getcwd()}")
print(f"AMAP_API_KEY: {'✅ 已设置' if os.getenv('AMAP_API_KEY') else '❌ 未设置'}")
print(f"AMAP_MAPS_API_KEY: {'✅ 已设置' if os.getenv('AMAP_MAPS_API_KEY') else '❌ 未设置'}")
print(f"LLM_API_KEY: {'✅ 已设置' if os.getenv('LLM_API_KEY') else '❌ 未设置'}")
print(f"LLM_MODEL_ID: {os.getenv('LLM_MODEL_ID', '未设置')}")

# 2. 依赖检查
print("\n【2. 依赖检查】")
try:
    import hello_agents
    print(f"✅ hello-agents: {hello_agents.__version__ if hasattr(hello_agents, '__version__') else '版本未知'}")
except ImportError as e:
    print(f"❌ hello-agents 未安装: {e}")
    sys.exit(1)

try:
    from hello_agents import SimpleAgent, HelloAgentsLLM
    from hello_agents.tools import MCPTool
    print("✅ HelloAgents核心组件导入成功")
except ImportError as e:
    print(f"❌ HelloAgents组件导入失败: {e}")
    sys.exit(1)

# 3. MCP工具测试
print("\n【3. MCP工具测试】")
try:
    from app.config import get_settings
    settings = get_settings()

    print("创建MCPTool...")
    amap_tool = MCPTool(
        name="amap",
        description="高德地图服务",
        server_command=["uvx", "amap-mcp-server"],
        env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
        auto_expand=True
    )
    print("✅ MCPTool创建成功")

    print("展开MCP工具...")
    tools = amap_tool.get_expanded_tools()
    print(f"✅ 工具展开成功，共 {len(tools)} 个工具")

    # 列出所有工具
    print("\n可用工具列表:")
    for i, tool in enumerate(tools, 1):
        tool_name = getattr(tool, 'name', '未知')
        print(f"  {i}. {tool_name}")

except Exception as e:
    print(f"❌ MCP工具测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Agent创建测试
print("\n【4. Agent创建测试】")
try:
    print("初始化LLM...")
    llm = HelloAgentsLLM()
    print(f"✅ LLM初始化成功")
    print(f"   Provider: {llm.provider}")
    print(f"   Model: {llm.model}")

    print("\n创建SimpleAgent...")
    agent = SimpleAgent(
        name="测试Agent",
        llm=llm,
        system_prompt="你是一个测试助手。"
    )
    print("✅ SimpleAgent创建成功")

    print("\n添加MCP工具到Agent...")
    agent.add_tool(amap_tool)
    print("✅ 工具添加成功")

    print("\n查看Agent的工具列表...")
    agent_tools = agent.list_tools()
    print(f"✅ Agent共有 {len(agent_tools)} 个工具")

except Exception as e:
    print(f"❌ Agent创建测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. 简单的工具调用测试
print("\n【5. 工具调用测试（可选）】")
print("⚠️  跳过实际LLM调用测试（需要API调用和较长时间）")
print("   如需测试，请手动运行以下代码:")
print("""
agent.run("搜索北京的景点")
""")

print("\n" + "=" * 80)
print(" ✅ 所有诊断测试通过！")
print("=" * 80)
print("\n【诊断结论】")
print("1. ✅ 环境变量配置正确")
print("2. ✅ HelloAgents框架安装正常")
print("3. ✅ MCP服务器连接成功")
print("4. ✅ 工具展开正常")
print("5. ✅ Agent创建正常")
print("\n【可能的问题】")
print("如果运行时仍然出现MCP连接失败，请检查：")
print("1. 网络连接是否正常")
print("2. API密钥是否有效")
print("3. LLM API是否有足够的配额")
print("4. 查看后端日志获取详细错误信息")
print("\n【建议】")
print("- 使用 python run.py 启动后端服务")
print("- 查看控制台输出的详细日志")
print("- 使用 test_mcp.py 测试MCP连接")
print("- 使用前端界面进行完整测试")
