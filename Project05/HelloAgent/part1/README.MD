最小版：仅调用天气 API + 规则推荐的北京旅行助手。  
用户任务："你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"

## 运行步骤
1) 安装依赖：`pip install -r requirements.txt`  
2) 运行：`python main.py`

## 流程说明
- 调用 Open-Meteo（无钥匙）获取北京实时天气。  
- 根据天气用规则选择一个合适景点和理由。  
- 直接在命令行打印结果。

## 项目结构
- main.py：主程序，调用工具并打印结果。  
- utils.py：天气 API 与规则推荐函数。  
- requirements.txt：依赖列表（仅 requests）。  
