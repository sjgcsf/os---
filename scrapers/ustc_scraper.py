from config import CONFIG
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapers.scraper import Scraper

class USTCScraper(Scraper):
    def get_page_links(self, university_name):
        # 生成26个链接
        base_url = 'https://faculty.ustc.edu.cn/letter_teacherlist.jsp?urltype=tsites.PinYinTeacherList&wbtreeid=1002&py={}&lang=zh_CN'
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
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".footer.clearfix")))

            # 首先获取包含条数和页数的文本
            fanye_text = driver.find_element(By.ID, "fanye").text
            # 使用正则表达式来解析条数和页数
            import re
            match = re.search(r'共(\d+)条.*?(\d+)/(\d+)', fanye_text)
            if match:
                num_items = int(match.group(1))
                num_pages = int(match.group(3))

            print(f"Number of items: {num_items}")
            print(f"Number of pages: {num_pages}")

            teacher_list = []
            # 处理第一页
            tree = html.fromstring(driver.page_source)
            teacher_list.extend(self.extract_teacher_info(tree,university_name,page=1))

            # 处理剩下的页
            for page in range(2, int(num_pages) + 1):
                # 找到并点击下一页按钮
                next_button = driver.find_element(By.PARTIAL_LINK_TEXT, "下页")
                next_button.click()
                # 等待新页面加载
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".footer.clearfix")))
                # 提取信息
                tree = html.fromstring(driver.page_source)
                teacher_list.extend(self.extract_teacher_info(tree, university_name,page=page))

        finally:
            # 关闭Selenium浏览器
            driver.quit()

        print(f"teacher_list的长度: {len(teacher_list)}")
        return teacher_list

    def extract_teacher_info(self, tree, university_name, page):
        new_teachers = []  # 创建一个新列表来存储新提取的教师信息
        # 定位所有教师的li元素
        teacher_elements = tree.xpath("/html/body/div[4]/div[2]/ul[@class='clearfix']/li")

        for element in teacher_elements:
            # 从提供的HTML中提取教师信息
            name = element.xpath(".//div[@class='jgname']/h2/a/text()")[0]
            try:
                college = element.xpath(".//div[@class='jgname']/p[1]/text()")[0]
            except IndexError:
                college = None
            try:
                professional_title = element.xpath(".//div[@class='jgname']/p[2]/text()")[0]
            except IndexError:
                professional_title = None
            teacher_url = element.xpath(".//div[@class='imgbox']/a/@href")[0]

            if teacher_url.endswith("/index.htm"):
                try:
                    teacher_id = teacher_url.split('/')[-3]
                except IndexError:
                    teacher_id = teacher_url
            elif teacher_url.endswith("/"):
                teacher_id = teacher_url.split('/')[-2]
            else:
                teacher_id = teacher_url.split('/')[-1]
            teacher_id = university_name + "_" + teacher_id.replace('~', '')

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
