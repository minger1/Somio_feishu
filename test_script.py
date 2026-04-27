import sys
import subprocess
import os

def main():
    print("开始执行核心用例...", flush=True)
    # 当前文件所在的目录
    cwd = os.path.dirname(os.path.abspath(__file__))
    cmd = [
        "pytest", 
        "testcase/test_text_create_song.py", 
        "testcase/test_lyrics_create_song.py",
        "-n", "3",
        "--tb=short",
        "-v"
    ]
    # 确保运行开始前删除上一次的遗留报告文件
    report_file = os.path.join(cwd, "test_results.jsonl")
    if os.path.exists(report_file):
        try:
            os.remove(report_file)
        except OSError:
            pass
            
    result = subprocess.run(cmd, cwd=cwd)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
