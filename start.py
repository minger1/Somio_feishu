import os
import sys

os.environ['NO_PROXY'] = 'open.feishu.cn'

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("警告: 找不到 python-dotenv，尝试使用现有的环境变量。建议运行 pip install python-dotenv")

import server

if __name__ == '__main__':
    # 启动 WebSocket 阻塞挂起主线程
    server.start_ws()
