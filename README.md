# Somio Playwright Test Framework

这是一个基于 Playwright 和 Pytest 构建的标准 Web 自动化测试框架。它使用了 Page Object Model (POM) 设计模式，结合 Allure 报告用于执行和管理自动化用例。

## 目录结构
```text
Somio_PlayWright/
├── config/              # 配置文件目录
│   ├── settings.py      # 项目的环境变量和基础配置 (例如邮箱, 环境域名)
│   ├── locators.py      # 元素定位器统一存放点
│   └── __init__.py 
├── data/                # 测试数据目录
│   ├── test_data.py     # 独立抽落的测试数据 (例如固定的测试歌词文案等)
│   └── __init__.py 
├── pages/               # Page Object Model (各个页面的操作封装)
├── testcase/            # 所有的 Pytest 测试用例
├── utils/               # 公共工具类代码 (如日志封装 logger.py, 生成随机邮箱等)
├── logs/                # 自动化运行日志存放录
├── report/              # HTML 或 Allure 测试报告存放目录
├── conftest.py          # Pytest 全局 fixture 夹具配置
├── pytest.ini           # Pytest 的基础和命令行默认配置
├── requirements.txt     # 项目 Python 依赖库
└── run.py               # 快捷运行脚本支持多线程
```

## 快速开始

### 1. 安装依赖
请确保本地环境安装了 Python 3.8+，然后安装依赖库：
```bash
pip install -r requirements.txt
playwright install
```

### 2. 运行测试
您可以使用内置的 `run.py` 脚本统一执行，这会自动开启并发并生成 HTML 报告。
```bash
python run.py --workers 2
```

或者使用标准的 pytest 命令单文件运行：
```bash
pytest testcase/test_login.py -v
```

## 测试数据与配置
- 如果需要修改基础的测试网站环境，请访问并修改 `config/settings.py`
- 如果需要修改具体的长文案、测试预期的歌词文案，请修改 `data/test_data.py`
- 所有页面的元素配置请不要硬编码在 pages 文件夹里，统一步伐到 `config/locators.py`
