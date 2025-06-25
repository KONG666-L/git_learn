import requests
import json
from login import login
from config import BASE_URL, LANGUAGE_LIST, TRANSLATION_DIR, DEFAULT_HEADERS, LOGIN_CONFIG


def get_task_list(accept_language='',):
    """获取导出任务列表
    
    Args:
        accept_language (str): 接受的语言代码，如'zh-CN', 'en'等
    
    Returns:
        set: 包含(taskId, url)元组的集合，如果发生错误则返回None
    """
    # API端点URL
    url = f'{BASE_URL}/device-service/task/list'
    
    # 设置分页参数
    params = {
        'pageIndex': 1,  # 页码，从1开始
        'pageSize': 20   # 每页显示的记录数
    }
    
    # 设置请求头信息
    headers = {
        'accept': 'application/json, text/plain, */*',
        'Accept-Language': accept_language,
        'token':login(accept_language=accept_language),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
    }
    
    try:
        # 发送GET请求获取任务列表
        response = requests.get(url, params=params, headers=headers)
        
        # 解析JSON响应
        json_response = response.json()
        
        # 初始化返回数据集合
        return_data = set()
        
        # 从响应中提取任务信息
        if 'data' in json_response:
            data = json_response['data']
            if isinstance(data, list):
                # 遍历任务列表，提取taskId和下载URL
                for idx, task in enumerate(data, 1):
                    return_data.add(
                        (task['taskId'], task['url'])
                    )
        return return_data
    
    except requests.exceptions.RequestException as e:
        # 处理网络请求异常
        print(f"请求发生错误: {e}")
        return None
    except json.JSONDecodeError as e:
        # 处理JSON解析异常
        print(f"JSON解析错误: {e}")
        return None

if __name__ == "__main__":
    # 测试获取中文任务列表
    result = get_task_list(LANGUAGE_LIST[1])
    
    # 检查返回结果
    if result and result.get('ret') == 1:
        print("\n成功获取任务列表！")
        
        # 获取总记录数
        if 'data' in result and isinstance(result['data'], dict):
            total = result['data'].get('total', 0)
            print(f"总记录数: {total}")
    else:
        print("\n获取任务列表失败！")
        if result and 'msg' in result:
            print(f"错误信息: {result['msg']}")