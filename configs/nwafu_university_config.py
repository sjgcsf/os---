# nwafu_university_config.py
NWAFU_UNIVERSITY = {
    'name': '西北农林科技大学_test',
    'module': 'nwafu_scraper',
    'class': 'NWAFUScraper',
     'colleges': [
            {
                'name': '生命学院',
                'url': 'https://sm.nwafu.edu.cn/szdw/js2/index.htm',
                'structures': {
                        'page_count': 3,
                        'title_page_xpaths': [
                            '//a[contains(text(), "副教授")]/@href',
                            '//a[contains(text(), "中级职称")]/@href'
                        ],
                        'prefix_title_page': 'https://sm.nwafu.edu.cn/szdw/szdw/',#这其实也可以通过页面获得
                        'teacher_elements_xpath': "//div[@class='w-full ml-2 mr-2 mb-8 mx-auto ']/p/a",
                        'name_xpath': ".//text()",
                        'url_xpath':".//@href",
                        'prefix_url': ['https://sm.nwafu.edu.cn/szdw/js2/','https://sm.nwafu.edu.cn/szdw/fjs/','https://sm.nwafu.edu.cn/szdw/zjzc/'],
                        #prefix_url可能是当前页面的前缀，到时候再改一改
                        'id_path_index': -1#默认值删去就好了
                    },
            },
            {
                'name': '农学院',
                'url': 'https://nxy.nwsuaf.edu.cn/szdw/jsyjy/index.htm',
                'structures': {
                    'page_count': 3,
                    'title_page_xpaths': [
                        '//div[@class="sort_leftcont"]/ul/li/a[contains(text(), "副教授、副研究员")]/@href',
                        '//div[@class="sort_leftcont"]/ul/li/a[contains(text(), "中级职称")]/@href'
                    ],
                    'prefix_title_page':  'https://nxy.nwsuaf.edu.cn/szdw/szdw/',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath': "//a[contains(@href, 'szdw/zjrc/') or contains(@href, 'szdw/fjsfyjy/') or contains(@href, 'szdw/zjzc/')]",
                    'name_xpath': ".//text()",
                    'url_xpath': ".//@href",
                    'prefix_url': ['','',''],
                    # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
                'name': '马克思主义学院',
                'url': 'https://iipe.nwsuaf.edu.cn/szdw/index.htm',
                'structures': {
                    'page_count': 1,
                    'title_page_xpaths': [],
                    'prefix_title_page': '',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath':"//a[(contains(@href, 'js/') or contains(@href, 'fjs/') or contains(@href, 'js1/') or contains(@href, 'zj/')) and not(contains(@href, 'index.htm'))]",
                    'name_xpath': ".//text()",
                    'url_xpath': ".//@href",
                    'prefix_url': ['https://iipe.nwsuaf.edu.cn/szdw/'],
                    # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
                'name': '语言文化学院',
                'url': 'https://fld.nwsuaf.edu.cn/szdw/js/index.htm',
                'structures': {
                    'page_count': 3,
                    'title_page_xpaths': [
                        '//a[contains(text(), "副教授")]/@href',
                        '//a[contains(text(), "讲师")]/@href'
                    ],
                    'prefix_title_page': 'https://fld.nwsuaf.edu.cn/szdw/szdw/',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath': ["//tbody/tr/td/p//a","//tbody/tr/td/p//a","//a[contains(@href, 'szdw/js_szdw/')]"],
                    'name_xpath': ".//text()",
                    'url_xpath':  ".//@href",
                    'prefix_url': ['https://fld.nwsuaf.edu.cn/szdw/js/','https://fld.nwsuaf.edu.cn/szdw/fjs/',''],
                    # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
                'name': '体育部',
                'url': 'https://tyb.nwsuaf.edu.cn/szdw/js/index.htm',
                'structures': {
                    'page_count':3,
                    'title_page_xpaths': ['//div[@class="sort_leftcont"]/ul/li/a[contains(text(), "副教授")]/@href',
                        '//div[@class="sort_leftcont"]/ul/li/a[contains(text(), "讲师")]/@href'],
                    'prefix_title_page': 'https://tyb.nwsuaf.edu.cn/szdw/szdw/',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath':"//table[@border='0']/tbody/tr/td/a",
                    'name_xpath': ".//text()",
                    'url_xpath': ".//@href",
                    'prefix_url': [ 'https://tyb.nwsuaf.edu.cn/szdw/js/','https://tyb.nwsuaf.edu.cn/szdw/fjs/','https://tyb.nwsuaf.edu.cn/szdw/js1/'],
                    # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
                'name': '园艺学院',
                'url': 'https://yyxy.nwsuaf.edu.cn/szdw/jsyjy/index.htm',
                'structures': {
                    'page_count':3,
                    'title_page_xpaths': ['//li/a[contains(text(), "副教授、副研究员")]/@href',
                        '//li/a[contains(text(), "中级职称")]/@href'],
                    'prefix_title_page': 'https://yyxy.nwsuaf.edu.cn/szdw/szdw/',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath':"//td//a[(starts-with(@href, 'https://yyxy.nwsuaf.edu.cn') or starts-with(@href, 'http://yyxy.nwsuaf.edu.cn'))]",
                    'name_xpath': ".//text()",
                    'url_xpath': ".//@href",
                    'prefix_url': '', # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
             'name': '动科学院',
             'url': 'https://dkxy.nwsuaf.edu.cn/szdw/jsyjy/index.htm',
             'structures': {
                 'page_count': 3,
                 'title_page_xpaths': ['//li/a[contains(text(), "副教授、副研究员")]/@href',
                                       '//li/a[contains(text(), "讲师")]/@href'],
                 'prefix_title_page': 'https://dkxy.nwsuaf.edu.cn/szdw/szdw/',  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': "//table/tbody/tr/td[1]/a",
                 'name_xpath': ".//text()",
                 'url_xpath': ".//@href",
                 'prefix_url':['https://dkxy.nwsuaf.edu.cn/szdw/jsyjy/','https://dkxy.nwsuaf.edu.cn/szdw/fjsfyjy/',
                               'https://dkxy.nwsuaf.edu.cn/szdw/js/'],  # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
             'name': '草业学院',
             'url': 'https://cga.nwsuaf.edu.cn/szdwB/jsyjyB/index.htm',
             'structures': {
                 'page_count': 3,
                 'title_page_xpaths': ['//li/a[contains(text(), "副教授、副研究员")]/@href',
                                       '//li/a[contains(text(), "讲师")]/@href'],
                 'prefix_title_page': ['https://cga.nwafu.edu.cn/szdwB/fjsfyjyB/',
                                       'https://cga.nwafu.edu.cn/szdwB/szdwB/'],  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': "//table/tbody/tr[position() > 1]/td[1]/a",
                 'name_xpath': ".//text()",
                 'url_xpath':".//@href",
                 'prefix_url':'',  # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
             'name': '动医学院',
             'url': 'https://dyxy.nwsuaf.edu.cn/szdw/jsyjy/index.htm',
             'structures': {
                 'page_count': 3,
                 'title_page_xpaths': ['//li/a[contains(text(), "副教授、副研究员")]/@href',
                                       '//li/a[contains(text(), "中级职称")]/@href'],
                 'prefix_title_page': 'https://dyxy.nwsuaf.edu.cn/szdw/szdw/',  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': "//table/tbody/tr[position() > 1]/td[1]/a",
                 'name_xpath': ".//text()",
                 'url_xpath': ".//@href",
                 'prefix_url':'',  # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
             'name': '信息学院',
             'url': 'https://cie.nwsuaf.edu.cn/szdw/js/index.htm',
             'structures': {
                 'page_count': 3,
                 'title_page_xpaths': None,
                 'prefix_title_page': None,  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': ["//h3[a/@title='正高级职称']/following-sibling::ul[1]/li/a",
                                            "//h3[a/@title='副高级职称']/following-sibling::ul[1]/li/a",
                                            "//h3[a/@title='中级职称']/following-sibling::ul[1]/li/a"],
                 'name_xpath': ".//text()",
                 'url_xpath': ".//@href",
                 'prefix_url':["https://cie.nwsuaf.edu.cn/szdw/js/",'https://cie.nwsuaf.edu.cn/szdw/szdw/','https://cie.nwsuaf.edu.cn/szdw/szdw/'],  # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -2# 默认值删去就好了
             },
         },
            {
             'name': '食品学院',
             'url': 'https://food.nwsuaf.edu.cn/szll/js/spkjx/index.htm',
             'structures': {
                 'page_count': 3,
                 'title_page_xpaths': ['//li/a[contains(text(), "食品安全系")]/@href',
                                       '//li/a[contains(text(), "食品营养系")]/@href'],
                 'prefix_title_page': 'https://food.nwsuaf.edu.cn/szll/js/js/',  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': ["//tbody/tr/td//a","//td//a[@rel='nofollow']","//td//a[@rel='nofollow']"],
                 'name_xpath': ".//text()",
                 'url_xpath': ".//@href",
                 'prefix_url':'',  # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
             'name': '葡萄酒学院',
             'url': 'https://wine.nwsuaf.edu.cn/szdw/bssds/index.htm',
             'structures': {
                 'page_count': 4,
                 'title_page_xpaths': ['//li/a[contains(text(), "副教授")]/@href',
                                       '//li/a[contains(text(), "青年副教授")]/@href',
                                       '//li/a[contains(text(), "讲师")]/@href'],
                 'prefix_title_page': 'https://wine.nwsuaf.edu.cn/szdw/szdw/',  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': "//td//a[contains(@rel, 'nofollow')]",
                 'name_xpath': ".//text()",
                 'url_xpath': ".//@href",
                 'prefix_url':'',  # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
             'name': '经管学院',
             'url': 'https://cem.nwsuaf.edu.cn/szdw/jsyjy/index.htm',
             'structures': {
                 'page_count': 3,
                 'title_page_xpaths': ['//li/a[contains(text(), "副教与副研")]/@href',
                                       '//li/a[contains(text(), "讲师与其他")]/@href',],
                 'prefix_title_page': 'https://cem.nwsuaf.edu.cn/szdw/szdw/',
                 'teacher_elements_xpath': ["//table/tbody/tr[position() > 1]/td[2]/a",
                                             "//table/tbody/tr[position() > 1]/td[2]/a",
                                            "//div[@class='cont']/p//a"],# 这其实也可以通过页面获得
                 'name_xpath': ".//text()",
                 'url_xpath': ".//@href",
                 'prefix_url': 'https://cem.nwsuaf.edu.cn/',  # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
                'name': '植保学院',
                'url': 'https://ppc.nwsuaf.edu.cn/szdw/kjdw/zwblx2022/index.htm',
                'structures': {
                    'page_count': 1,
                    'title_page_xpaths': '',
                    'prefix_title_page': '',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath': "//ul[@class='tabcontent'][position() <= 3]/li",
                    'name_xpath':".//h3/text()",
                    'url_xpath': "./@onclick",
                    'prefix_url': 'https://ppc.nwsuaf.edu.cn/szdw/kjdw/zwblx2022/',
                    # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
                'name': '理学院',
                'url': 'https://lxy.nwsuaf.edu.cn/szdw/wlxk/index.htm',
                'structures': {
                    'page_count': 3,
                    'title_page_xpaths': ['//li/a[contains(text(), "数学学科")]/@href',
                                          '//li/a[contains(text(), "气象学科")]/@href'],
                    'prefix_title_page': 'https://lxy.nwsuaf.edu.cn/szdw/szdw/',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath':"//table/tbody/tr/td",
                    'name_xpath': "./a/span/text() | ./a/text() | ./p/a/span/text() | ./p/a/text() | ./p/span/text() | ./span/text() | ./p/text()",
                    'url_xpath': "./a/@href | ./p/a/@href",
                    'prefix_url': '',
                    # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
                'name': '林学院',
                'url': 'https://cf.nwsuaf.edu.cn/xkjs/szdw/kjdw2/index.htm',
                'structures': {
                    'page_count': 1,
                    'title_page_xpaths': '',
                    'prefix_title_page': '',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath':"//table/tbody/tr[position() >= 2 and position() <= 29]/td[not(descendant::strong)]",
                    'name_xpath': "./a/descendant-or-self::span/text() | ./a/text() | ./p/a/descendant-or-self::span/text() | ./p/a/text() | ./span/descendant-or-self::span/text() | ./text()",
                    'url_xpath': "./a/@href | ./p/a/@href",
                    'prefix_url': '',
                    # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
             'name': '风景园林学院',
             'url': 'https://ylxy.nwsuaf.edu.cn/szdw/kjdw/index.htm',
             'structures': {
                 'page_count': 1,
                 'title_page_xpaths': '',
                 'prefix_title_page': '',  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': "//table/tbody/tr[position() >= 2 and position() <= 29]/td[not(descendant::strong)]",
                 'name_xpath':"./a/descendant-or-self::span/text() | ./a/text() | ./p/a/descendant-or-self::span/text() | ./p/a/text() | ./span/descendant-or-self::span/text() | ./text() | ./span/text()",
                 'url_xpath':"./a/@href | ./p/a/@href",
                 'prefix_url':  'https://ylxy.nwsuaf.edu.cn/szdw/kjdw/',
                 # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
                'name': '资环学院',
                'url': 'https://zhxy.nwsuaf.edu.cn/szdw/kjdw/index.htm',
                'structures': {
                    'page_count': 1,
                    'title_page_xpaths': [],
                    'prefix_title_page': '',  # 这其实也可以通过页面获得
                    'teacher_elements_xpath':"//table[position()<4]/tbody/tr/td[1]",
                    'name_xpath': ".//span[not(ancestor::strong)]/text()",
                    'url_xpath':  ".//a/@href",
                    'prefix_url': ['https://iipe.nwsuaf.edu.cn/szdw/'],
                    # prefix_url可能是当前页面的前缀，到时候再改一改
                    'id_path_index': -1  # 默认值删去就好了
                },
            },
            {
             'name': '水建学院',
             'url': 'https://sjxy.nwsuaf.edu.cn/szdwB/gjzcB/index.htm',
             'structures': {
                 'page_count': 3,
                 'title_page_xpaths': None,
                 'prefix_title_page': None,  # 这其实也可以通过页面获得
                 'teacher_elements_xpath':[ "/html/body/div[3]/div[3]/div/div[2]/p",
                                            "/html/body/div[3]/div[3]/div/div[2]//p//a",
                                            "/html/body/div[3]/div[3]/div/div[2]/p/a/span/span"],
                 'name_xpath':["./a/span/text() | ./a/text() | ./span/span/span/a/text() | ./a/span/text() | ./text() ",
                               './text()',
                               './text()'],
                 'url_xpath': [ "./a/@href | ./span/span/span/a/@href",
                                '@href',
                                '../../@href'],
                 'prefix_url':'',
                 # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
             'name': '机电学院',
             'url': 'https://cmee.nwsuaf.edu.cn/szdw/gjzcry/index.htm',
             'structures': {
                 'page_count': 1,
                 'title_page_xpaths': [],
                 'prefix_title_page': '',  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': "/html/body/div[3]/div[3]/div/div[2]//table//tbody//tr//td",
                 'name_xpath': ".//text()",
                 'url_xpath':".//a/@href",
                 'prefix_url':'',
                 # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
             'name': '化学与药学院',
             'url': 'https://hxyyxy.nwsuaf.edu.cn/szdwB/jsdwB/index.htm',
             'structures': {
                 'page_count': 1,
                 'title_page_xpaths': [],
                 'prefix_title_page': '',  # 这其实也可以通过页面获得
                 'teacher_elements_xpath':"/html/body/div[3]/div[3]/div/div[2]//table//tbody//tr//td[not(.//strong)]",
                 'name_xpath': ".//text()",
                 'url_xpath':".//a/@href",
                 'prefix_url':'',
                 # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
            {
             'name': '人文学院',
             'url': 'https://ch.nwsuaf.edu.cn/szdw/kjdw/index.htm',
             'structures': {
                 'page_count': 1,
                 'title_page_xpaths': [],
                 'prefix_title_page': '',  # 这其实也可以通过页面获得
                 'teacher_elements_xpath': "//div/dl/dd/div/div/table/tbody/tr/td/a/span",
                 'name_xpath': ".//text()",
                 'url_xpath':"./../@href",
                 'prefix_url': '',
                 # prefix_url可能是当前页面的前缀，到时候再改一改
                 'id_path_index': -1  # 默认值删去就好了
             },
         },
# ... 更多学院
        ]
}
