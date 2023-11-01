THU_UNIVERSITY = {
    'name': '清华大学_test',
    'module': 'thu_scraper',
    'class': 'THUScraper',
     'colleges': [
            {
             'name': '公共管理学院',
             'url': 'https://www.sppm.tsinghua.edu.cn/szdw/qzjs/qyjs.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[@id="xp_zw"]//table//tr[td/div/a[@title] and td/div]',
                 "name_xpath": ".//td[1]/div/a/text()",
                 "url_xpath":".//td[1]/div/a/@href",
                 "prefix_url": "https://www.sppm.tsinghua.edu.cn/",#一定要以/结尾
                 "id_path_index": -1,
             }
         },#1process_college_with_xpath（一页）
            {
             'name': '环境学院',
             'url': 'https://www.env.tsinghua.edu.cn/szdw/jyjs.htm',
             'processing_function': 'process_pages_with_xpath',
             "structures": {
                 "page_elements_xpath": '//li[@class="dqlm"]/div[@class="item-inner-list"]/div[@class="item-inner-list-content common-display "]/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",
                 "page_prefix_url":"https://www.env.tsinghua.edu.cn/szdw/",

                 "teacher_elements_xpath": '//div[@class="academician-inner-content"]/a',
                 "name_xpath": "./@title",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.env.tsinghua.edu.cn/ ",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },#2process_pages_with_xpath（按系分页）
            {
             'name': '经济管理学院',
             'url': 'https://www.sem.tsinghua.edu.cn/js/szdw.htm',
             'processing_function': 'process_pages_with_chrome',
             "structures": {
                 "page_located":'//*[@class="pb_sys_common pb_sys_normal pb_sys_style1"]',#页面加载
                 "items_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[1]',
                 "items_number_regex": '\\d+',# "共155条"匹配155
                 "page_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[3]',
                 "page_number_regex": '\\d+$',# "1/16"匹配16

                 "teacher_elements_xpath": '//div[@class="detailsdes"]/div[@class="content"]',
                 "name_xpath": "./div[@class='name']/text()",
                 "url_xpath": "./div[@class='detailsMore w-flex justify-content-end align-items-center']/a/@href",
                 "prefix_url": "https://www.sem.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },#3process_pages_with_chrome(下页)
            {
             'name': '土木水利学院',
             'url': 'https://www.civil.tsinghua.edu.cn/ce/szdw/jiaosh.htm',
             'processing_function': 'process_pages_with_chrome',
             "structures": {
                 "page_located":'//*[@class="p_pages"]',#页面加载
                 "page_number_xpath": '/html/body/div[2]/div[3]/span/span[8]/a/text()',

                 "teacher_elements_xpath": '//ul[@class="teach-list clearfix"]/li//div[@class="lind-bottom"]',
                 "name_xpath": './div[@class="teacher-name"]/a/text()',
                 "url_xpath": './div[@class="teacher-name"]/a/@href ',
                 "prefix_url": "https://www.civil.tsinghua.edu.cn/ce/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '马克思主义学院',
             'url': 'https://www.smarx.tsinghua.edu.cn/szqk/js.htm',
             'processing_function': 'process_xpath_chrome',
             "structures": {
                 "page_elements_xpath": '//ul[@class="pull-right banner-ul clearfix"]/li/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",                #js.htm      https://www.smarx.tsinghua.edu.cn/szqk/    js.htm
                 "page_prefix_url":" https://www.smarx.tsinghua.edu.cn/szqk/",

                 "page_located":'//*[@class="pb_sys_common pb_sys_normal pb_sys_style1"]',#页面加载
                 "items_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[1]',
                 "items_number_regex": '\\d+',# "共155条"匹配155
                 "next_page_link":'//a[text()="下页"]',

                 "teacher_elements_xpath": '//ul[@class="teach-list clearfix"]/li//div[@class="teacher-name"]/a',
                 "name_xpath": ".//text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.smarx.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },#4process_xpath_chrome(按系分，下页)
# ... 更多学院
            {
             'name': '机械工程学院_1',
             'department': '机械工程系',
             'url': 'https://me.tsinghua.edu.cn/szdw/zzjs.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                    "teacher_elements_xpath": "//div[@class='tea-text']/a",
                    "name_xpath": "./text()",
                    "url_xpath": "./@href",
                    "prefix_url": "https://me.tsinghua.edu.cn/",
                    "id_path_index": -1,
             }
         },#按系分，6个系  process_college_with_xpath
            {
             'name': '机械工程学院_2',
             'department': '精密仪器系',
             'url': 'http://faculty.dpi.tsinghua.edu.cn/index.html',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                    "teacher_elements_xpath": "//div[@class='third']//li",
                    "name_xpath": "./h6/text()",
                    "url_xpath": "./a/@href",
                    "prefix_url": "http://faculty.dpi.tsinghua.edu.cn/",
                    "id_path_index": -1,
             }
         },
            {
             'name': '机械工程学院_3',
             'department': '能源与动力工程系',
             'url': 'https://www.depe.tsinghua.edu.cn/szdw/szxx1.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": "//tbody/tr/td//a",
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.depe.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '机械工程学院_4',
             'department': '车辆与运载学院',
             'url': 'http://www.svm.tsinghua.edu.cn/column/26_1.html',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[@class="list"]//a',
                 "name_xpath": "./div/text()",
                 "url_xpath": "./@href",
                 "prefix_url": "http://www.svm.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '机械工程学院_5',
             'department': '工业工程系',
             'url': 'https://www.ie.tsinghua.edu.cn/szll/jsdw.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//ul[@class="teacher"]//li/div[@class="box"]',
                 "name_xpath": "./a/@title",
                 "url_xpath": "./a/@href",
                 "prefix_url": "https://www.ie.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '机械工程学院_6',
             'department': '基础工业训练中心',
             'url': 'https://www.icenter.tsinghua.edu.cn/szdw/zzjs.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//table[@align="center"]/tr/td[@style="text-align: center;"]/a',
                 "name_xpath": "./@title",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.icenter.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '人文学院_1',
             'department': '中国语言文学系',
             'url': 'https://www.zhongwen.tsinghua.edu.cn/szdw/js.htm',
             'processing_function': 'process_xpath_chrome',
             "structures": {
                 "page_elements_xpath": '//ul[@class="pull-right banner-ul clearfix"]/li/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",
                 "page_prefix_url": "https://www.zhongwen.tsinghua.edu.cn/szdw/",

                 "page_located": '//*[@class="p_pages"]',  # 页面加载
                 "items_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[1]',
                 "items_number_regex": '\\d+',  # "共155条"匹配155
                 "next_page_link": '//a[text()="下页"]',

                 "teacher_elements_xpath": '//div[@class="teacher-name"]/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.zhongwen.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },#按系分，5个系_函数4
            {
             'name': '人文学院_2',
             'department': '外国语言文学系',
             'url': 'https://www.dfll.tsinghua.edu.cn/szll/axkq1.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                    "teacher_elements_xpath": "//ul[@class='clearfix']/li/a",
                    "name_xpath": "./text()",
                    "url_xpath": "./@href",
                    "prefix_url": "https://www.dfll.tsinghua.edu.cn/",
                    "id_path_index": -1,
             }
         }, #函数1
            {
             'name': '人文学院_3',
             'department': '历史系',
             'url': 'https://www.lsx.tsinghua.edu.cn/szdw1.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": "//div[@id='vsb_content_2']/p[3]/a | //div[@id='vsb_content_2']/p[5]/a | //div[@id='vsb_content_2']/p[7]/a",
                 "name_xpath": "./span/text()",
                  "url_xpath": "./@href",
                  "prefix_url": "https://www.lsx.tsinghua.edu.cn/",
                  "id_path_index": -1,
             }
         },
            {
             'name': '人文学院_4',
             'department': '科学史系',
             'url': 'http://www.dhs.tsinghua.edu.cn/?page_id=2087',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                   "teacher_elements_xpath": "//div[@id='w4pl-inner-438']/a | //div[@id='w4pl-inner-446']/a | //div[@id='w4pl-inner-447']/a | //div[@id='w4pl-inner-448']/a",
                   "name_xpath": "./text()",
                   "url_xpath": "./@href",
                   "prefix_url": "",
                   "id_path_index": -1,
             }
         },
            {
             'name': '人文学院_5',
             'department': '哲学系',
             'url': 'https://www.phil.tsinghua.edu.cn/szqk/js.htm',
             'processing_function': 'process_xpath_chrome',
             "structures": {
                 "page_elements_xpath": '//ul[@class="pull-right banner-ul clearfix"]/li/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",
                 "page_prefix_url": "https://www.phil.tsinghua.edu.cn/szqk/",

                 "page_located": '//*[@class="p_t"]',  # 页面加载
                 "items_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[1]',
                 "items_number_regex": '\\d+',  # "共155条"匹配155
                 "next_page_link": '//a[text()="下页"]',

                 "teacher_elements_xpath": '//div[@class="teacher-name"]/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.phil.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },#函数4
# ... 更多学院
            {
             'name': '航天航空学院',
             'url': 'https://www.hy.tsinghua.edu.cn/szqk/szxx.htm',
             'processing_function': 'process_college_with_xpath',  # 处理函数
             "structures": {
                 "teacher_elements_xpath": "//div[@id='vsb_content']/p/a",
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.hy.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '社会科学学院',
             'url': 'https://www.sss.tsinghua.edu.cn/szll.htm',
             'processing_function': 'process_college_with_xpath',  # 处理函数
             "structures": {
                 "teacher_elements_xpath": '//ul/li[@class="wow fadeInLeft"]/a',
                 "name_xpath": "./h2/div/text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.sss.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '信息科学技术学院_1',
             'department': '电子工程系',
             'url': 'https://www.ee.tsinghua.edu.cn/ryqk/teacher/xxgdzyjs/js2.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": "//div[@class='t']/a",
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "",
                 "id_path_index": -3,
             }
         },  # 按系分，6个系  process_college_with_xpath
            {
             'name': '信息科学技术学院_2',
             'department': '计算机科学与技术系',
             'url': 'https://www.cs.tsinghua.edu.cn/szzk/jzgml.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": "//li/div[@class='text']",
                 "name_xpath": "./h2/a/text()",
                 "url_xpath": "./h2/a/@href",
                 "prefix_url": "https://www.cs.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '信息科学技术学院_3',
             'department': '自动化系',
             'url': 'https://www.au.tsinghua.edu.cn/szdw/jsdw1/ayjscz/kzyjcyjs.htm',
             'processing_function': 'process_xpath_xpath',
             "structures": {
                 "page_elements_xpath":'//dl[@class="list18 list19"]//dd/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",
                 "page_prefix_url": "https://www.au.tsinghua.edu.cn/szdw/jsdw1/ayjscz/",

                 "teacher_elements_xpath":'//ul[@class="list13 flex"]/li/a',
                 "name_xpath": ".//h3//text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.au.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },#5 process_xpath_xpath(按系分，一页)
            {
             'name': '信息科学技术学院_4',
             'department': '集成电路学院',
             'url': 'https://www.sic.tsinghua.edu.cn/szdw/rygc/szxx.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": "//div[@class='clearfloat list_zhy']/a",
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.sic.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '信息科学技术学院_5',
             'department': '软件学院',
             'url': 'https://www.thss.tsinghua.edu.cn/szdw/jsml.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": "//div[@class='name-container']/a",
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.thss.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '信息科学技术学院_6',
             'department': '网络科学与网络空间研究院',
             'url': 'https://www.insc.tsinghua.edu.cn/szdw_/zzjs.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": "//p[@style='text-indent: 0em;']//a",
                 "name_xpath": ".//text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.insc.tsinghua.edu.cn/",
                 "id_path_index": -1,
             }
         },
            {
             'name': '建筑学院_0',
             'url': 'http://lad.arch.tsinghua.edu.cn/current-faculty-members/',
             'processing_function': 'process_college_with_xpath',  # 处理函数
             "structures": {
                 "teacher_elements_xpath": "//div[@class='leadership-wrapper']",
                 "name_xpath": ".//h1[@class='leadership-function title-median']/text()",
                 "url_xpath": "",
                 "prefix_url": "",
                 "id_path_index": -1,
             }
         },#最初的建筑学院-景观学系，弃用
            {
             'name': '建筑学院',
             'url': 'http://www.arch.tsinghua.edu.cn/column/sz',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//ul/li/div[@class="name"]/a',
                 "name_xpath": "./div/text()",
                 "url_xpath": "./@href",
                 "prefix_url": "http://www.arch.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '法学院',
             'url': 'https://www.law.tsinghua.edu.cn/szll/byjs/zzjs.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[@class="side-name"]/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.law.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '新闻与传播学院',
             'url': 'https://www.tsjc.tsinghua.edu.cn/xysz/jszy/jxkyjs1.htm',
             'processing_function': 'process_pages_with_chrome',
             "structures": {
                 "page_located": '//*[@class="pb_sys_common pb_sys_normal pb_sys_style1"]',  # 页面加载
                 "items_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[1]',
                 "items_number_regex": '\\d+',  # "共155条"匹配155
                 "page_number_xpath": '//div[@id="page-list"]/span[2]/span[7]/a',
                 "page_number_regex": '\\d+',
                 "next_page_link": '//a[text()="下页"]',

                 "teacher_elements_xpath": '//div[@class="teacher-name"]',
                 "name_xpath": "./a/text()",
                 "url_xpath": "./a/@href",
                 "prefix_url": "https://www.tsjc.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '材料学院',
             'url': 'https://www.mse.tsinghua.edu.cn/szqk/jsdw1.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[@class="szdw-list"]/div[@class="ul-box"]/ul/li/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.mse.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '美术学院',
             'url': 'https://www.ad.tsinghua.edu.cn/jx/js/ayx1.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//ul/li',
                 "name_xpath": './/div[@class="teacher_name"]/text()',
                 "url_xpath": "./a/@href",
                 "prefix_url": "https://www.ad.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '电机工程与应用电子技术系',
             'url': 'https://www.eea.tsinghua.edu.cn/szdw/zzjs/qbjs/all.htm',
             'processing_function': 'process_pages_with_chrome',
             "structures": {
                 "page_located": '//*[@class="pb_sys_common pb_sys_normal pb_sys_style1"]',  # 页面加载
                 "items_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[1]',
                 "items_number_regex": '\\d+',  # "共155条"匹配155
                 "page_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[2]/span[9]/a',
                 "page_number_regex": '\\d+',
                 "next_page_link": '//a[text()="下页"]',

                 "teacher_elements_xpath": '//ul/li/a',
                 "name_xpath": './div[@class="con fr"]/p[1]/text()',
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.eea.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '工程物理系',
             'url': 'https://www.ep.tsinghua.edu.cn/szdw/jsdw.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[@class="szdw-list"]/div/ul/li/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.ep.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '化学工程系',
             'url': 'https://www.chemeng.tsinghua.edu.cn/szdw/sz1/aflck/zgj.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '/html/body/div[6]/div/div[@class="team-list"]/ul/li/div',
                 "name_xpath": "./a/h3/text()",
                 "url_xpath": "./a/@href",
                 "prefix_url": "https://www.chemeng.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '核能与新能源技术研究院',
             'url': 'https://www.inet.tsinghua.edu.cn/szdw/zgzc.htm',
             'processing_function': 'process_xpath_xpath',
             "structures": {
                 "page_elements_xpath":'//ul[@class="pull-right banner-ul clearfix"]/li/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",
                 "page_prefix_url": "https://www.inet.tsinghua.edu.cn/szdw/",

                 "teacher_elements_xpath":'//ul/li/p/a | //ul[@id="pcdh"]/li/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.inet.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '理学院_1',
             'department': '数学科学系',
             'url': 'https://www.math.tsinghua.edu.cn/szdw1/jsml.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//p[@style="text-align: justify;"]/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.math.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },  # 理学院 5个系
            {
             'name': '理学院_2',
             'department': '物理系',
             'url': 'https://www.phys.tsinghua.edu.cn/ry/jsfc/azyfl.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//ul/li/div[@class="teacher-name"]/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.phys.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '理学院_3',
             'department': '化学系',
             'url': 'https://www.chem.tsinghua.edu.cn/szdw/zzjg/apypx1.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[3]/div[@class="zhy_list"]/a | //div[4]/div[@class="zhy_list"]/a | //div[5]/div[@class="zhy_list"]/a |//div[6]/div[@class="zhy_list"]/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.chem.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '理学院_4',
             'department': '地球系统科学系',
             'url': 'http://faculty.dess.tsinghua.edu.cn/qzjs-xm.jsp?urltype=tree.TreeTempUrl&wbtreeid=1285',
             'processing_function': 'process_pages_with_all_chrome',
             "structures": {
                     "page_located": '//*[@id="pageBarLastPageIdu11"]',  # 页面加载
                     "items_number_id": 'pageBarTotalNumberIdu11',
                     "page_number_id": 'pageBarTotalPageIdu11',
                     "next_page_id":'pageBarNextPageIdu11',  #通过该id点击下一页

                     "teacher_elements_xpath": '//li//div[@class="txt"]',
                     "name_xpath": "./h4/a",
                     "url_xpath": "./h4/a",
                     "prefix_url": "",  # 一定要以/结尾
                     "id_path_index": -3,
              }
         },
         # 3—1、chrome处理学院的函数(很多页)  process_pages_with_all_chrome,   动态加载条数、页数的
         #extract_teacher_info_with_chrome  动态提取信息
            {
             'name': '理学院_5',
             'department': '天文系',
             'url': 'https://astro.tsinghua.edu.cn/zh/ry/js.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//tr[@class="cat-list-row0"]',
                 "name_xpath": './td[@class="item-title"]/a/text()',
                 "url_xpath": './td[@class="item-title"]/a/@href',
                 "prefix_url": "https://astro.tsinghua.edu.cn/zh/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '教育研究院',
             'url': 'https://www.ioe.tsinghua.edu.cn/szdw/jyzcyglyjs.htm',
             'processing_function': 'process_xpath_xpath',
             "structures": {
                 "page_elements_xpath": '//ul[@class="left-nav"]/li/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",
                 "page_prefix_url": "https://www.ioe.tsinghua.edu.cn/szdw/",

                 "teacher_elements_xpath": '//ul/li/div[@class="teacher-name"]/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.ioe.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '生命科学学院',
             'url': 'https://life.tsinghua.edu.cn/szdw/jzyg1.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[2]/ul[@class="clearfix"]/li/a | //div[4]/ul[@class="clearfix"]/li/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://life.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '全球创新学院',
             'url': 'https://gix.tsinghua.edu.cn/sz.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//ul[@class="clearfix"]/li/a',
                 "name_xpath": "./h4/text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.sppm.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '医学院_1',
             'department': '基础医学系',
             'url': 'https://www.med.tsinghua.edu.cn/szdw/jcyxx.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//ul/li/div[@class="con"]/dd/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.med.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },  # 医学院 3个系
            {
             'name': '医学院_2',
             'department': '生物医学工程系',
             'url': 'https://www.med.tsinghua.edu.cn/szdw/swyxgcx.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//ul/li/div[@class="con"]/dd/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.med.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '医学院_3',
             'department': '临床医学院',
             'url': 'https://www.scm.tsinghua.edu.cn/szll/szdw/lcxl.htm',
             'processing_function': 'process_xpath_xpath',
             "structures": {
                 "page_elements_xpath": '//li[@class="on"]/dl/dd/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",
                 "page_prefix_url": "https://www.scm.tsinghua.edu.cn/szll/szdw/",

                 "teacher_elements_xpath": '//div[@class="bottom clearfix"]/dd/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.scm.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '万科公共卫生与健康学院',
             'url': 'https://vsph.tsinghua.edu.cn/szdw/zzjs.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[@class="txt"]/a',
                 "name_xpath": "./text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://vsph.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '交叉信息研究院',
             'url': 'https://iiis.tsinghua.edu.cn/people/#jy1',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//ul/li//div[@class="info"]',
                 "name_xpath": './div[@class="name"]/a/text()',
                 "url_xpath":'./div[@class="name"]/a/@href',
                 "prefix_url": "https://iiis.tsinghua.edu.cn/",#一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '体育部',
             'url': 'https://www.thsports.tsinghua.edu.cn/yxgk/szdw.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[@class="line"]/a',
                 "name_xpath": "./div/text()",
                 "url_xpath": "./@href",
                 "prefix_url": "https://www.thsports.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '语言教学中心',
             'url': 'https://www.lc.tsinghua.edu.cn/szdw/jxtd/yjsyy.htm',
             'processing_function': 'process_xpath_chrome',
             "structures": {
                 "page_elements_xpath": '//div[@class="pageNav"]/div[@class="list"]/ul/li/a',
                 "page_name_xpath": "./text()",
                 "page_url_xpath": "./@href",
                 "page_prefix_url": " https://www.lc.tsinghua.edu.cn/szdw/jxtd/",

                 "page_located": '//*[@class="pb_sys_common pb_sys_normal pb_sys_style1"]',  # 页面加载
                 "items_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[1]',
                 "items_number_regex": '\\d+',  # "共155条"匹配155
                 "next_page_link": '//a[text()="下页"]',

                 "teacher_elements_xpath": '//div[@class="teacher"]/ul/li',
                 "name_xpath": './div[@class="name"]/a/text()',
                 "url_xpath": './div[@class="name"]/a/@href',
                 "prefix_url": "https://www.lc.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '出土文献研究与保护中心',
             'url': 'https://www.ctwx.tsinghua.edu.cn/szdw/qzjs.htm',
             'processing_function': 'process_pages_with_chrome',
             "structures": {
                 "page_located":'//*[@class="pb_sys_common pb_sys_normal pb_sys_style1"]',#页面加载
                 "items_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]/span[1]',
                 "items_number_regex": '\\d+',# "共155条"匹配155
                 "page_number_xpath": '//div[@class="pb_sys_common pb_sys_normal pb_sys_style1"]//span[5]/a',
                 "page_number_regex": '\\d+',# "1/16"匹配16

                 "teacher_elements_xpath": '//ul[@class="teach-list clearfix"]/li',
                 "name_xpath": './/div[@class="teacher-name"]/a/text()',
                 "url_xpath": './/div[@class="teacher-name"]/a/@href',
                 "prefix_url": "https://www.ctwx.tsinghua.edu.cn/",  # 一定要以/结尾
                 "id_path_index": -1,
             }
         },
            {
             'name': '艺术教育中心',
             'url': 'https://www.arts.tsinghua.edu.cn/szdw.htm',
             'processing_function': 'process_college_with_xpath',
             "structures": {
                 "teacher_elements_xpath": '//div[@id="vsb_content"]/p/a',
                 "name_xpath": "./span/text()",
                 "url_xpath":"./@href",
                 "prefix_url": "https://www.arts.tsinghua.edu.cn/",#一定要以/结尾
                 "id_path_index": -1,
             }
         },
        ]
}
