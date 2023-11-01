from config import CONFIG
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from scrapers.scraper import Scraper

class CSUScraper(Scraper):
    def get_page_links(self, university_name):
        # 生成26个链接
        base_url = 'https://faculty.csu.edu.cn/pinyinjiansuo.jsp?urltype=tsites.PinYinTeacherList&wbtreeid=1001&py={}&lang=zh_CN'
        all_list = []
        letters = CONFIG['LETTERS']
        for letter in letters:
            url = base_url.format(letter.lower())  # 因为URL中的字母是小写的
            all_list.append(url)
        return all_list

    def fetch_teachers(self, url,university_name):
        # 启动Selenium浏览器
        driver_path = CONFIG['DRIVER_PATH']
        driver = webdriver.Chrome(executable_path=driver_path)
        # driver = webdriver.Chrome()
        try:
            # 打开网页
            driver.get(url)
            # 等待页面加载
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/div/div[1]/div[1]/p/a")))
            # 获取条数和页数元素
            pagination_element = driver.find_element(By.XPATH,
                                                     "/html/body/div/div/div[3]/div/div/div/div/div[2]/div/div[2]/a/table/tbody/tr/td/table/tbody/tr/td[1]")

            # 从元素文本中提取条数和页数
            pagination_text = pagination_element.text
            matches = re.findall(r'共(\d+)条.*?(\d+)/(\d+)', pagination_text)
            if matches:
                num_items = int(matches[0][0])
                num_pages = int(matches[0][2])
                print(f"条数: {num_items}")
                print(f"页数: {num_pages}")

            teacher_list = []
            # 处理第一页
            tree = html.fromstring(driver.page_source)
            teacher_list.extend(self.extract_teacher_info(tree,university_name,page=1))
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
                        xpath_expression = "/html/body/div/div/div[4]/div/div[1]/div[1]/p/a"
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_expression)))
                        # 提取信息
                        tree = html.fromstring(driver.page_source)
                        teacher_list.extend(self.extract_teacher_info(tree, university_name,page=page))
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

        # 定位所有教师的div元素
        teacher_elements = tree.xpath("/html/body/div/div/div[3]/div/div/div/div/div[2]/div/div[1]/div")
        for element in teacher_elements:
            # 提取教师名字
            name_elements = element.xpath(".//a[@class='lib_title']/text()")
            name = name_elements[0].strip() if name_elements else None
            if not name:
                continue  # 如果没有找到教师名字，跳过当前迭代

            # 提取href，用于生成URL和ID
            href_elements = element.xpath(".//div[@class='sz_unit float-left']/a/@href")
            href = href_elements[0].strip() if href_elements else None

            # 提取职称
            professional_title_elements = element.xpath(".//div[@class='sz_unit float-left']/a/div[1]/text()")
            professional_title = professional_title_elements[0].strip() if professional_title_elements else None

            # 提取导师资格
            mentor_elements = element.xpath(".//div[@class='sz_unit float-left']/a/div[2]/text()")
            mentor = mentor_elements[0].strip() if mentor_elements else None

            # 提取学院名
            college_elements = element.xpath(".//div[@class='sz_unit float-left']/a/div[3]/text()")
            college = college_elements[0].strip() if college_elements else None

            # 生成ID
            teacher_id = university_name + "_" + href.split('/')[-3] if href else None

            # 生成URL
            teacher_url = href if href else None

            teacher_info = {
                "_id": teacher_id,
                "name": name,
                "college": college,
                "professional_title": professional_title,
                "mentor": mentor,
                "url": teacher_url
            }
            new_teachers.append(teacher_info)  # 将新教师信息添加到新列表中
        # print(new_teachers)
        return new_teachers  # 返回新提取的教师信息