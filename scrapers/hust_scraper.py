from config import CONFIG
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pypinyin import lazy_pinyin
from scrapers.scraper import Scraper

class HUSTScraper(Scraper):

    def fetch_teachers(self, url, university_name):
        # 启动Selenium浏览器
        driver_path =CONFIG['DRIVER_PATH']
        driver = webdriver.Chrome(executable_path=driver_path)
        #driver = webdriver.Chrome()
        try:
            # 打开网页
            driver.get(url)
            # 等待页面加载
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pageBarNextPageId1036549")))

            # 获取条数和页数
            num_items = driver.find_element(By.ID, "pageBarTotalNumberId1036549").text
            num_pages = driver.find_element(By.ID, "pageBarTotalPageId1036549").text
            print(f"条数: {num_items}")
            print(f"页数: {num_pages}")

            teacher_list = []

            # 处理第一页
            tree = html.fromstring(driver.page_source)
            teacher_list.extend(self.extract_teacher_info(tree, university_name, page=1))

            # 处理剩下的页
            for page in range(2, int(num_pages) + 1):
                # 找到并点击下一页按钮
                next_button = driver.find_element(By.ID, "pageBarNextPageId1036549")
                next_button.click()

                # 等待新页面加载
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pageBarCurPageId1036549")))
                # 提取信息
                tree = html.fromstring(driver.page_source)
                teacher_list.extend(self.extract_teacher_info(tree, university_name, page=page))

        finally:
            driver.quit()  # 关闭Selenium浏览器

        print(f"teacher_list的长度: {len(teacher_list)}")
        # print(teacher_list)
        return teacher_list

    def extract_teacher_info(self, tree,university_name,page):
        new_teachers = []  # 创建一个新列表来存储新提取的教师信息
        # 定位所有教师的li元素
        teacher_elements = tree.xpath("//div[@class='jsfc-list']/ul/li")

        for element in teacher_elements:
            # teacher_id = element.xpath("@id")[0]
            name = element.xpath(".//div[@class='jsfc-info']/h3/text()")[0]
            professional_title = element.xpath(".//div[@class='jsfc-info']/p/text()")[0].split('——')[1]
            teacher_url = element.xpath(".//a/@href")[0]
            # print(teacher_url)
            try:
                teacher_id = university_name + "_" + teacher_url.split('/')[3]
            except IndexError:
                print(f"Error: 'teacher_url.split('/')[3]' list index out of range for name: {name}")

            # 如果teacher_id为“system”，则将URL设置为null
            if teacher_url.split('/')[3] == "system":
                teacher_url = None
                # 获取名字的拼音并将其与"****大学_"连接
                name_pinyin = ''.join(lazy_pinyin(name))
                teacher_id = university_name + "_" + name_pinyin

            teacher_info = {
                "_id": teacher_id,
                "name": name,
                "professional_title": professional_title,
                "url": teacher_url
            }
            new_teachers.append(teacher_info)  # 将新教师信息添加到新列表中

        print(f"第{page}页长度: {len(new_teachers)}")
        return new_teachers  # 返回新提取的教师信息

    def get_page_links(self, university_name):
        url = 'http://faculty.hust.edu.cn/#section1'
        tree = self.get_and_save_page(url, university_name + '_original_page.txt', 0)
        base_url = 'http://faculty.hust.edu.cn/'
        all_list = tree.xpath('//div[@class="letter px1280"]/div/a/@href')
        # 返回完整的链接列表
        return [base_url + link for link in all_list]
