#!/usr/bin/env python3
"""API测试脚本"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

print("=" * 60)
print("API功能测试")
print("=" * 60)

# 测试1: 健康检查
print("\n1. 健康检查:")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试2: 生成旅行计划（简单测试）
print("\n2. 测试旅行计划API:")
try:
    payload = {
        "city": "北京",
        "start_date": "2025-03-10",
        "end_date": "2025-03-12",
        "travel_days": 3,
        "transportation": "地铁",
        "accommodation": "经济型酒店",
        "preferences": ["历史文化"],
        "free_text_input": "简单测试"
    }

    print(f"   发送请求: {json.dumps(payload, ensure_ascii=False)}")
    response = requests.post(
        f"{BASE_URL}/api/trip/plan",
        json=payload,
        timeout=60
    )

    print(f"   状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ 旅行计划生成成功")
        print(f"   城市: {result.get('city')}")
        print(f"   天数: {len(result.get('days', []))}")
    else:
        print(f"   ❌ 请求失败")
        print(f"   响应: {response.text[:500]}")

except requests.exceptions.Timeout:
    print(f"   ⚠️  请求超时（60秒）")
except Exception as e:
    print(f"   ❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
