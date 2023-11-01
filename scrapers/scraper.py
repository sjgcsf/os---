import re

from config import CONFIG
from lxml import etree
import requests

from abc import ABC, abstractmethod

class Scraper(ABC):
    """
    基类 Scraper，用于定义和实现爬取教师信息的通用逻辑。

    Attributes:
        headers (dict): 包含User-Agent等信息的请求头。
    """

    def __init__(self):
        """
        初始化方法，设定请求头信息。
        """
        self.headers = {
            "User-Agent": CONFIG['USER_AGENT']
        }

    def get_and_save_page(self, url, filename=None, save_flag=0, return_html_content=0):
        """
        根据给定的URL获取页面内容，并根据需要将其保存为文件。

        Args:
            url (str): 要爬取的URL。
            filename (str): 保存页面内容的文件名。
            save_flag (int): 标志是否保存页面。1表示保存，0表示不保存。
            return_html_content (int): 标志是否返回页面的HTML内容。1表示返回HTML内容，0表示返回页面的树结构。
        Returns:
             lxml.etree._ElementTree 或 str: 如果 return_html_content 为 0，则返回页面的树结构；
             如果 return_html_content 为 1，则返回页面的HTML内容。
        """
        headers = {
            'User-Agent': CONFIG["USER_AGENT"]
        }
        proxies = {}#禁用代理
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # 若请求不成功，引发异常

        response.encoding = 'utf-8'  # 或者使用网页实际的编码
        page_text = response.text
        if save_flag:
            with open(filename, 'w', encoding='utf-8') as fp:
                fp.write(page_text)

        if return_html_content:
            return page_text
        else:
            return etree.HTML(page_text)

    @abstractmethod
    def get_page_links(self, university_name):
        """
        抽象方法，用于获取学校的初始页面链接。

        Args:
            university_name (str): 学校名称。

        Returns:
            list: 初始页面的链接列表。
        """
        pass

    @abstractmethod
    def fetch_teachers(self, url, university_name):
        """
        抽象方法，用于从给定的URL获取教师列表。

        Args:
            url (str): 要爬取的URL。
            university_name (str): 学校名称。

        Returns:
            list: 教师信息列表。
        """
        pass

    @abstractmethod
    def extract_teacher_info(self, tree, university_name, page):
        """
        抽象方法，从页面树结构中提取教师的具体信息。

        Args:
            tree (lxml.etree._ElementTree): 页面的树结构。
            university_name (str): 学校名称。
            page (int): 页面编号。

        Returns:
            dict: 提取出的教师信息。
        """
        pass


