from config import CONFIG
from lxml import html
import re
from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from scrapers.scraper import Scraper

class XJTUScraper(Scraper):
    def get_page_links(self, university_name):
        # 生成26个链接
        base_url = 'https://gr.xjtu.edu.cn/home?p_p_id=cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_mvcRenderCommandName=%2Fsearch%2Fview_teacher_search&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_name=&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_colleges=&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_firstspell={}&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_departments='
        all_list = []
        letters = CONFIG['LETTERS']
        for letter in letters:
            url = base_url.format(letter)
            all_list.append(url)
        return all_list

    def extract_number(self,text):
        match = re.search(r'显示(\d+)结果', text)
        if match:
            return int(match.group(1))
        return 0

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
                EC.presence_of_element_located((By.XPATH, "//*[@id='portlet_cn_edu_xjtu_gr_web_latestupdate_XjtuGrHomeWebLatestupdatePortlet_INSTANCE_ah9Iid6k6mfK']/div/div/div/div/div[1]/span[1]/div[1]")))

            # 获取条数
            try:
                num_items_element = driver.find_element(By.XPATH, "//p[@class='pagination-results']")
                num_items_text = num_items_element.text
                num_items = self.extract_number(num_items_text)
            except NoSuchElementException:
                num_items = 0

            # 计算页数
            num_pages = ceil(num_items / 20)
            print(f"Number of items: {num_items}")
            print(f"Number of pages: {num_pages}")

            teacher_list = []
            # 处理第一页
            tree = html.fromstring(driver.page_source)
            teacher_list.extend(self.extract_teacher_info(tree, university_name, page=1))
            # 获取当前页面的URL
            current_url = driver.current_url
            # 使用正则表达式提取必要的参数
            pattern = re.compile(r'firstspell=(\w)')
            match = pattern.search(current_url)
            firstspell = match.group(1) if match else None
            # 如果提取成功，使用这个参数来构建其他页面的URL
            if firstspell:
                base_url = f"https://gr.xjtu.edu.cn/home?p_p_id=cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_mvcRenderCommandName=%2Fsearch%2Fview_teacher_search&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_name=&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_colleges=&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_departments=&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_firstspell={firstspell}&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_delta=20&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_resetCur=false&p_auth=Mk95CYzO&_cn_edu_xjtu_gr_web_search_XjtuGrHomeWebSearchPortlet_INSTANCE_eIE1VwwFuntr_cur={{page}}"

                # 处理剩下的页
                for page in range(2, int(num_pages) + 1):
                    try:
                        url = base_url.format(page=page)
                        driver.get(url)
                        # 等待新页面加载
                        xpath_expression = "//h2[text()='教师个人主页']"
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_expression)))
                        # 提取信息
                        tree = html.fromstring(driver.page_source)
                        teacher_list.extend(self.extract_teacher_info(tree, university_name, page=page))
                    except TimeoutException:
                        print(f"页面{page}没有加载成功")
                        break
            else:
                print("无法从当前URL中提取首字母")
        finally:
            # 关闭Selenium浏览器
            driver.quit()

        print(f"teacher_list的长度: {len(teacher_list)}")
        # print(teacher_list)
        return teacher_list

    def extract_teacher_info(self, tree, university_name, page):
        new_teachers = []  # 创建一个新列表来存储新提取的教师信息

        # 定位所有教师的tr元素
        teacher_elements = tree.xpath("//table/tbody/tr")
        for element in teacher_elements:
            # 提取教师名字
            name_elements = element.xpath(".//td[contains(@class, 'name-column')]/a/text()")
            if not name_elements:
                continue  # 如果没有找到教师名字，跳过当前迭代
            name = name_elements[0]

            # 提取href，用于生成URL和ID
            href_elements = element.xpath(".//td[contains(@class, 'name-column')]/a/@href")
            href = href_elements[0] if href_elements else None

            # 提取学院名
            college_elements = element.xpath(".//td[contains(@class, 'college-column')]/span/text()")
            college = college_elements[0] if college_elements else None

            # 提取系名
            department_elements = element.xpath(".//td[contains(@class, 'department-column')]/span/text()")
            department = department_elements[0] if department_elements else None

            # 生成ID和URL
            teacher_id = university_name + href.split('/')[-1] if href else university_name + "详情页链接缺失" + name
            teacher_url = 'https://gr.xjtu.edu.cn' + href if href else None

            teacher_info = {
                "_id": teacher_id,
                "name": name,
                "college": college,
                "Department": department,
                "url": teacher_url
            }
            new_teachers.append(teacher_info)  # 将新教师信息添加到新列表中

        print(f"第{page}页长度: {len(new_teachers)}")
        return new_teachers  # 返回新提取的教师信息
