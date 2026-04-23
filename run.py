import sys
import argparse
import pytest
import os
from datetime import datetime

def run_tests():
    """
    运行测试套件，支持并发执行。
    """
    parser = argparse.ArgumentParser(description="运行 Playwright 测试")
    parser.add_argument("-n", "--workers", type=str, default="1", help="并发运行的 worker 数量，例如 2 或 auto")
    parser.add_argument("-k", "--filter", type=str, default="", help="可选：按名称过滤测试用例")
    args_parsed, extra_args = parser.parse_known_args()

    report_dir = "report"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"report_{timestamp}.html")
    
    # 基础运行命令
    pytest_args = [
        "-v",
        f"-n={args_parsed.workers}",  # 并发核心数
        "--dist=load",              # 改为 load，允许同一个文件内的用例分发给多个 worker，loadfile：按文件分配，保证同一个文件内的用例在同一个 worker（可选）
        "testcase/test_text_create_song.py::TestTextCreateSong::test_text_mode_v5_5", # 恢复运行整个文件以展示并发优势
        f"--html={report_file}",
        "--self-contained-html",
    ]

    if args_parsed.filter:
        pytest_args.extend(["-k", args_parsed.filter])

    # 如果有其他透传参数，也加上
    pytest_args.extend(extra_args)
    
    print(f"正在启动测试 (Workers: {args_parsed.workers})，报告将保存至: {report_file}")
    
    import threading
    import time

    def tail_logs(stop_event):
        log_dir = "logs"
        ts = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"info_{ts}.log")
        
        while not os.path.exists(log_file) and not stop_event.is_set():
            time.sleep(0.1)
            
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                f.seek(0, 2) # 只看本次运行的新日志
                while not stop_event.is_set():
                    where = f.tell()
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        f.seek(where)
                    else:
                        try:
                            # 绕过 pytest 主进程捕获，强制输出到真实终端
                            sys.__stdout__.write(line)
                            sys.__stdout__.flush()
                        except:
                            pass

    stop_event = threading.Event()
    t = threading.Thread(target=tail_logs, args=(stop_event,), daemon=True)
    t.start()

    try:
        pytest.main(pytest_args)
    finally:
        stop_event.set()
        t.join(timeout=1.0)

if __name__ == "__main__":
    run_tests()
