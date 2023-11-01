import re
from collections import defaultdict
from pypinyin import lazy_pinyin
from urllib.parse import urljoin
from scrapers.scraper import Scraper
from config import UNIVERSITIES

class NWAFUScraper(Scraper):
    def fetch_teachers(self, college_url, university_name, college_name):
        university_config = UNIVERSITIES[university_name]#对应学校信息列表
        college_config = None#指定学院的配置信息
        # 查找指定学院的配置信息
        for college in university_config['colleges']:
            if college['name'] == college_name:
                college_config = college
                break
        if college_config is None:
            print(f"未找到{university_name}的{college_name}")
            return []
        print(f"开始搜索{university_name}的{college_name}：{college_url}")

        # 这里你可以用Selenium或其他方式获取学院的HTML，然后转换为lxml的tree对象
        college_tree = self.get_and_save_page(college_url,filename=college_name,save_flag=0)
        # 访问单一的学院配置
        structure = college['structures']

        teacher_list = []

        # page_count代表了这个学院有几个页面要爬取
        page_count = structure['page_count']

        # 遍历每个页面
        for i in range(page_count):
            print(f"开始搜索第{i + 1}页的教师信息", end=' ')
            # 根据当前页面选择相应的xpath或前缀
            teacher_elements_xpath = structure['teacher_elements_xpath'][i] if isinstance(
                 structure['teacher_elements_xpath'], list) else structure['teacher_elements_xpath']
            name_xpath = structure['name_xpath'][i] if isinstance(structure['name_xpath'], list) else structure[
                 'name_xpath']
            url_xpath = structure['url_xpath'][i] if isinstance(structure['url_xpath'], list) else structure[
                   'url_xpath']
            prefix_url = structure['prefix_url'][i] if isinstance(structure['prefix_url'], list) else structure[
                  'prefix_url']
            id_path_index = structure['id_path_index'][i] if isinstance(structure['id_path_index'], list) else \
                  structure['id_path_index']

            # 如果是第一个页面，则使用原始的college_tree, 否则需要根据title_page_xpaths获取新的页面tree
            if i > 0 and structure['title_page_xpaths'] and structure['prefix_title_page']:
                #print(structure['title_page_xpaths'][i - 1])
                partial_url = college_tree.xpath(structure['title_page_xpaths'][i - 1])[0]
                #print(partial_url)
                if not partial_url:
                    print(f"错误：在处理 {university_name} 的 {college_name} 时，未能找到第 {i+1} 页的 URL。请检查 XPath 表达式和网页内容。")
                    continue  # 跳过这次循环的其余部分，继续下一次循环

                prefix_title_page=structure['prefix_title_page'][i - 1]if isinstance(structure['prefix_title_page'], list) else structure[
                  'prefix_title_page']
                # 使用college_url获取新的页面内容并转换为lxml的tree对象
                #print(prefix_title_page,partial_url)
                college_url = urljoin(prefix_title_page, partial_url)  # 构建绝对链接,注意/szdw/会被删去一个
                college_tree = self.get_and_save_page(college_url)
            print(f"搜索第{i + 1}页:{college_url}")

            if college_name=='语言文化学院' and  i <2:#考虑其他情况
                html_content = self.get_and_save_page(college_url,return_html_content=1)
                self.extract_teacher_info_regex(html_content=html_content,
                                          teacher_list=teacher_list,
                                          college_name=college_name,
                                          prefix_url=prefix_url)
            elif college_name == '水建学院' and i < 1:  # 考虑其他情况
                self.extract_teacher_info_ergodic(college_tree, university_name, teacher_list, college_name,
                                                 teacher_elements_xpath)
            else:
                # 调用extract_teacher_info方法
                #print(teacher_elements_xpath)
                self.extract_teacher_info(college_tree, university_name,
                                          college_name=college_name,
                                          teacher_list=teacher_list,
                                          teacher_elements_xpath=teacher_elements_xpath,
                                          name_xpath=name_xpath,
                                          url_xpath=url_xpath, prefix_url=prefix_url,
                                          id_path_index=id_path_index)
        # 补丁，补充，修改错误的id和url
        techer_list_patch=self.patch(college_name, university_name, teacher_list)
        print(f"teacher_list的长度: {len(techer_list_patch)}")
        return techer_list_patch

    # xpath
    def extract_teacher_info(self, faculty_tree, university_name, college_name, teacher_list,
                                 teacher_elements_xpath, name_xpath='.//text()', url_xpath='".//@href"',
                                 prefix_url='', id_path_index=-1):
        """
        参数:
            学院树 (lxml.etree._ElementTree): 学院网页的解析HTML树
            教师信息列表 (list): 存储教师信息字典的列表。
            学院名称 (str): 学院名称。
            teacher_elements_xpath(str): 定位教师元素的XPath表达式。
            姓名XPath (str): 提取教师姓名的XPath表达式。
            URLXPath (str): 提取教师URL的XPath表达式。
            prefix_url:教师url的前缀
            id_path_index(int):id在url中的位置，注意！倒数
        返回:
            list: 包含提取的教师信息的更新后的教师信息列表。
        """

        teacher_elements = faculty_tree.xpath(teacher_elements_xpath)
        # print("找到的可能是教师的元素数量:", len(teacher_elements))
        for teacher_element in teacher_elements:
            teacher_name = teacher_element.xpath(name_xpath)
            teacher_name = ' '.join(teacher_name).strip()
            # print(teacher_name)
            teacher_name = teacher_name.replace('\xa0', ' ').strip()  # 后加的，为了去除NBSP
            if not teacher_name:
                continue
            teacher_url_elements = teacher_element.xpath(url_xpath)
            #print(teacher_name,teacher_url_elements)

            if not teacher_url_elements:
                print(f"没有找到链接的教师名字是：{teacher_name}")  # 输出没有链接的教师名字
                teacher_url = None
                # 获取名字的拼音并将其与"****大学_"连接
                name_pinyin = ''.join(lazy_pinyin(teacher_name))
                teacher_id = university_name + "_" + name_pinyin
            else:
                # teacher_url
                if not teacher_url_elements[0].strip().startswith("http"):  # url的开头不对
                    if url_xpath=="./@onclick":                                            #对植保学院
                        # 使用正则表达式从JavaScript代码中提取URL
                        match = re.search(r"'(.*?)'", teacher_url_elements[0])
                        if match:
                            teacher_url = prefix_url + match.group(1)
                    else:
                        teacher_url = prefix_url + teacher_url_elements[0].strip()#对大部分学院
                else:                                                                                       #url开头正确
                    teacher_url = teacher_url_elements[0].strip()

                # id_path_index : id是url最后一段,id_path_index=-1
                teacher_id_suffix=teacher_url.split('/')[id_path_index].split('.')[0]

                if teacher_id_suffix=='href':#href是错误id
                    teacher_id_suffix = ''.join(lazy_pinyin(teacher_name))

                teacher_id = university_name + "_" + teacher_id_suffix

            teacher_info = {
                        "_id": teacher_id,
                        "name": teacher_name,
                        "college": college_name,
                        "url": teacher_url
                }
            teacher_list.append(teacher_info)
        print("正常处理后的教师信息列表长度:", len(teacher_list))
        return teacher_list

    # 正则表达式的方法
    def extract_teacher_info_regex(self, html_content, teacher_list, college_name, prefix_url):
            """
            参数:
                html_content (str): 学院网页的HTML内容。
                teacher_list (list): 存储教师信息字典的列表。
                college_name (str): 学院名称。
                prefix_url (str): 教师详情页面的基础URL。

            返回:
                list: 包含提取的教师信息的更新后的教师信息列表。
            """

            # D定义正则表达式以匹配 HTML 内容中的教师信息结构
            import re
            # print(college_name, prefix_url)
            #print(html_content)
            teacher_info_pattern = re.compile(r'<A href="(.*?)">(.*?)</A>')

            # 查找所有出现的教师信息
            found_teacher_info = teacher_info_pattern.findall(html_content)
            #print(found_teacher_info)
            # 过滤掉名称为空的条目
            found_teacher_info = [(url, name) for url, name in found_teacher_info if name.strip()]

            # 填充teacher_info_list
            for url, name in found_teacher_info:
                teacher_info = {
                    "_id": "西北农林科技大学_"+url.split('/')[-1].split('.')[0],
                    "name": name,
                    "Faculty": college_name,
                    "url": prefix_url + url
                }
                teacher_list.append(teacher_info)

            print("正常处理后的教师信息列表长度:", len(teacher_list))
            return teacher_list

    #XPATH+遍历每个教师元素的 <a> 标签
    def extract_teacher_info_ergodic(self, faculty_tree, university_name, teacher_list, college_name, teacher_elements_xpath):
        teacher_elements = faculty_tree.xpath(teacher_elements_xpath)
        #print("找到的可能是教师的元素数量:", len(teacher_elements))
        for teacher_element in teacher_elements:
            # 新增：遍历每个教师元素的子元素（这里假设是 <a> 标签）
            for a_tag in teacher_element.xpath('.//a'):
                # 从 <a> 标签中提取教师姓名和 URL
                 teacher_name = a_tag.xpath('./span/text()')[0] if a_tag.xpath('./span/text()') else None
                 teacher_url = a_tag.xpath('./@href')[0] if a_tag.xpath('./@href') else None

                 if teacher_name:
                    teacher_name = teacher_name.strip()
                    teacher_url = teacher_url.strip()
                    teacher_id = university_name + "_" + teacher_url.split('/')[-1].split('.')[0]
                    if not teacher_url:
                        print(f"没有找到链接的教师名字是：{teacher_name}")  # 输出没有链接的教师名字
                        teacher_url = None
                        # 获取名字的拼音并将其与"****大学_"连接
                        name_pinyin = ''.join(lazy_pinyin(teacher_name))
                        teacher_id = university_name + "_" + name_pinyin

                    teacher_info = {
                            "_id": teacher_id,
                            "name": teacher_name,
                            "college": college_name,
                            "url": teacher_url
                        }
                    teacher_list.append(teacher_info)
        print("正常处理后的教师信息列表长度:", len(teacher_list))
        return teacher_list

    def get_page_links(self, university_name):
        #无用函数
        all_list = []
        return all_list

    # 补丁，补充，修改错误的id和url
    def patch(self, college_name, university_name, teacher_list):
        def update_teacher_info(updates):
            for teacher_info in teacher_list:
                if teacher_info["name"] in updates:
                    new_id = university_name + '_' + updates[teacher_info["name"]]["_id"]
                    new_url = updates[teacher_info["name"]]["url"]
                    print(
                        f"更新 {teacher_info['name']} 的 _id 从 {teacher_info['_id']} 到 {new_id} 和 url 从 {teacher_info['url']} 到 {new_url}")
                    teacher_info["_id"] = new_id
                    teacher_info["url"] = new_url

        if college_name == '化学与药学院':
            updates = {
                "郑怀基": {"_id": university_name+"21456B", "url": "https://hxyyxy.nwafu.edu.cn/szdwB/21456B.htm"},
                "高锦明": {"_id": university_name+"21445B", "url": "https://hxyyxy.nwafu.edu.cn/szdwB/21445B.htm"},
                "曹   蔚": {"_id": university_name+"21447B", "url": "https://hxyyxy.nwafu.edu.cn/szdwB/21447B.htm"}
            }
            update_teacher_info(updates)
        elif college_name == '资环学院':
            updates = {
                "王延平": {"_id": university_name+"318796", "url": "https://zhxy.nwsuaf.edu.cn/szdw/kjdw/318796.htm"}
            }
            update_teacher_info(updates)
        elif college_name == '林学院':
            updates = {
                "马艳萍": {"_id": university_name+"be5047a12e294915912704b73094c5a3", "url": "https://cf.nwafu.edu.cn/szdw/zjrc2/be5047a12e294915912704b73094c5a3.htm"},
                "李冬兵": {"_id": university_name + "375884", "url":"https://rcb.nwsuaf.edu.cn/rcdw/375884.htm"}
            }
            update_teacher_info(updates)
        elif college_name == '语言文化学院':
            # 特殊处理， "马海燕"和 "後藤美智子"的htm页面相同，後藤美智子没有详情页
            for teacher_info in teacher_list:
                if teacher_info.get('name') == '後藤美智子':
                    teacher_info['_id'] = university_name +'431307'
                    teacher_info['url'] = None
                    break

        elif college_name == '人文学院':
            merged_dict = defaultdict(dict)
            for info in teacher_list:
                teacher_id = info['_id']
                if 'name' not in merged_dict[teacher_id]:
                    merged_dict[teacher_id] = info
                else:
                    merged_dict[teacher_id]['name'] += info['name']
            teacher_list = list(merged_dict.values())

        return teacher_list

