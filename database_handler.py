import time
import pymongo
from pymongo import MongoClient
import requests
from config import CONFIG

class DatabaseHandler:
    def __init__(self, host='localhost', port=27017, database_name='faculty_db', collection_name='teacher_info'):
        self.client = MongoClient(host, port)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def save_teacher_info_to_mongo(self, teacher_info_list):
        headers = { "User-Agent": CONFIG['USER_AGENT']}
        for teacher_info in teacher_info_list:
            #time.sleep(1)  # 在请求之间加入一个延迟,以避免被目标网站屏蔽。
            teacher_info['detail_page'] = teacher_info.get('detail_page', None)
            #在 teacher_info 字典中获取 'detail_page' 的值，如果 'detail_page' 不存在，就返回 None 并设置 teacher_info['detail_page'] 为 None”。
            if teacher_info['url']:                             #当url有内容才会触发下载详情页
                response = None
                # 尝试获取网页的二进制数据并保存到 teacher_info 字典中
                try:
                    proxies = {}
                    response = requests.get(teacher_info['url'], timeout=10, headers=headers, proxies=proxies)
                    response.raise_for_status()  # 这将抛出一个HTTPError，如果HTTP请求返回了不成功的状态码
                except requests.RequestException as e:
                    print(f"下载网页二进制报错 {teacher_info['url']}: {e}")

                # 检查响应是否成功
                if response and response.status_code == 200:
                    teacher_info['detail_page'] = response.content
                else:
                    print(f"下载网页二进制失败{teacher_info['url']}")  # 下载网页失败
                    teacher_info['detail_page'] = None

            # 尝试将教师信息插入 MongoDB
            original_id = teacher_info['_id']
            counter = 1
            while True:
                try:
                    self.collection.insert_one(teacher_info)
                    break  # 如果成功插入，则跳出循环
                except pymongo.errors.DuplicateKeyError:
                    # id相同的情况，加后缀_counter
                    print(f"_id重复，修改{teacher_info['_id']}为", end=' '.encode('utf-8').decode('utf-8'))
                    teacher_info['_id'] = f"{original_id}_{counter}"
                    print(teacher_info['_id'])
                    counter += 1
            else:
                print("{teacher_info['_id']}的url：None")


    def save_teacher_html_from_mongo(self, n):
        # 查询并获取第n个教师信息的二进制HTML数据
        teacher_info = self.collection.find().skip(n - 1).limit(1).next()
        if not teacher_info:
            print("数据库中未找到教师信息!")
            return
        if 'detail_page' in teacher_info:
            binary_data = teacher_info['detail_page']
            # 使用该数据在本地创建一个HTML文件
            filename = "teacher_detail" + teacher_info['_id'] + ".html"
            with open(filename, 'wb') as file:
                file.write(binary_data)
            print(f"HTML saved as {filename}.")
        else:
            print("找不到教师的二进制详细信息页面!")

    def redownload_and_update_missing_pages(self):
        """重新下载缺失的detail_page并更新到MongoDB"""
        print("重新下载缺失的detail_page并更新到MongoDB")
        '''
        name="何震"
        documents_with_short_detail_page = self.collection.find({"name": "何震"})
        
        count = 0
        found = False
        for doc in self.collection.find():
            count += 1
            if doc.get("name") == name:
                print(f"名为{name}的文档在集合中的次序为: {count}")
                found = True
                break
        if not found:
            print(f"没有找到名为{name}的文档。")
            '''
        # 获取detail_page=None or False的文档
        documents_without_page = list(self.collection.find({"$or": [{'detail_page': None}, {"detail_page": {"$exists": False}}, {"detail_page": {"$size": 0}}]}))
        # 获取字段长度较短（例如小于200）的文档
        #documents_without_page = list(self.collection.find({"detail_page": {"$type": "binData", "$lt": 200}}))
        print("缺失文档的数量：",list(documents_without_page))
        headers = {"User-Agent": CONFIG['USER_AGENT']}
        for doc in documents_without_page:
            url = doc.get('url')
            if not url:
                print(f"重新下载：{doc.get('_id')}没有url")
                continue

            try:
                proxies = {}
                response = requests.get(url, timeout=20, headers=headers, proxies=proxies)
                if response.status_code == 200:
                    self.collection.update_one({'_id': doc['_id']}, {'$set': {'detail_page': response.content}})
                    print(f"下载成功{doc['_id']}:{doc['name']}")
                else:
                    print(f"下载网页二进制失败 {url}: {response.status_code}")
            except requests.RequestException as e:
                print(f"下载网页二进制报错 {url}: {e}")

