import random
import requests
from faker import Faker
from sqlalchemy import desc

fake = Faker("zh_CN")

BASE_URL = "https://saas.whatsgps.com/saas-pre"

class Context:

    def __init__(self, username="duoruimi", password="duo123", lang="cn"):
        self._token = None
        self.username = username
        self.password = password
        self.lang = lang
    
    @property
    def headers(self):
        return {
            "Accept-Language": "cn",
        }
    
    @property
    def token(self):
        if self._token is None:
            self.login()
        return self._token
        
    def get_item(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise Exception(f"Item {key} not found")
        
    def set_item(self, key, value):
        setattr(self, key, value)
        
    def remove_item(self, key):
        delattr(self, key)
        
    def login(self):
        try:
            headers = self.headers
            headers['clientType'] = 'pc'
            response = requests.get(f"{BASE_URL}/user/login.do?name={self.username}&password={self.password}&lang={self.lang}", headers=headers)
            if response.ok:
                self._token = response.json()["data"]["token"]
            else:
                raise Exception(f"Login failed: {response.text}")
        except Exception as e:
            raise e

def send_request(context, url, method="GET", data=None, headers=None):
    if headers is None:
        headers = context.headers
    full_url = f"{BASE_URL}{url}"
    try:
        if method.upper() == "GET":
            response = requests.get(full_url, headers=headers, params=data)
        elif method.upper() == "POST":
            response = requests.post(full_url, headers=headers, data=data)
        else:
            raise Exception(f"Invalid method: {method}")
        return response
    except Exception as e:
        raise e
    
    
def run_single_test(context, api_class):
    api = api_class(context)
    api.setup()
    print(f"Running API: {api_class.desc} - {api.url}")
    for method in ["GET", "POST"]:
        for token_mode in ["HeaderToken", "BodyToken"]:
            headers = api.context.headers
            data = api.body
            if token_mode == "HeaderToken":
                headers["token"] = api.context.token
            else:
                data["token"] = api.context.token

            response = send_request(api.context, api.url, method, data, headers)
            output_str = f"    {method} {token_mode}: {response.status_code}"
            if (not response.ok) or (int(response.json().get("code")) != 200):
                output_str = f"{output_str} -- {response.headers.get('X-Trace-Id', 'N/A')} -- " + (response.text.replace('\n', '').replace('\r', ''))
            print(output_str)
            api.teardown(response)      

def run_all_test(context):
    # 查找出当前模块下所有BaseApi的子类
    for obj in globals().values():
        if isinstance(obj, type) and issubclass(obj, BaseApi) and obj != BaseApi:
            print("*" * 100)
            run_single_test(context, obj)

        
# 根据父id分页	user/getByParentIdPage.do
# 根据父id导出	user/exportByParentId.do
# 新增用户	user/add.do
# 更新用户信息	user/update.do
# 删除用户	user/del.do
# 用户修改密码	user/updatePsw.do
# 重置用户密码	user/resetPsw.do
# 获取当前用户上级代理商信息	user/getParentUserInfo.do
# 划拨用户	user/tranUser.do
# 批量划拨用户	user/tranUserBatch.do
# 根据用户id导出	car/getByUserIdExport.do
# 批量转移车辆	carManager/transferBatch.do
# 重置密码	car/resetPsw.do
# 分页查询	carFenceBound/queryPage.do
# 分页查询车辆绑定电子围栏	carFenceBound/queryCarFencePage.do
# 根据电子围栏查询车辆是否绑定	carFenceBound/getCarGroupAndStatus.do


class BaseApi:
    def __init__(self, context):
        self.context = context
        
    def setup(self):
        pass
        
    def teardown(self, response):
        # 清理操作，如果有需要的话
        pass

class GetByParentId(BaseApi):
    desc = "根据父级ID分页查询"
    url = "/user/getByParentIdPage.do"

    @property
    def body(self):
        return {
            "pageNo": 1,
            "parentId": self.context.get_item("parendId"),
            "rowCount": 20
        }



class ExportByParentId(BaseApi):
    desc = "根据父级ID导出"
    url = "/user/exportByParentId.do"

    @property
    def body(self):
        return {
            "parentId": self.context.get_item("parendId")
        }



class AddUser(BaseApi):
    desc = "添加用户"
    url = "/user/add.do"
    
    def __init__(self, context):
        super().__init__(context)
        self.index = 0

    @property
    def body(self):
        return {
            "address": fake.address(),
            "email": fake.email(),
            "linkMan": fake.name(),
            "linkPhone": fake.phone_number(),
            "name": fake.name(),
            "password": "a123456",
            "remark": "a123456",
            "userName": f"{fake.name()}{random.randint(100000, 999999)}",
            "userType": 1,
            "parentId": self.context.get_item("parendId"),
        }
        
    def teardown(self, response):
        if response.ok:
            self.index += 1
            self.context.set_item(f"user_id_{self.index}", response.json()["data"]["userId"])


class UpdateUser(BaseApi):
    desc = "更新用户"
    url = "/user/update.do"
    
    @property
    def body(self):
        return {
            "userId": 189046,
            "userType": 1,
            "name": "OpenAPI测试专用"
        }

class UpdatePsw(BaseApi):
    desc = "用户更新密码"
    url = "/user/updatePsw.do"
    
    @property
    def body(self):
        return {
            "newPassword": self.context.get_item("password"),
            "oldPassword": self.context.get_item("password"),
        }
    

class ResetPsw(BaseApi):
    desc = "重置用户密码"
    url = "/user/resetPsw.do"
    
    def setup(self):
        print("  Running setup")
        run_single_test(self.context, AddUser)
    
    @property
    def body(self):
        return {
            "id": self.context.get_item("user_id_1"),
            "password": "a123456",
            "type": 1,
        }
    
class DeleteUser(BaseApi):
    desc= "删除用户"
    url = "/user/del.do"
    
    def __init__(self, context):
        super().__init__(context)
        self.index = 0
        
    def setup(self):
        print("  Running setup")
        run_single_test(self.context, AddUser)

    @property
    def body(self):
        self.index += 1
        return {
            "id": self.context.get_item(f"user_id_{self.index}"),
        }
    
    def teardown(self, response):
        if response.ok:
            self.context.remove_item(f"user_id_{self.index}")
            
class GetParentUserInfo(BaseApi):
    desc = "获取父级用户信息"
    url = "/user/getParentUserInfo.do"
    
    @property
    def body(self):
        return {}
    
    
class TranUser(BaseApi):
    desc = "转移用户"
    url = "/user/tranUser.do"
    
    def __init__(self, context):
        super().__init__(context)
        self.index = 0
    
    def setup(self):
        print("  Running setup")
        run_single_test(self.context, AddUser)
    
    @property
    def body(self):
        self.index += 1
        return {
            "targetUserId": self.context.get_item("tran_target_user_id"),
            "parentId": self.context.get_item(f"user_id_{self.index}"),
        }
    
class TranUserBatch(BaseApi):
    desc = "批量转移用户"
    url = "/user/tranUserBatch.do"
    
    def setup(self):
        print("  Running setup")
        run_single_test(self.context, AddUser)
    
    @property
    def body(self):
        return {
            "targetUserId": self.context.get_item("tran_target_user_id"),
            "userIds": ",".join([self.context.get_item(f"user_id_{i}") for i in range(1, 4)])
        }
        
class GetByUserIdExport(BaseApi):
    desc = "根据用户ID导出"
    url = "/car/getByUserIdExport.do"
    
    @property
    def body(self):
        return {
            "recursion": False,
            "userId": self.context.get_item("parendId"),
        }
        
class TransferBatch(BaseApi):
    desc = "批量转移车辆"
    url = "/carManager/transferBatch.do"
    
    @property
    def body(self):
        return {
            "carIds": ",".join([self.context.get_item(f"car_id_{i}") for i in range(1, 3)]),
            "targetUserId": self.context.get_item("tran_target_user_id"),
        }

class ResetCarPsw(BaseApi):
    desc = "重置车辆密码"
    url = "/car/resetPsw.do"
    
    @property
    def body(self):
        return {
            "carId": self.context.get_item("car_id_1"),
            "password": "a123456",
        }
        
class QueryPage(BaseApi):
    desc = "分页查询"
    url = "/carFenceBound/queryPage.do"
    
    @property
    def body(self):
        return {
            "bound": False,
            "carFenceId": self.context.get_item("car_fence_id_1"),
            "carId": self.context.get_item("car_id_1"),
            "pageNo": 1,
            "rowCount": 20,
            "userId": self.context.get_item("parendId"),
        }
        
class QueryCarFencePage(BaseApi):
    desc = "分页查询车辆绑定电子围栏"
    url = "/carFenceBound/queryCarFencePage.do"
    
    @property
    def body(self):
        return {
            "carId": self.context.get_item("car_id_1"),
            "mapType": 1,
            "pageNo": 1,
            "rowCount": 20,
        }

class GetCarGroupAndStatus(BaseApi):
    desc = "根据电子围栏查询车辆是否绑定"
    url = "/carFenceBound/getCarGroupAndStatus.do"
    
    @property
    def body(self):
        return {
            "carFenceId": self.context.get_item("car_fence_id_1"),
            "groupId": self.context.get_item("car_group_id_1"),
            "mapType": 1,
            "orderType": 1,
            "targetUserId": self.context.get_item("tran_target_user_id"),
        }

        
if __name__ == "__main__":
    context = Context()
    context.parendId = 189046
    context.tran_target_user_id = 1935646366822825984
    context.car_id_1 = 2466003
    context.car_fence_id_1 = 251068
    context.car_group_id_1 = 0

    run_all_test(context)
    
    
    
    
    
