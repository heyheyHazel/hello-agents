# MCP连接问题诊断报告

## 📋 问题概述

项目运行时显示连接MCP失败。

## 🔍 诊断过程

### 1. 环境变量检查

**发现的问题：**
- `.env` 文件第36行：`AMAP_MAPS_API_KEY = 859d19a94623ed25910d4a82df350c9f`
- 等号两边有空格，导致环境变量无法正确读取

**解决方案：**
```bash
# 错误格式
AMAP_MAPS_API_KEY = 859d19a94623ed25910d4a82df350c9f

# 正确格式
AMAP_MAPS_API_KEY=859d19a94623ed25910d4a82df350c9f
```

✅ **已修复**

### 2. MCP服务器连接测试

**测试结果：**
- ✅ uvx命令可用
- ✅ amap-mcp-server可以运行
- ✅ MCPTool可以成功创建
- ✅ 工具展开成功（16个工具）

**可用工具列表：**
1. amap_maps_regeocode - 逆地理编码
2. amap_maps_geo - 地理编码
3. amap_maps_ip_location - IP定位
4. amap_maps_weather - 天气查询
5. amap_maps_bicycling_by_address - 骑行路线规划
6. amap_maps_bicycling_by_coordinates - 骑行路线规划(坐标)
7. amap_maps_direction_walking_by_address - 步行路线规划
8. amap_maps_direction_walking_by_coordinates - 步行路线规划(坐标)
9. amap_maps_direction_driving_by_address - 驾车路线规划
10. amap_maps_direction_driving_by_coordinates - 驾车路线规划(坐标)
11. amap_maps_direction_transit_integrated_by_address - 公交路线规划
12. amap_maps_direction_transit_integrated_by_coordinates - 公交路线规划(坐标)
13. amap_maps_distance - 距离测量
14. amap_maps_text_search - 文字搜索
15. amap_maps_around_search - 周边搜索
16. amap_maps_search_detail - 详情查询

### 3. Agent配置检查

**检查结果：**
- ✅ HelloAgentsLLM初始化成功
  - Provider: deepseek
  - Model: deepseek-chat
- ✅ SimpleAgent创建成功
- ✅ MCP工具添加成功

## 🐛 发现的问题

### 问题1: 环境变量格式错误 ✅ 已修复

**位置：** `backend/.env` 第36行

**问题：** 等号两边有空格

**影响：** MCP服务器启动时找不到`AMAP_MAPS_API_KEY`环境变量

**错误信息：**
```
ValueError: AMAP_MAPS_API_KEY environment variable is required
```

### 问题2: API请求超时 ⚠️ 需要注意

**现象：** 旅行规划API请求超过60秒未响应

**可能原因：**
1. LLM响应时间较长
2. MCP工具调用耗时
3. 多个Agent顺序执行

**建议：**
- 增加前端请求超时时间到120-180秒
- 优化Agent提示词，减少不必要的工具调用
- 考虑添加进度反馈机制

## ✅ 验证测试

运行诊断脚本验证修复：

```bash
cd backend
python diagnose.py
```

**预期结果：**
```
✅ 所有诊断测试通过！
1. ✅ 环境变量配置正确
2. ✅ HelloAgents框架安装正常
3. ✅ MCP服务器连接成功
4. ✅ 工具展开正常
5. ✅ Agent创建正常
```

## 📝 使用建议

### 1. 启动后端服务

```bash
cd backend
python run.py
```

**预期输出：**
```
✅ LLM服务初始化成功
   提供商: deepseek
   模型: deepseek-chat
🔄 开始初始化多智能体旅行规划系统...
  - 创建共享MCP工具...
  - 创建景点搜索Agent...
  - 创建天气查询Agent...
  - 创建酒店推荐Agent...
  - 创建行程规划Agent...
✅ 多智能体系统初始化成功
```

### 2. 测试API

访问 `http://localhost:8000/docs` 查看API文档

### 3. 查看日志

后端日志会显示：
- MCP连接状态
- 工具调用过程
- Agent执行步骤

## 🔧 故障排查

如果仍然出现MCP连接失败：

### 1. 检查网络连接

```bash
# 测试高德地图API
curl "https://restapi.amap.com/v3/config/district?key=YOUR_API_KEY"
```

### 2. 验证API密钥

```bash
# 在backend目录运行
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('AMAP_MAPS_API_KEY:', os.getenv('AMAP_MAPS_API_KEY'))
"
```

### 3. 测试MCP服务器

```bash
# 手动测试amap-mcp-server
export AMAP_MAPS_API_KEY=your_api_key
uvx amap-mcp-server
```

### 4. 查看详细错误

```bash
# 启动后端时查看完整日志
cd backend
python run.py 2>&1 | tee server.log
```

## 📊 系统要求

- Python 3.10+
- Node.js 16+
- uvx (uv package manager)
- 有效的API密钥：
  - 高德地图API Key
  - LLM API Key (DeepSeek/OpenAI等)

## 🎯 总结

**主要问题：** 环境变量格式错误导致MCP服务器无法获取API密钥

**解决方案：** 修复`.env`文件中的环境变量格式

**验证状态：** ✅ MCP连接正常，工具展开成功

**后续建议：**
1. 监控API请求耗时
2. 优化Agent执行效率
3. 添加错误处理和重试机制
4. 考虑添加缓存机制减少API调用

---

**诊断时间：** 2025-03-06
**诊断工具：** diagnose.py, test_mcp.py
