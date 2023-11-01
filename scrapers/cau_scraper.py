from config import CONFIG
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapers.scraper import Scraper

class CAUScraper(Scraper):
    def get_page_links(self, university_name):
        # 只有一页，而非26页
        url = 'http://faculty.cau.edu.cn/67/list.htm?tectitle=&selectedCareers=&selectedDepartments=&selectedletters='
        all_list = []
        all_list.append(url)
        return all_list

    def fetch_teachers(self, url, university_name):
        chrome_options = webdriver.ChromeOptions()
        #禁用代理
        chrome_options.add_argument("--no-proxy-server")
        # 设置Chrome为无头模式
        chrome_options.add_argument("--headless")
        # 启动Selenium浏览器
        driver_path = CONFIG['DRIVER_PATH']
        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        # driver = webdriver.Chrome()
        try:
            # 打开网页
            driver.get(url)
            # 等待页面加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "last"))
            )
            '''
            # 下载新页面
            updated_page_source = driver.page_source
            with open('updated_page.txt', 'w', encoding='utf-8') as file:
                file.write(updated_page_source)
                '''
            # 计算页数
            tree = html.fromstring(driver.page_source)
            num_pages_elements = tree.xpath("//em[@class='all_pages']/text()")
            num_pages = num_pages_elements[0].strip() if num_pages_elements else None
            print(f"共有{num_pages}页")

            teacher_list = []
            # 处理第一页
            tree = html.fromstring(driver.page_source)
            new_teachers = self.extract_teacher_info(tree, university_name, page=1)
            teacher_list.extend(new_teachers)
            # print(f"第1页教师信息: {new_teachers}")
            print(f"第1页教师数量: {len(new_teachers)}")

            # 处理剩下的页
            for page in range(2, int(num_pages) + 1):  # num_pages+ 1
                try:
                    # 找到并点击下一页按钮
                    if page == 2:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[2]/ul/li[2]/a[2]"))
                        )
                    else:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[2]/ul/li[2]/a[3]"))
                        )

                    # 使用JavaScript来点击按钮
                    driver.execute_script("arguments[0].click();", next_button)
                    # 获取当前页的第一个和最后一个教师的名字
                    first_teacher_name = teacher_list[0]['name']
                    last_teacher_name = teacher_list[-1]['name']
                    # 等待新页面加载，即第一个和最后一个教师的名字都发生变化
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(By.XPATH, "//div[@class='news_title']").text != first_teacher_name
                                  and d.find_element(By.XPATH,
                                                     "//li[@class='news list_item tec_rec'][last()]//div[@class='news_title']").text != last_teacher_name
                    )

                    # 提取信息
                    tree = html.fromstring(driver.page_source)
                    new_teachers =self.extract_teacher_info(tree, university_name, page=1)
                    teacher_list.extend(new_teachers)
                    # print(f"第{page}页教师信息: {new_teachers}")
                    print(f"第{page}页教师数量: {len(new_teachers)}")
                except Exception as e:
                    print(f"无法加载第{page}页, 错误类型：{type(e)}, 错误信息: {str(e)}")
                    break

        finally:
            # 关闭Selenium浏览器
            driver.quit()
        print(f"teacher_list的长度: {len(teacher_list)}")
        return teacher_list

    def extract_teacher_info(self, tree, university_name, page):
        new_teachers = []  # 创建一个新列表来存储新提取的教师信息

        # 定位所有教师的li元素
        teacher_elements = tree.xpath("/html/body/div[5]/div/div/div[1]/h3/ul/li")
        for element in teacher_elements:
            # 提取教师名字
            name_elements = element.xpath(".//div[@class='news_wz']/div[@class='news_title']/text()")
            name = name_elements[0].strip() if name_elements else None
            if not name:
                continue  # 如果没有找到教师名字，跳过当前迭代

            # 提取href，用于生成URL和ID
            href_elements = element.xpath(".//a[@class='news_box clearfix']/@href")
            href = href_elements[0].replace(" ", "") if href_elements else None  # 移除空格

            # 提取职称
            professional_title_elements = element.xpath(".//div[@class='news_wz']/p[@class='news_meta'][1]/text()")
            professional_title = professional_title_elements[0].strip() if professional_title_elements else None

            # 提取学院名
            college_elements = element.xpath(".//div[@class='news_wz']/p[@class='news_meta'][2]/text()")
            college = college_elements[0].strip() if college_elements else None

            # 生成ID和URL
            teacher_id = university_name+"_".join(href.split('/')[-3:-1]) if href else None

            # 检查URL是否以"http"开头，否则设为None
            teacher_url = href if href and href.startswith("http") else None

            teacher_info = {
                "_id": teacher_id,
                "name": name,
                "college": college,
                "professional_title": professional_title,
                "url": teacher_url
            }
            new_teachers.append(teacher_info)  # 将新教师信息添加到新列表中

        return new_teachers  # 返回新提取的教师信息




