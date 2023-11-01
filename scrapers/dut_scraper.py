from config import CONFIG
from lxml import html
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from scrapers.scraper import Scraper

class DUTScraper(Scraper):
    def get_page_links(self, university_name):
        # 生成26个链接
        base_url = 'http://faculty.dlut.edu.cn/pylby.jsp?urltype=tsites.PinYinTeacherList&wbtreeid=1001&py={}&lang=zh_CN'
        all_list = []
        letters = CONFIG['LETTERS']
        for letter in letters:
            url = base_url.format(letter.lower())  # 因为URL中的字母是小写的
            all_list.append(url)
        return all_list

    def fetch_teachers(self, url, university_name):
        # 设置Chrome为无头模式
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # 启动Selenium浏览器
        driver_path = CONFIG['DRIVER_PATH']
        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        # driver = webdriver.Chrome()
        try:
            # 打开网页
            driver.get(url)
            # 等待页面加载
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='fanye']")))

            # 获取条数和页数
            num_items_element = driver.find_element(By.XPATH, "//*[@id='fanye']")
            num_items_text = num_items_element.text
            # 使用正则表达式提取数字
            match = re.search(r'共(\d+)条.*?(\d+)/(\d+)', num_items_text)
            if match:
                num_items = int(match.group(1))
                num_pages = int(match.group(3))
            else:
                num_items = 0
                num_pages = 0
            #print(f"Number of items: {num_items}")
            #print(f"Number of pages: {num_pages}")

            teacher_list = []
            # 处理第一页
            tree = html.fromstring(driver.page_source)
            teacher_list.extend(self.extract_teacher_info(tree, university_name, page=1))
            # 处理剩下的页
            for page in range(2, int(num_pages) + 1):
                try:
                    # 定位"下页"链接的元素
                    next_page_link = driver.find_element(By.LINK_TEXT, "下页")
                    # 获取"下页"链接的href属性
                    next_page_href = next_page_link.get_attribute("href")

                    if next_page_href:
                        driver.get(next_page_href)
                        # print(next_page_href)
                        # 等待新页面加载
                        xpath_expression = "/html/body/table/tbody/tr/td"
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_expression)))
                        # 提取信息
                        tree = html.fromstring(driver.page_source)
                        teacher_list.extend(self.extract_teacher_info(tree, university_name, page=page))
                    else:
                        print("没有找到下一页链接")
                        break
                except TimeoutException:
                    print(f"页面{page}没有加载成功")
                    break
        finally:
            # 关闭Selenium浏览器
            driver.quit()

        print(f"teacher_list的长度: {len(teacher_list)}")
        # print(teacher_list)
        return teacher_list

    def extract_teacher_info(self, tree, university_name, page):
        new_teachers = []  # 创建一个新列表来存储新提取的教师信息
        # 定位所有教师的li元素
        teacher_elements = tree.xpath("//div[@class='subJCRCmainLis']/ul/li")
        for element in teacher_elements:
            # teacher_id = element.xpath("@id")[0]
            name = element.xpath(".//span/h2/a/text()")[0]
            # 提取学院名
            college_elements = element.xpath(".//span/p[1]/text()")
            college = college_elements[0].strip() if college_elements else None

            professional_title_elements = element.xpath(".//span/p[2]/text()")
            professional_title = professional_title_elements[0].strip() if professional_title_elements else None

            teacher_url = element.xpath(".//a/@href")[0]
            # print(teacher_url)
            try:
                teacher_id = university_name + "_" + teacher_url.split('/')[3]
            except IndexError:
                print(f"Error: 'teacher_url.split('/')[3]' list index out of range for name: {name}")
            '''
            # 如果teacher_id为“system”，则将URL设置为null
            if teacher_url.split('/')[3] == "system":
                teacher_url = None
                # 获取名字的拼音并将其与"****大学_"连接
                #name_pinyin = ''.join(lazy_pinyin(name))
                #teacher_id = university_name + "_" + name_pinyin
'''
            teacher_info = {
                "_id": teacher_id,
                "name": name,
                "college": college,
                "professional_title": professional_title,
                "url": teacher_url
            }
            new_teachers.append(teacher_info)  # 将新教师信息添加到新列表中

        print(f"第{page}页长度: {len(new_teachers)}")
        return new_teachers  # 返回新提取的教师信息
