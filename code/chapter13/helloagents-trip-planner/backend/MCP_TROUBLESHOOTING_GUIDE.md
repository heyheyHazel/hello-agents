# MCP连接问题排查总结

## ✅ 问题已解决

### 根本原因
`.env` 文件第36行的环境变量格式错误（等号两边有空格），导致MCP服务器无法读取API密钥。

### 修复内容
```diff
- AMAP_MAPS_API_KEY = 859d19a94623ed25910d4a82df350c9f
+ AMAP_MAPS_API_KEY=859d19a94623ed25910d4a82df350c9f
```

## 🧪 验证测试

### 1. 环境变量测试 ✅
```bash
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('AMAP_MAPS_API_KEY:', os.getenv('AMAP_MAPS_API_KEY'))"
```
**结果：** API密钥正确读取

### 2. MCP连接测试 ✅
```bash
python test_mcp.py
```
**结果：**
- MCPTool创建成功
- 工具展开成功（16个工具）
- 连接正常

### 3. 诊断测试 ✅
```bash
python diagnose.py
```
**结果：**
```
✅ 所有诊断测试通过！
1. ✅ 环境变量配置正确
2. ✅ HelloAgents框架安装正常
3. ✅ MCP服务器连接成功
4. ✅ 工具展开正常
5. ✅ Agent创建正常
```

### 4. 后端服务测试 ✅
```bash
python run.py
```
**结果：**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
应用名称: HelloAgents智能旅行助手
✅ 配置验证通过
```

## 📊 可用的MCP工具

成功连接到高德地图MCP服务器后，以下16个工具可用：

1. **地理编码**
   - `amap_maps_regeocode` - 逆地理编码（坐标→地址）
   - `amap_maps_geo` - 地理编码（地址→坐标）
   - `amap_maps_ip_location` - IP定位

2. **天气查询**
   - `amap_maps_weather` - 天气查询

3. **路线规划**
   - `amap_maps_direction_walking_by_address` - 步行路线（地址）
   - `amap_maps_direction_walking_by_coordinates` - 步行路线（坐标）
   - `amap_maps_direction_driving_by_address` - 驾车路线（地址）
   - `amap_maps_direction_driving_by_coordinates` - 驾车路线（坐标）
   - `amap_maps_direction_transit_integrated_by_address` - 公交路线（地址）
   - `amap_maps_direction_transit_integrated_by_coordinates` - 公交路线（坐标）
   - `amap_maps_bicycling_by_address` - 骑行路线（地址）
   - `amap_maps_bicycling_by_coordinates` - 骑行路线（坐标）

4. **搜索服务**
   - `amap_maps_text_search` - 关键词搜索
   - `amap_maps_around_search` - 周边搜索
   - `amap_maps_search_detail` - 详情查询

5. **其他**
   - `amap_maps_distance` - 距离测量

## 🚀 启动项目

### 后端
```bash
cd backend
python run.py
```

访问 http://localhost:8000/docs 查看API文档

### 前端
```bash
cd frontend
npm run dev
```

访问 http://localhost:5173 使用应用

## 📝 注意事项

### 1. 首次请求可能较慢
由于需要：
- 初始化LLM连接
- 启动MCP服务器
- 执行多个Agent协作
- 调用多个工具

首次生成旅行计划可能需要30-90秒，请耐心等待。

### 2. API密钥安全
- 不要将`.env`文件提交到Git
- 定期更换API密钥
- 监控API使用量

### 3. 性能优化建议
- 增加前端请求超时时间（建议120秒）
- 考虑添加进度反馈
- 可以实现结果缓存

## 🔧 故障排查

如果仍然遇到问题：

### 1. 检查服务状态
```bash
# 检查后端是否运行
curl http://localhost:8000/

# 检查进程
ps aux | grep uvicorn
```

### 2. 查看详细日志
```bash
# 启动时保存日志
python run.py 2>&1 | tee server.log

# 实时查看日志
tail -f server.log
```

### 3. 测试MCP连接
```bash
# 运行诊断
python diagnose.py

# 测试MCP
python test_mcp.py

# 快速工具测试
python quick_test.py
```

### 4. 验证API密钥
```bash
# 测试高德地图API
curl "https://restapi.amap.com/v3/config/district?key=YOUR_KEY&keywords=北京"
```

## 📚 相关文件

- `diagnose.py` - 完整诊断脚本
- `test_mcp.py` - MCP连接测试
- `quick_test.py` - 快速工具调用测试
- `MCP_DIAGNOSIS_REPORT.md` - 详细诊断报告

## ✨ 总结

**问题：** MCP连接失败

**原因：** 环境变量格式错误

**解决：** 修复`.env`文件格式

**状态：** ✅ 已解决，所有功能正常

---

**最后更新：** 2025-03-06
**测试环境：** Python 3.12, macOS
