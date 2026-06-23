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
    return f"testljkj{timestamp}@qq.com"


# ==================== 歌名生成 ====================



def get_song(prefix: str = "TEST", model: str = "") -> str:
    """
    生成测试歌名，格式: [PREFIX]-[MODEL]-[16位十六进制时间戳]
    例如: TEXT-V5-018f3a7c2d4e9b01
    
    * 使用 16位十六进制纳秒级时间戳 保证多进程/高并发时的绝对唯一性。
    """
    timestamp = f"{time.time_ns():016x}"
    
    parts = []
    if prefix:
        parts.append(prefix.upper())
    if model:
        # 将 '+' 替换为 '_PLUS'，将 '.' 替换为 '_'，并转为大写
        clean_model = model.replace("+", "_PLUS").replace(".", "_").upper()
        parts.append(clean_model)
    parts.append(timestamp)
    
    return "-".join(parts)