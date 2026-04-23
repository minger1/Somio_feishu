import time
import threading
import random
from datetime import datetime


# ==================== 生成未注册邮箱 ====================

def generate_email():
    """
    生成未注册邮箱：test + 年月日时分秒毫秒 + @qq.com
    例如：test202602261456123@qq.com
    """
    now = datetime.now()
    date_part = now.strftime("%Y%m%d%H%M%S")
    ms_part = f"{now.microsecond // 1000:03d}"
    timestamp = date_part + ms_part
    return f"ljkjtest{timestamp}@qq.com"


# ==================== 歌名生成 ====================



def get_song() -> str:
    """
    生成测试歌名，格式: TEST-[16位十六进制时间戳]
    例如: TEST-018f3a7c2d4e9b01
    纳秒级时间戳保证多进程并发唯一性。
    """
    return f"TEST-{time.time_ns():016x}"