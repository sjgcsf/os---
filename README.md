```markdown
# Faculty Information Scraper

本项目旨在爬取各大学校的教师信息，并将数据存储到本地的 MongoDB 数据库中。目前，该项目已在 Windows 环境下的 PyCharm 中成功运行，并计划将其打包为 Docker 镜像，以便在 CentOS 7 系统上运行。

## 项目结构

```plaintext
faculty_info/
│   Dockerfile
│   requirements.txt
│   main.py
│   .env
│
├───scrapers/
│   │   scraper.py
│   │   csu_scraper.py
│   │   ...
│   │   __init__.py
│
├───configs/
│   │   nwafu_university_config.py
│   │   thu_university_config.py
│   │   __init__.py
│
├───database_handler/
│   │   database_handler.py
│   │   __init__.py
│
└───scripts/
    │   start.sh
```

## 主要组件

1. `main.py`: 主执行文件。
2. `scrapers` 文件夹: 包含所有的爬虫类。`scraper.py` 包含 `Scraper` 类，作为其他具体学校爬虫类的父类。每个学校的爬虫类都在单独的 Python 文件中定义，例如 `CSUScraper` 类在 `csu_scraper.py` 中定义。
3. `database_handler.py`: 包含 `DatabaseHandler` 类，用于与 MongoDB 数据库进行交互。
4. `configs` 文件夹: 存放特定学校的教师信息配置文件，例如 `nwafu_university_config.py` 和 `thu_university_config.py`。

## 如何运行

在 Windows 环境下

1.使用 PyCharm 打开项目，并确保所有依赖都已正确安装。运行 `main.py` 即可启动项目。

2.windows下启动虚拟环境运行项目，举例：
`C:\Users\HRR> conda activate faculty_info`

`(faculty_info) C:\Users\HRR>cd C:\Users\HRR\Desktop\faculty_info`

`(faculty_info) C:\Users\HRR\Desktop\faculty_info>pip install -r requirements.txt`

`(faculty_info) C:\Users\HRR\Desktop\faculty_info>python main.py`

## Docker 部署

该项目计划在 CentOS 7 系统上通过 Docker 运行。更多关于如何将项目打包为 Docker 镜像并运行的详细信息将在后续文档中提供。



## 配置文件 `.env`

为了运行这个项目，需要在项目的根目录下创建一个 `.env` 文件，并在其中设置一些环境变量。这里是一些必要的配置项及其说明：

- 数据库配置：请确保在 `.env` 文件中正确配置了 MongoDB 的连接字符串。
- `DRIVER_PATH`: ChromeDriver 的路径。这是 Selenium 用来控制 Chrome 浏览器进行自动化操作的。例如：`C:/ProgramData/Anaconda3/chromedriver.exe`
- `USER_AGENT`: 用于在 HTTP 请求的 `User-Agent` 头中设置的字符串。它可以帮助你伪装你的爬虫，使其看起来像一个正常的浏览器。例如：`Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36`

这里是一个 `.env` 文件的示例：

```plaintext
DRIVER_PATH=C:/ProgramData/Anaconda3/chromedriver.exe
DB_HOST=localhost
DB_PORT=27017
DB_NAME=faculty_db
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36
```

## 联系方式

如果你有任何问题或建议，请联系我们。

[]

---

