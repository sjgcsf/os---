from database_handler import DatabaseHandler
from config import UNIVERSITIES
from config import CONFIG
from config import get_selected_university_scraper

if __name__ == '__main__':
    university_name = CONFIG['UNIVERSITY_NAME']
    print(f"搜集{university_name}教师信息")
    # 实例化爬取教师信息类、数据存储类
    ScraperClass = get_selected_university_scraper()
    scraper = ScraperClass()
    db_handler = DatabaseHandler(CONFIG['HOST'], CONFIG['PORT'], CONFIG['DATABASE_NAME'],
                                 collection_name=CONFIG['COLLECTION_NAME'])
    #db_handler.redownload_and_update_missing_pages()#重新下载缺失的detail_page并更新到MongoDB

    university_config = UNIVERSITIES.get(university_name)
    if 'colleges' in university_config:
        # 1.按学院组织的学校：
        print("该校是按“学院”组织的学校")
        specified_colleges = CONFIG.get('SPECIFIED_COLLEGES', [])
        all_colleges = university_config['colleges']
        # 将所有学院的信息存储在一个字典中，键是学院名，值是URL
        colleges_dict = {college['name']: college['url'] for college in all_colleges}
        #print(colleges_dict)

        # 判断是否有指定的学院：
        if specified_colleges:
            # 根据指定的学院搜索
            print("有指定的学院")
            for college_name in specified_colleges:
                if college_name in colleges_dict:
                    college_url = colleges_dict[college_name]
                    print(f"开始搜集 {college_name} 的教师信息！")
                    teacher_list = scraper.fetch_teachers(college_url, university_name, college_name)
                    db_handler.save_teacher_info_to_mongo(teacher_list)
                else:
                    print(f"错误：学院 {college_name} 在配置中未找到！")
        else:
            # 搜索全部学院
            print("搜索全部学院")
            for college_name, college_url in colleges_dict.items():
                print(f"开始搜集 {college_name} 的教师信息！")
                teacher_list = scraper.fetch_teachers(college_url, university_name, college_name)
                db_handler.save_teacher_info_to_mongo(teacher_list)

    else:
        # 2.整页存储的学校：
        letters = CONFIG['LETTERS']
        specififd_letters = CONFIG['SPECIFIED_LETTERS']
        all_links = scraper.get_page_links(university_name)  # 获得初始的26/1网页的链接
        # 判断是否有指定的首字母
        if specififd_letters:
            # 根据指定的首字母搜索
            for letter in specififd_letters:
                i = letters.index(letter)  # 找到大写字母在 letters 列表中的索引
                link = all_links[i]  # 使用该索引来从 all_list 中取得相应的链接
                print(f"开始搜集首字母为 {letters[i].upper()} 的教师信息！")
                teacher_list = scraper.fetch_teachers(link, university_name)
                db_handler.save_teacher_info_to_mongo(teacher_list)
        else:
            # 搜索全部首字母
            for i, link in enumerate(all_links):
                print(f"开始搜集首字母为 {letters[i].upper()} 的教师信息！")
                teacher_list = scraper.fetch_teachers(link, university_name)
                db_handler.save_teacher_info_to_mongo(teacher_list)

    print(f"学校： {university_name} 的教师信息搜索完毕！")
    # 下载第n个教师详情页html以查看
    #db_handler.save_teacher_html_from_mongo(1)