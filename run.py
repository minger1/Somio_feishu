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
    parser.add_argument("-n", "--workers", type=str, default="3", help="并发运行的 worker 数量，例如 2 或 auto")
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
        "testcase/test_text_create_song.py", # 恢复运行整个文件以展示并发优势
        f"--html={report_file}",
        "--self-contained-html",
    ]

    if args_parsed.filter:
        pytest_args.extend(["-k", args_parsed.filter])

    # 如果有其他透传参数，也加上
    pytest_args.extend(extra_args)
    
    print(f"正在启动测试 (Workers: {args_parsed.workers})，报告将保存至: {report_file}")
    pytest.main(pytest_args)

if __name__ == "__main__":
    run_tests()
