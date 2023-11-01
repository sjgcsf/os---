
from config import CONFIG
from lxml import html
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from pypinyin import lazy_pinyin
from urllib.parse import urljoin
from scrapers.scraper import Scraper
from config import UNIVERSITIES

class THUScraper(Scraper):

    def fetch_teachers(self, college_url, university_name, college_name):
        university_config = UNIVERSITIES[university_name]#对应学校信息列表
        college_config = None#指定学院的配置信息
        teacher_list = []
        # 查找指定学院的配置信息
        for college in university_config['colleges']:
            if college['name'] == college_name:
                college_config = college
                break
        if college_config is None:
            print(f"未找到{university_name}的{college_name}")
            return []
        print(f"开始搜索{university_name}的{college_name}：{college_url}")

        # 获取处理函数的名称
        processing_function_name = college_config.get('processing_function')
        # 检查是否为None或者空字符串
        if not processing_function_name:
            print(f"{college_name}没有指定处理函数")
            return []
        # 动态调用处理函数
        if hasattr(self, processing_function_name):
            processing_function = getattr(self, processing_function_name)
            if 'department' in college_config and college_config['department']:#搜索某一系的教师
                print(f"开始处理系：{college_config['department']}")
                teacher_list = processing_function(university_name, college_name, college_url, college_config,
                                                   teacher_list, college_config['department'])
                #如果用函数1，page_name接收系名，如果函数4/5，department_name接收系名，page_name充当“教授”页名
            else:                                                                                                #搜索某一学院的教师
                teacher_list=processing_function(university_name,college_name,college_url,college_config,teacher_list)
            #print(f"动态调用处理函数，teacher_list的长度: {len(teacher_list)}")

        else:
            print(f"未找到处理函数：{processing_function_name}")

        print(f"teacher_list的长度: {len(teacher_list)}")
        #print(teacher_list)
        return teacher_list

    def get_page_links(self, university_name):
        #无用函数
        all_list = []
        return all_list

    #1、xpath处理学院的函数
    def process_college_with_xpath(self,university_name,college_name,college_url,college_config,teacher_list,page_name=None,department_name=None):
        # 这里你可以用Selenium或其他方式获取学院的HTML，然后转换为lxml的tree对象
        college_tree = self.get_and_save_page(college_url, filename=college_name, save_flag=1)
        # 访问单一的学院配置
        structure = college_config['structures']
        teacher_elements_xpath =structure['teacher_elements_xpath']
        name_xpath = structure['name_xpath']
        url_xpath =structure['url_xpath']
        prefix_url = structure[ 'prefix_url']
        id_path_index= structure[ 'id_path_index']

        teacher_list=self.extract_teacher_info(structure,college_tree, university_name,
                                  college_name=college_name,
                                  teacher_list=teacher_list,
                                  teacher_elements_xpath=teacher_elements_xpath,
                                  name_xpath=name_xpath,
                                  url_xpath=url_xpath, prefix_url=prefix_url,
                                  id_path_index=id_path_index,
                                  page_name=page_name,#一般情况下式None
                                 department_name=department_name
                                  )
        #print("从建筑学院处理函数返回teacher_list，长度", len(teacher_list))
        return teacher_list

    # 2、xpath处理学院的函数(很多页)
    def process_pages_with_xpath(self,university_name,college_name,college_url,college_config,teacher_list):
        # 第一页
        college_tree = self.get_and_save_page(college_url, filename=college_name, save_flag=1)
        # 访问单一的学院配置
        structure = college_config['structures']
        teacher_elements_xpath =structure['teacher_elements_xpath']
        name_xpath = structure['name_xpath']
        url_xpath =structure['url_xpath']
        prefix_url = structure[ 'prefix_url']

        # 从配置文件中获取页面元素的XPath
        page_elements_xpath = structure['page_elements_xpath']
        page_url_xpath = structure['page_url_xpath']
        page_prefix_url = structure['page_prefix_url']
        page_name_xpath = structure.get('page_name_xpath')  # 使用 .get() 方法，如果键不存在则返回 None

        # 获取所有 页面元素
        page_elements = college_tree.xpath(page_elements_xpath)

        for page_element in page_elements:
            # 使用XPath从页面元素中获取页面名称和相对URL
            if page_name_xpath:  # 如果 page_name_xpath 存在
                page_name = page_element.xpath(page_name_xpath)[0].strip()
            else:
                page_name = None
            # 跳过 "其他教师" 和 "荣退教师" 页面
            if page_name and page_name in ['其他教授', '荣退教师']:
                continue

            # 检查URL是否以"http"开头，如果不是，则拼接前缀URL得到完整的页面URL
            page_url_elements = page_element.xpath(page_url_xpath)
            relative_url=page_url_elements[0].strip()
            if not relative_url.startswith("http"):
                page_url = urljoin(page_prefix_url, page_url_elements[0].strip())
            else:
                page_url = page_url_elements[0].strip()

            #print(f"Page Name: {page_name}")
            print(f"Page URL: {page_url}")

            page_tree = self.get_and_save_page(page_url, filename=college_name, save_flag=0)

            # page_name==类似于  水环境保护教研所
            teacher_list = self.extract_teacher_info(structure, page_tree, university_name,
                                                     college_name=college_name,
                                                     teacher_list=teacher_list,
                                                     teacher_elements_xpath=teacher_elements_xpath,
                                                     name_xpath=name_xpath,
                                                     url_xpath=url_xpath,
                                                     prefix_url=prefix_url,
                                                     page_name=page_name)

            # 返回最终的teacher_list
        return teacher_list

    # 3、chrome处理学院的函数(很多页)
    def process_pages_with_chrome(self,university_name,college_name,college_url,college_config,teacher_list,page_name=None,department_name=None):
        # 设置Chrome为无头模式
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # 启动Selenium浏览器
        driver_path = CONFIG['DRIVER_PATH']
        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        try:
            # 打开网页
            driver.get(college_url)
            # 访问单一的学院配置
            structure = college_config['structures']
            page_located = structure['page_located']
            teacher_elements_xpath = structure['teacher_elements_xpath']
            name_xpath = structure['name_xpath']
            url_xpath = structure['url_xpath']
            prefix_url = structure['prefix_url']
            # 等待页面加载
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, page_located)))
            # 尝试提取和打印条目数和页数
            college_tree = self.get_and_save_page(college_url, filename=page_name, save_flag=0)
            #通过xpath和tree
            if 'items_number_xpath' in structure and 'items_number_regex' in structure:
                items_elements = college_tree.xpath(structure['items_number_xpath'])
                if items_elements:

                    items_text = items_elements[0].text.strip()  # 获取文本内容
                    # print("items_text",items_text)
                    items_number = re.search(structure['items_number_regex'], items_text)
                    if items_number:
                        items_number = items_number.group()
                        print(f"总条数: {items_number}")
            # 获取页数
            page_number=100
            if 'page_number_xpath' in structure:
                page_text_elements = college_tree.xpath(structure['page_number_xpath'])
                if page_text_elements:
                    if 'page_number_regex' in structure:
                        print("使用正则表达式提取页数")
                        page_text = page_text_elements[0].text.strip()  # 获取文本内容
                        page_number = re.search(structure['page_number_regex'], page_text)
                        if page_number:
                            page_number = page_number.group()
                    else:
                        print("直接提取文本内容并转换为整数")
                        page_text = page_text_elements[0]  # 直接获取元素
                        page_number_text = page_text.strip()  # 获取元素的文本内容并去除前后空白
                        page_number = int(page_number_text)  # 将文本内容转换为整数
                    print(f"总页数: {page_number}")
            #动态获取，方便可靠
            if 'items_number_id' in structure:
                items_text_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, structure['items_number_id']))
                )
                items_number = items_text_element.text.strip()
                print(f"总条数: {items_number}")
            if 'page_number_id' in structure:
                page_number_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, structure['page_number_id']))
                )
                page_number = page_number_element.text.strip()
                print(f"总页数: {page_number}")

            # 处理第一页
            teacher_list=self.extract_teacher_info(structure, college_tree, university_name,
                                                     college_name=college_name,
                                                     teacher_list=teacher_list,
                                                     teacher_elements_xpath=teacher_elements_xpath,
                                                     name_xpath=name_xpath,
                                                     url_xpath=url_xpath,
                                                     prefix_url=prefix_url,
                                                     page_name=page_name,
                                                    department_name=department_name)
            print(f"页面1的条数：{len(teacher_list)}")
            # 处理剩下的页
            for page in range(2, int(page_number) + 1):
                try:
                    # 定位"下页"链接的元素
                    if 'next_page_link' in structure:  #xpath情况
                        next_page_links = driver.find_elements(By.XPATH, structure['next_page_link'])
                        if next_page_links:
                            next_page_link = next_page_links[0]  # 选择第一个
                            next_page_href = next_page_link.get_attribute("href")
                        else:
                            print("没有找到下一页链接，退出循环")
                            break
                    else:                                   #正常情况
                        next_page_link = driver.find_element(By.LINK_TEXT, "下页")
                       # 获取"下页"链接的href属性
                        next_page_href = next_page_link.get_attribute("href")

                    if next_page_href:
                        driver.get(next_page_href)
                        print("下一页链接",next_page_href)
                        # 等待新页面加载
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, page_located)))
                        # 提取信息
                        tree = html.fromstring(driver.page_source)
                        len_old=len(teacher_list)
                        teacher_list=self.extract_teacher_info(structure, tree, university_name,
                                                     college_name=college_name,
                                                     teacher_list=teacher_list,
                                                     teacher_elements_xpath=teacher_elements_xpath,
                                                     name_xpath=name_xpath,
                                                     url_xpath=url_xpath,
                                                     prefix_url=prefix_url,
                                                     page_name=page_name,
                                                     department_name = department_name)
                        len_new=len(teacher_list)
                        print(f"页面{page}的条数：{len_new-len_old}")
                    else:
                        print("没有找到下一页链接")
                        break
                except TimeoutException:
                    print(f"页面{page}没有加载成功")
                    break
        finally:
            # 关闭Selenium浏览器
            driver.quit()
        print(f"经过process_pages_with_chrome后的teacher_list的长度: {len(teacher_list)}")
        #print(teacher_list)
        return teacher_list

    # 4、xpath_chrome处理学院的函数(很多系，很多页)
    def process_xpath_chrome(self, university_name, college_name, college_url, college_config, teacher_list,department_name=None):
        # 访问单一的学院配置
        structure = college_config['structures']
        # 从配置文件中获取系的页面元素的XPath
        page_elements_xpath = structure['page_elements_xpath']
        page_url_xpath = structure['page_url_xpath']
        page_prefix_url = structure['page_prefix_url']
        page_name_xpath = structure.get('page_name_xpath')  # 使用 .get() 方法，如果键不存在则返回 None

        # 获取学院的主页面
        college_tree = self.get_and_save_page(college_url, filename=college_name, save_flag=0)
        # 获取所有系的页面元素
        page_elements = college_tree.xpath(page_elements_xpath)

        for page_element in page_elements:
            # 使用XPath从页面元素中获取系的名称和相对URL
            if page_name_xpath:  # 如果 department_name_xpath 存在
                page_name = page_element.xpath(page_name_xpath)[0].strip()
            else:
                page_name = None

            # 检查URL是否以"http"开头，如果不是，则拼接前缀URL得到完整的系页面URL
            page_url_elements = page_element.xpath(page_url_xpath)
            relative_url = page_url_elements[0].strip()
            if not relative_url.startswith("http"):
                relative_url = re.sub(r'\.\./', '', relative_url)  # 去除所有的 "../"
                #print(page_prefix_url,relative_url)
                page_url = page_prefix_url+relative_url
                #print(page_url)
            else:
                page_url = relative_url

            # 跳过 "其他教师" 和 "荣退教师" 页面
            if page_name and page_name in ['双聘教授、兼职教授','未来教师计划','机关','离退休教师','离退休职工']:
                     continue


            print(f"Department Name: {page_name}")
            print(f"Department URL: {page_url}")

            # 对每个系的页面调用 process_pages_with_chrome 函数处理分布在多个页面上的教师信息
            teacher_list = self.process_pages_with_chrome(university_name, college_name, page_url,
                                                          college_config, teacher_list,page_name=page_name,department_name=department_name)

        print("teacher_list")
        # 返回最终的teacher_list
        return teacher_list

    # 5、process_xpath_xpath处理学院的函数(很多系，很多页)  page_name:研究所，department_name:系
    def process_xpath_xpath(self, university_name, college_name, college_url, college_config, teacher_list,
                             department_name=None):
        # 访问单一的学院配置
        structure = college_config['structures']
        # 从配置文件中获取系的页面元素的XPath
        page_elements_xpath = structure['page_elements_xpath']
        page_url_xpath = structure['page_url_xpath']
        page_prefix_url = structure['page_prefix_url']
        page_name_xpath = structure.get('page_name_xpath')  # 使用 .get() 方法，如果键不存在则返回 None

        # 获取学院的主页面
        college_tree = self.get_and_save_page(college_url, filename=college_name, save_flag=1)
        # 获取所有系的页面元素
        page_elements = college_tree.xpath(page_elements_xpath)
        #print("page_elements",page_elements)

        for page_element in page_elements:
            # 使用XPath从页面元素中获取系的名称和相对URL
            if page_name_xpath:  # 如果 department_name_xpath 存在
                page_name = page_element.xpath(page_name_xpath)[0].strip()
            else:
                page_name = None

            # 检查URL是否以"http"开头，如果不是，则拼接前缀URL得到完整的系页面URL
            page_url_elements = page_element.xpath(page_url_xpath)
            relative_url = page_url_elements[0].strip()
            if not relative_url.startswith("http"):
                relative_url = re.sub(r'\.\./', '', relative_url)  # 去除所有的 "../"
                # print(page_prefix_url,relative_url)
                page_url = page_prefix_url + relative_url
                # print(page_url)
            else:
                page_url = relative_url

            # 跳过 "其他教师" 和 "荣退教师" 页面
            if page_name and page_name in ['离退休教师', '离退休职工','杰出人才','教辅、职员','博士后','退休教师','杰出访问教授']:
                continue

            print(f"Department Name: {page_name}")
            print(f"Department URL: {page_url}")

            # 对每个系的页面调用 process_pages_with_chrome 函数处理分布在多个页面上的教师信息
            teacher_list = self.process_college_with_xpath(university_name, college_name, page_url,
                                                          college_config, teacher_list, page_name=page_name,
                                                          department_name=department_name)
        #print("teacher_list")
        # 返回最终的teacher_list
        return teacher_list

    # xpath的extract_teacher_info
    def extract_teacher_info(self,structure, faculty_tree, university_name, college_name, teacher_list,
                                 teacher_elements_xpath, name_xpath='.//text()', url_xpath='".//@href"',
                                 prefix_url='',id_path_index=-1,page_name=None,department_name=None):
        """
        参数:
            学院树 (lxml.etree._ElementTree): 学院网页的解析HTML树
            教师信息列表 (list): 存储教师信息字典的列表。
            学院名称 (str): 学院名称。
            teacher_elements_xpath(str): 定位教师元素的XPath表达式。
            姓名XPath (str): 提取教师姓名的XPath表达式。
            URLXPath (str): 提取教师URL的XPath表达式。
            prefix_url:教师url的前缀
        返回:
            list: 包含提取的教师信息的更新后的教师信息列表。
        """
        teacher_elements = faculty_tree.xpath(teacher_elements_xpath)
        print("找到的可能是教师的元素数量:", len(teacher_elements),teacher_elements_xpath)
        for teacher_element in teacher_elements:
            teacher_name = teacher_element.xpath(name_xpath)
            teacher_name = ' '.join(teacher_name).strip()
            # print(teacher_name)
            teacher_name = teacher_name.replace('\xa0', ' ').strip()  # 后加的，为了去除NBSP
            if not teacher_name or teacher_name == '·':
                continue

            #teacher_url
            teacher_url=None
            if url_xpath:                                                                         #寻找url
                teacher_url_elements = teacher_element.xpath(url_xpath)
                #print("teacher_url_elements",teacher_url_elements)
                if teacher_url_elements:                                                 #该地址下找到教师链接了
                    if not teacher_url_elements[0].strip().startswith("http"):  # url的开头不对
                        # print(prefix_url, teacher_url_elements[0].strip())
                        teacher_url_element_cleaned = re.sub(r'\.\./', '',
                                                             teacher_url_elements[0].strip())  # 去除所有的 "../"
                        teacher_url = urljoin(prefix_url,
                                              teacher_url_element_cleaned)  # prefix_url不以斜杠结尾，urljoin会先去掉prefix_url路径的最后一部分，再附加relative_url
                        # print(teacher_url)
                    else:  # url开头正确
                        teacher_url = teacher_url_elements[0].strip()
                else:
                    print(f"没有链接的教师名字是：{teacher_name}")  # 输出没有链接的教师名字
                    teacher_url = None

            #teacher_id
            if  teacher_url==None:
                # 获取名字的拼音并将其与"****大学_"连接
                name_pinyin = ''.join(lazy_pinyin(teacher_name))
                teacher_id = university_name + "_" + name_pinyin
            else:
                # id_path_index : id是url最后一段,id_path_index=-1
                teacher_id_suffix=teacher_url.split('/')[id_path_index].split('.')[0]
                if not teacher_id_suffix :       #对应位置没有东西，向前看一位
                    teacher_id_suffix = teacher_url.split('/')[id_path_index-1].split('.')[0]
                elif teacher_id_suffix=='index':
                    teacher_id_suffix = teacher_url.split('/')[id_path_index - 2].split('.')[0]
                teacher_id = university_name + "_" + teacher_id_suffix

            # 检查college_name是否以'_'+数字结尾_____为了某些按系分的学院，比如'college_name': '机械工程学院_2'
            match = re.search(r'(_\d+)$', college_name)
            if match:
                # 如果匹配，去除'_'+数字
                college_name = college_name[:match.start()]

            teacher_info = {
                        "_id": teacher_id,
                        "name": teacher_name,
                        "college": college_name,
                        "url": teacher_url,
                        "detail_page":None
                }
            #print(teacher_info)

            # 提取额外信息
            if college_name == '建筑学院_0':
                # 设置部门信息
                teacher_info['department'] = '景观学系'
                teacher_info['mentor'] = None
                teacher_info['professional_title'] =None
                teacher_info['detail_page']=None
                # 提取行政职称
                administrative_positions = teacher_element.xpath('.//small//text()')
                teacher_info['administrative_positions'] = administrative_positions[
                    0] if administrative_positions else None
                # 处理教授和博士生导师信息
                positions_text = teacher_element.xpath('.//div[@class="leadership-position"]//text()')
                positions = positions_text[0].split('，') if positions_text else ''
                # 处理<div class="leadership-position">教授，博士生导师</div>
                for position in positions:
                    if '导师' in position:
                        teacher_info['mentor'] = position
                    else:
                        teacher_info['professional_title'] = position
                # 提取详细信息页的内容
                detail_page_elements = teacher_element.xpath('.//p//text()')
                teacher_info['detail_page'] = ' '.join(
                    [element.strip() for element in detail_page_elements if element.strip()])
            elif college_name == '公共管理学院':
                # 设置部门信息
                teacher_info['professional_title'] =None
                teacher_info['education_background'] = None
                teacher_info['telephone'] = None
                teacher_info['email'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('.//td[2]/div/text()')
                teacher_info['professional_title'] = professional_titles[0] if professional_titles else None
                # 提取学历背景
                education_backgrounds = teacher_element.xpath('.//td[3]/div/text()')
                teacher_info['education_background'] = education_backgrounds[0] if education_backgrounds else None
                # 提取电话号码
                telephones = teacher_element.xpath('.//td[4]//text()')
                teacher_info['telephone'] = telephones[0] if telephones else None
                # 提取电子邮件地址
                emails = teacher_element.xpath('.//td[5]//text()')
                teacher_info['email'] = emails[0]if emails else None  # 去掉'mailto:'前缀
            elif college_name == '环境学院':
                teacher_info['research_institute'] = page_name
            elif college_name == '经济管理学院':
                # 设置部门信息
                teacher_info['department'] =None
                teacher_info['professional_title'] = None
                teacher_info['telephone'] = None
                teacher_info['email'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('./div[@class="contenttitle"]/text()')
                teacher_info['professional_title'] = professional_titles[0] if professional_titles else None
                # 提取系
                departments = teacher_element.xpath('./div[@class="contenttitle"]/span/text()')
                teacher_info['department'] = departments[0] if departments else None
                # 提取电话号码
                telephones = teacher_element.xpath('./div[@class="contentdes"]/div[1]/p/text()')
                teacher_info['telephone'] = telephones[0] if telephones else None
                # 提取电子邮件地址
                emails = teacher_element.xpath('./div[@class="contentdes"]/div[2]/p/text()')
                teacher_info['email'] = emails[0]if emails else None
            elif college_name == '土木水利学院':
                # 设置部门信息
                teacher_info['professional_title'] = None
                teacher_info['telephone'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('./div[@class="teacher-p"]/a/p[1]/text()')
                teacher_info['professional_title'] = professional_titles[0] if professional_titles else None
                # 提取电话号码
                telephones = teacher_element.xpath('./div[@class="teacher-p"]/a/p[2]/text()')
                teacher_info['telephone'] = telephones[0] if telephones else None
            elif college_name == '马克思主义学院':
                teacher_info['professional_title'] = page_name
            elif college_name == '机械工程学院':
                if page_name=='基础工业训练中心':
                    teacher_info['research_institute'] = page_name
                else:
                    teacher_info['department'] = page_name
                    if page_name == '精密仪器系':
                        teacher_info['professional_title'] = None
                        # 提取教授职称
                        professional_titles = teacher_element.xpath('./p/text()')
                        teacher_info['professional_title'] = professional_titles[0] if professional_titles else None
                    elif page_name == '工业工程系':
                        teacher_info['professional_title'] = None
                        # 提取教授职称
                        professional_titles = teacher_element.xpath('./div[@class="desc"]/p/text()')
                        teacher_info['professional_title'] = professional_titles[0] if professional_titles else None
            elif college_name == '人文学院':
                if department_name=='中国语言文学系' or department_name=='哲学系':
                    teacher_info['department'] = department_name
                    teacher_info['professional_title'] = page_name
                else:
                    teacher_info['department'] = page_name
            elif college_name == '航天航空学院':
                if teacher_name=='|':
                    teacher_info['name'] = "徐曼琼"
                    name_pinyin = ''.join(lazy_pinyin(teacher_info['name']))
                    teacher_info['_id'] = university_name + "_" + name_pinyin
                    teacher_info['url'] = None
            elif college_name == '信息科学技术学院':
                if page_name=='网络科学与网络空间研究院':
                    teacher_info['research_institute'] = page_name
                elif department_name=='自动化系':#使用了函数5
                    teacher_info['department'] = department_name
                    teacher_info['research_institute'] = page_name
                    if   teacher_info['url']=="https://www.au.tsinghua.edu.cn/":
                        teacher_info['url']=None
                        name_pinyin = ''.join(lazy_pinyin(teacher_info['name']))
                        teacher_info['_id'] = university_name + "_" + name_pinyin
                else:
                    teacher_info['department'] = page_name
                    if page_name == '计算机科学与技术系':
                        teacher_info['professional_title'] = None
                        teacher_info['telephone'] = None
                        teacher_info['email'] = None
                        # 提取教授职称
                        professional_titles = teacher_element.xpath('./p[1]/text()')
                        teacher_info['professional_title'] = professional_titles[0] if professional_titles else None
                        # 提取电话号码
                        telephones = teacher_element.xpath('./p[2]/text()')
                        teacher_info['telephone'] = telephones[0] if telephones else None
                        # 提取电子邮件地址
                        emails = teacher_element.xpath('./p[3]/text()')
                        teacher_info['email'] = emails[0] if emails else None  # 去掉'mailto:'前缀
            elif college_name == '美术学院':
                # 设置部门信息
                teacher_info['professional_title'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('.//div[@class="zc"]/text()')
                teacher_info['professional_title'] = professional_titles[0] if professional_titles else None
            elif college_name == '电机工程与应用电子技术系':
                # 设置部门信息
                teacher_info['professional_title'] =None
                teacher_info['telephone'] = None
                teacher_info['office_address'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('./div[@class="con fr"]/p[2]/text()')
                teacher_info['professional_title'] = professional_titles[0].strip() if professional_titles else None
                # 提取电话号码
                telephones = teacher_element.xpath('./div[@class="con fr"]/p[3]/text()')
                teacher_info['telephone'] = telephones[0].strip() if telephones else None
                # 提取办公室地址
                office_addresses = teacher_element.xpath('./div[@class="con fr"]/p[4]/text()')
                teacher_info['office_address'] = office_addresses[0].strip() if office_addresses else None
            elif college_name == '化学工程系':
                # 设置部门信息
                teacher_info['professional_title'] =None
                teacher_info['telephone'] = None
                teacher_info['office_address'] = None
                teacher_info['email']=None
                # 提取教授职称
                professional_titles = teacher_element.xpath('./p/text()')
                teacher_info['professional_title'] = professional_titles[0].strip() if professional_titles else None
                # 提取电话号码
                telephones = teacher_element.xpath('./div/text()[1]')
                teacher_info['telephone'] = telephones[0].strip() if telephones else None
                # 提取办公室地址
                office_addresses = teacher_element.xpath('./div/text()[2]')
                teacher_info['office_address'] = office_addresses[0].strip() if office_addresses else None
                # 提取电子邮件地址
                emails = teacher_element.xpath('./div/a/text()')
                teacher_info['email'] = emails[0] if emails else None  # 去掉'mailto:'前缀
            elif college_name == '核能与新能源技术研究院':
                teacher_info['research_institute'] = teacher_info['college']
                teacher_info['college'] = None
                teacher_info['professional_title']=page_name
                if page_name=='两院院士':
                    prefix_url='https://www.inet.tsinghua.edu.cn/szdw/lyys/'
                    from urllib.parse import urlsplit
                    _, _, path, _, _ = urlsplit(teacher_info['url'])
                    last_part = path.split('/')[-1]
                    teacher_info['url'] = urljoin(prefix_url, last_part)
            elif college_name == '理学院':
                teacher_info['department'] =page_name
                if page_name == '数学科学系':
                    teacher_exists = False
                    for existing_teacher in teacher_list:
                        # 检查所有的字段是否相等
                        if all(existing_teacher[key] == teacher_info.get(key) for key in existing_teacher):
                            print("Teacher already exists:", existing_teacher)
                            teacher_exists = True
                            break
                    if teacher_exists:
                        continue
                elif page_name == '天文系':
                    # 设置部门信息
                    teacher_info['professional_title'] = None
                    teacher_info['email'] = None
                    teacher_info['office_address'] = None
                    teacher_info['research_field'] = None
                    # 提取教授职称
                    professional_titles = teacher_element.xpath('./td[@class="item-position"]/text()')
                    teacher_info['professional_title'] = professional_titles[0].strip() if professional_titles else None
                    # 提取电子邮件地址
                    emails = teacher_element.xpath('./td[@class="item-email hidden-phone hidden-xs"]/span/a/@href')
                    teacher_info['email'] = emails[0].strip() if emails else None  # 去掉'mailto:'前缀
                    # 提取办公室地址
                    office_addresses = teacher_element.xpath('./td[@class="item-street-address hidden-phone hidden-xs"]/text()')
                    teacher_info['office_address'] = office_addresses[0].strip() if office_addresses else None
                    # 提取研究方向
                    research_fields = teacher_element.xpath('./td[@class="item-extra_field_1"]/text()')
                    teacher_info['research_field'] = research_fields[0].strip() if research_fields else None
            elif college_name == '教育研究院':
                teacher_info['research_institute'] = page_name
            elif college_name == '全球创新学院':
                # 设置部门信息
                teacher_info['professional_title'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('./div[@class="title"]/text()')
                teacher_info['professional_title'] = professional_titles[0] if professional_titles else None
            elif college_name == '万科公共卫生与健康学院':
                teacher_info['name'] = "赵艾 助理教授"
                teacher_info['name'], teacher_info['professional_title'] = teacher_info['name'].split(' ', 1)  # 使用空格分割一次
            elif college_name == '交叉信息研究院':
                # 设置部门信息
                teacher_info['professional_title'] = None
                teacher_info['research_field'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('./div[2]/text()')
                teacher_info['professional_title'] = professional_titles[0].strip() if professional_titles else None
                # 提取学历背景
                research_fields = teacher_element.xpath('./div[3]/text()')
                teacher_info['research_field'] = research_fields[0].strip() if research_fields else None
            elif college_name == '语言教学中心':
                # 设置部门信息
                teacher_info['professional_title'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('./div[@class="content"]/text()')
                teacher_info['professional_title'] = professional_titles[0].strip() if professional_titles else None
            elif college_name == '出土文献研究与保护中心':
                # 设置部门信息
                teacher_info['professional_title'] = None
                # 提取教授职称
                professional_titles = teacher_element.xpath('.//div[@class="teacher-p"]/p/text()')
                teacher_info['professional_title'] = professional_titles[0].strip() if professional_titles else None



            #print(teacher_info)
            teacher_list.append(teacher_info)
        print("正常处理后的教师信息列表长度:", len(teacher_list))
        return teacher_list







    # 3—1、chrome处理学院的函数(很多页)
    def process_pages_with_all_chrome(self,university_name,college_name,college_url,college_config,teacher_list,page_name=None,department_name=None):
        # 设置Chrome为无头模式
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # 启动Selenium浏览器
        driver_path = CONFIG['DRIVER_PATH']
        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        try:
            # 打开网页
            driver.get(college_url)
            # 访问单一的学院配置
            structure = college_config['structures']
            page_located = structure['page_located']
            teacher_elements_xpath = structure['teacher_elements_xpath']
            name_xpath = structure['name_xpath']
            url_xpath = structure['url_xpath']
            prefix_url = structure['prefix_url']
            id_path_index = structure['id_path_index']
            # 等待页面加载
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, page_located)))
            # 尝试提取和打印条目数和页数
            #college_tree = self.get_and_save_page(college_url, filename=page_name, save_flag=1)

            #动态获取，方便可靠
            if 'items_number_id' in structure:
                items_text_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, structure['items_number_id']))
                )
                items_number = items_text_element.text.strip()
                print(f"总条数: {items_number}")
            if 'page_number_id' in structure:
                page_number_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, structure['page_number_id']))
                )
                page_number = page_number_element.text.strip()
                print(f"总页数: {page_number}")

            # 处理第一页
            teacher_list=self.extract_teacher_info_with_chrome(driver,university_name,
                                                     college_name=college_name,
                                                     teacher_list=teacher_list,
                                                     teacher_elements_xpath=teacher_elements_xpath,
                                                     name_xpath=name_xpath,
                                                     url_xpath=url_xpath,
                                                     prefix_url=prefix_url,
                                                     id_path_index=id_path_index,
                                                     page_name=page_name,
                                                    department_name=department_name)


            print(f"页面1的条数：{len(teacher_list)}")
            # 处理剩下的页
            for page in range(2, int(page_number) + 1):
                try:
                    # 定位到"下一页"的链接并点击
                    next_page_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, structure['next_page_id']))
                    )
                    next_page_button.click()
                    print("点击下一页")

                    # 等待新页面的某个元素加载完成
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, page_located)))
                    # 提取信息
                    #tree = html.fromstring(driver.page_source)
                    len_old=len(teacher_list)
                    teacher_list=self.extract_teacher_info_with_chrome(driver, university_name,
                                                     college_name=college_name,
                                                     teacher_list=teacher_list,
                                                     teacher_elements_xpath=teacher_elements_xpath,
                                                     name_xpath=name_xpath,
                                                     url_xpath=url_xpath,
                                                     prefix_url=prefix_url,
                                                     id_path_index=id_path_index,
                                                     page_name=page_name,
                                                     department_name = department_name)
                    len_new=len(teacher_list)
                    print(f"页面{page}的条数：{len_new-len_old}")

                except TimeoutException:
                    print(f"页面{page}没有加载成功")
                    break
        finally:
            # 关闭Selenium浏览器
            driver.quit()
        print(f"经过process_pages_with_chrome后的teacher_list的长度: {len(teacher_list)}")
        #print(teacher_list)
        return teacher_list

    def extract_teacher_info_with_chrome(self, driver, university_name, college_name, teacher_list,
                                         teacher_elements_xpath, name_xpath='.//text()', url_xpath='.//@href',
                                         prefix_url='', id_path_index=-1, page_name=None, department_name=None):
        """
        使用Selenium来提取教师信息。
        """
        # 等待教师元素加载
        teacher_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, teacher_elements_xpath))
        )
        print("找到的可能是教师的元素数量:", len(teacher_elements), teacher_elements_xpath)

        for teacher_element in teacher_elements:
            # 提取教师姓名
            teacher_name = teacher_element.find_element_by_xpath(name_xpath).text.strip()
            teacher_name = teacher_name.replace('\xa0', ' ').strip()
            if not teacher_name or teacher_name == '·':
                continue

            # 提取教师URL
            teacher_url = None
            if url_xpath:
                # 定位到<a>元素
                teacher_url_element = teacher_element.find_element_by_xpath(url_xpath)
                # 获取href属性的值
                teacher_url = teacher_url_element.get_attribute("href")
                if not teacher_url.startswith("http"):
                    teacher_url = urljoin(prefix_url, teacher_url)

            # 生成或提取教师ID
            if teacher_url is None:
                name_pinyin = ''.join(lazy_pinyin(teacher_name))
                teacher_id = university_name + "_" + name_pinyin
            else:
                teacher_id_suffix = teacher_url.split('/')[id_path_index].split('.')[0]
                teacher_id = university_name + "_" + teacher_id_suffix

            # 处理学院名称
            match = re.search(r'(_\d+)$', college_name)
            if match:
                college_name = college_name[:match.start()]

            teacher_info = {
                "_id": teacher_id,
                "name": teacher_name,
                "college": college_name,
                "url": teacher_url,
                "detail_page": None
            }

            # 提取额外信息
            if college_name == '理学院':
                teacher_info['department'] = page_name
                if page_name == '地球系统科学系':
                   # 设置部门信息
                   teacher_info['professional_title'] = None
                   teacher_info['research_field'] = None
                   # 提取教授职称
                   professional_title_element = teacher_element.find_element_by_xpath('./p')
                   teacher_info['professional_title'] = professional_title_element.text.strip() if professional_title_element else None
                   # 提取研究领域
                   research_field_element = teacher_element.find_elements_by_xpath('./p[3]')
                   teacher_info['research_field'] = research_field_element[0].text.strip() if research_field_element else None

            print(teacher_info)
            teacher_list.append(teacher_info)
        print("正常处理后的教师信息列表长度:", len(teacher_list))
        return teacher_list



