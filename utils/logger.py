import sys
import logging
from pathlib import Path
from loguru import logger

# ============== 配置日志 ============== #
# 日志存放目录
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 基础日志文件名
INFO_LOG = LOG_DIR / "info_{time:YYYY-MM-DD}.log"
ERROR_LOG = LOG_DIR / "error_{time:YYYY-MM-DD}.log"

# 定义日志输出格式
FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 移除默认的控制台输出
logger.remove()

# 将 loguru 日志重定向到标准 logging，以便 pytest 捕获并显示在报告中
def sink_to_logging(message):
    record = message.record
    level_name = record["level"].name
    level = logging.getLevelName(level_name)
    if not isinstance(level, int):
        level = logging.INFO
    logging.getLogger("loguru").log(level, record["message"])

logger.add(sink_to_logging, level="INFO", enqueue=True)

# 添加控制台输出 (让 pytest 能够捕获并在必要时进行输出)
logger.add(
    sys.stdout,
    format=FORMAT,
    level="INFO",
    colorize=True, # 开启彩色高亮日志等级
    enqueue=True,   # 确保多进程并发时文本不乱串
)

# 添加 INFO 级别到文件 (每日轮转，保留 7 天)
logger.add(
    str(INFO_LOG),
    format=FORMAT,
    level="INFO",
    rotation="00:00",
    retention="7 days",
    encoding="utf-8",
    enqueue=True,
)

# 专门错误日志的文件 (保留 30 天)
logger.add(
    str(ERROR_LOG),
    format=FORMAT,
    level="ERROR",
    rotation="00:00",
    retention="30 days",
    encoding="utf-8",
    enqueue=True,
)
