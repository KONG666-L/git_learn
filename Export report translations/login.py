import requests
from config import BASE_URL, LOGIN_CONFIG, DEFAULT_HEADERS

def login(username=LOGIN_CONFIG['username'], 
          password=LOGIN_CONFIG['password'], 
          timezone_second=LOGIN_CONFIG['timezone_second'], 
          accept_language='cn'):
    """
    调用登录接口获取token
    
    Args:
        username (str): 用户名，默认为配置文件中的用户名
        password (str): 密码，默认为配置文件中的密码
        timezone_second (int): 时区秒数，默认为配置文件中的时区设置
        accept_language (str): 接受的语言，默认为'cn'
    
    Returns:
        str: token字符串，登录失败返回None
    """
    url = f'{BASE_URL}/user-service/user/login'
    
    # 设置请求头信息
    headers = {
        'accept-language': accept_language,              # 接受的语言
        'user-agent': DEFAULT_HEADERS['User-Agent']     # 用户代理
    }
    
    # 设置请求参数
    data = {
        'name': username,                # 用户名
        'password': password,            # 密码
        'timeZoneSecond': timezone_second,  # 时区秒数
        'lang': accept_language          # 语言设置
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # 如果响应状态码不是200，将引发异常
        
        # 解析响应结果
        result = response.json()
        if response.status_code == 200:  # 请求成功
            return result.get('data', {}).get('token')  # 返回token
        else:
            print(f"登录失败: {result.get('msg')}")  # 打印错误信息
            return None
            
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"请求发生错误: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"错误响应状态码: {e.response.status_code}")
            print(f"错误详情: {e.response.text}")
        return None

if __name__ == "__main__":
    # 测试登录功能
    token = login()
    if token:
        print("登录成功，获取到的token:")
        print(token)
    else:
        print("登录失败") 