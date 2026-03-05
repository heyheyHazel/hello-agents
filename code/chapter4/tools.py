from dotenv import load_dotenv
# 加载 .env 文件中的环境变量
load_dotenv()

import os
from serpapi import SerpApiClient
from typing import Dict, Any


# 定义search函数：设置参数、API -> 交给client搜索结果 -> 解析结果
def search(query: str) -> str:
    """
    一个基于SerpApi的实战网页搜索引擎工具。
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    """
    print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "错误：SERPAPI_API_KEY 未在 .env 文件中配置。"

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",  # 国家代码
            "hl": "zh-cn", # 语言代码
        }
        
        client = SerpApiClient(params)
        results = client.get_dict()
        
        # 智能解析：优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)
        
        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误: {e}"
    
from typing import Dict, Any


# 集成管理各个工具 包括注册、查看等
class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        向工具箱中注册一个新工具。
        param:
            name: 工具名称（满足唯一性）
            description: 工具描述，大模型根据工具描述决定是否要调用工具
            func: 工具函数，如上面的search函数，定义这个工具所做的事情
        """
        if name in self.tools:
            print(f"警告：工具 '{name}' 已存在，将被覆盖。")
        
        # 增加一个工具 tools是嵌套字典 name是key 后面的字典是value
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")


    def getTool(self, name: str) -> callable:
        """
        根据名称获取一个工具的执行函数。
        param:
            name: 工具名称
        """
        # get(name, {}): 返回name, 如果没有就返回空{}
        # .get("func"): 只返回name下的func值
        return self.tools.get(name, {}).get("func")


    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        # 返回格式是 name: description
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])




# 使用示例
if __name__ == '__main__':
    # 初始化实例
    toolExecutor = ToolExecutor()

    # 注册search工具
    search_description = '一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。'
    toolExecutor.registerTool('Search', search_description, search)

    # 打印可以用的工具
    print('\n --- available tools ---')
    print(toolExecutor.getAvailableTools()) # 返回所有工具的名称和描述

    # 调用search工具
    print("\n --- 执行action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = 'Search'
    tool_input = '英伟达最新的GPU型号是什么'
    tool_function = toolExecutor.getTool(tool_name) # 返回的是search工具的function
    # 当function存在时
    if tool_function:
        observation = tool_function(tool_input) # 调用api得到输出(observation)
        print(observation)
    else:
        print(f"错误：未找到名为 '{tool_name}' 的工具。")