import os
import requests
from urllib.parse import urlparse
from pathlib import Path
import json  # 导入json模块用于处理 JSON 数据
from login import login
from config import BASE_URL, LANGUAGE_LIST, TRANSLATION_DIR, DEFAULT_HEADERS, LOGIN_CONFIG

def get_image_url(index,time=10000):
    """
    获取图片URL
    
    Args:
        accept_language: 语言列表
    
    Returns:
        list: 图片URL列表
    """
    headers = {
        'Trace-id': 'a45f1a20-62d0-4905-bdbb-e03fa386e211',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    
        
    data = {
        "url": "https://saas.gpsnow.net/saas-pre/#/login",
        "username": "swd",
        "password": "a123456",
        "language_index": index  # 使用索引列表而不是.index方法
    }
    
    url = 'http://192.168.100.190:8000/autotest_translate'
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("data", {}).get("pics", [])
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {response.text}")
        return []
    except ValueError as e:
        print(f"解析JSON失败: {e}")
        return []

def download_image(url,accept_language):
    lang_dir = os.path.join(TRANSLATION_DIR, f"web-{accept_language}")
    os.makedirs(lang_dir, exist_ok=True)
    file_name = os.path.join(lang_dir, f"{url.split('/')[-1]}")
    url = "http://192.168.100.190:8000/get_pic?path=" + url
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()  # 检查请求是否成功
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"{accept_language}{file_name} 下载完成")
        

if __name__ == '__main__':
    for index,accept_language in enumerate(LANGUAGE_LIST):
        url_list = get_image_url(index,10000)
        if url_list:
            for url in url_list:
                download_image(url,accept_language)
        else:
            print(f"{accept_language} 没有图片")
        