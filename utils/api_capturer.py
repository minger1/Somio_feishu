import json
import os
import re
from playwright.sync_api import Response, Page
from utils.logger import logger

class APICapturer:
    """核心 API 捕获器，使用 Playwright 的事件监听来捕获接口传参与响应"""
    def __init__(self, page: Page, test_name: str, version: str = "v1.0.0", target_patterns=None):
        self.page = page
        self.test_name = test_name
        self.version = version
        # 优先从项目根目录的已知接口数据文档中加载白名单，实现数据与代码逻辑的顶级解耦
        patterns_file = os.path.join("data", "api_patterns.txt")
        default_patterns = []
        if os.path.exists(patterns_file):
            try:
                with open(patterns_file, "r", encoding="utf-8") as f:
                    default_patterns = [
                        line.strip() 
                        for line in f 
                        if line.strip() and not line.strip().startswith("#")
                    ]
            except Exception as e:
                logger.error(f"[APICapturer] 解析 {patterns_file} 失败: {e}")
                
        if not default_patterns:
            try:
                from config.settings import API_CAPTURE_PATTERNS
                default_patterns = API_CAPTURE_PATTERNS
            except Exception:
                default_patterns = [r"/api/", r"/auth/", r"/login", r"/register"]
            
        self.target_patterns = target_patterns or default_patterns
        self.captured_apis = []
        
        # 注册 Playwright 响应事件监听
        self.page.on("response", self._handle_response)

    def _should_capture(self, url: str) -> bool:
        """根据正则匹配过滤是否是我们需要截获的主要接口"""
        return any(re.search(pattern, url, re.IGNORECASE) for pattern in self.target_patterns)

    def _handle_response(self, response: Response):
        url = response.url
        if not self._should_capture(url):
            return

        request = response.request
        
        # 提取 URL 的纯路径（不含 Query 参数和域名），方便进行接口去重分析
        from urllib.parse import urlparse
        try:
            parsed_url = urlparse(url)
            path_key = parsed_url.path
        except Exception:
            path_key = url

        # 1. 智能识别轮询接口并进行频次限制（过滤高频轮询噪音）
        polling_keywords = ["getUserInfo", "generateList", "checkStatus", "polling"]
        is_polling = any(kw in path_key for kw in polling_keywords)
        
        if is_polling:
            if not hasattr(self, "_polling_counts"):
                self._polling_counts = {}
            # 统计当前 Path 已经被拦截的次数
            current_count = self._polling_counts.get(path_key, 0)
            if current_count >= 2:
                # 轮询接口最多只保留前 2 次抓取（起步与最终状态验证），后续直接过滤
                return
            self._polling_counts[path_key] = current_count + 1

        # 2. 提取请求入参
        req_payload = None
        if request.post_data:
            try:
                req_payload = request.post_data_json
            except Exception:
                # 如果不是 JSON，尝试保存为原始文本
                req_payload = request.post_data

        # 3. 提取响应出参
        res_data = None
        if response.status >= 200 and response.status < 300:
            try:
                res_data = response.json()
            except Exception:
                try:
                    res_data = response.text()
                except Exception:
                    res_data = "[Unresolvable Response Body]"
        else:
            res_data = f"[HTTP Error Status: {response.status}]"

        # 特殊处理：针对生成音乐列表接口进行截断限制，防止用户数据过多导致快照文件过大
        if "web/music/generateList" in url:
            try:
                if isinstance(res_data, (dict, list)):
                    formatted_str = json.dumps(res_data, ensure_ascii=False, indent=2)
                else:
                    formatted_str = str(res_data)
                
                lines = formatted_str.splitlines()
                if len(lines) > 200:
                    res_data = "\n".join(lines[:200]) + "\n..."
            except Exception as e:
                logger.error(f"[APICapturer] 截断接口响应失败: {e}")

        # 4. 全局响应体一致性去重：如果出参与上一次完全相同，说明无状态变化，直接滤除
        if not hasattr(self, "_last_responses"):
            self._last_responses = {}
        
        resp_key = f"{request.method}:{path_key}"
        try:
            serialized_res = json.dumps(res_data, sort_keys=True, ensure_ascii=False)
        except Exception:
            serialized_res = str(res_data)
            
        if resp_key in self._last_responses and self._last_responses[resp_key] == serialized_res:
            # 响应内容完全没有变化，过滤重复噪音
            return
            
        self._last_responses[resp_key] = serialized_res

        captured_item = {
            "url": url,
            "method": request.method,
            "status": response.status,
            "request_headers": request.headers,
            "request_payload": req_payload,
            "response_body": res_data
        }
        self.captured_apis.append(captured_item)

    def save_snapshot(self, output_dir: str = "report/api_snapshots") -> str:
        """将捕获到的所有 API 序列化保存为 JSON 文件"""
        # 静默等待 500 毫秒，允许 Playwright 处理完事件循环中所有待处理的响应事件
        try:
            self.page.wait_for_timeout(500)
        except Exception:
            pass

        # 注销监听，防止后续页面行为继续触发捕获
        try:
            self.page.remove_listener("response", self._handle_response)
        except Exception:
            pass

        if not self.captured_apis:
            return None
        
        # 确保归档文件夹存在
        os.makedirs(output_dir, exist_ok=True)
        
        import datetime
        import time
        
        run_timestamp = os.environ.get("API_CAPTURE_RUN_TIMESTAMP")
        is_suite_run = bool(run_timestamp)
        
        if is_suite_run:
            file_name = f"test_api_data_{run_timestamp}.json"
        else:
            # 独立调试，生成自身专属时间戳
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]
            file_name = f"test_api_data_{self.test_name}_{timestamp}.json"
            
        file_path = os.path.join(output_dir, file_name)
        
        # 标注每一个 API 的来源用例名称
        for api in self.captured_apis:
            api["test_case"] = self.test_name

        if is_suite_run:
            # 采用进程安全的原子锁机制追加写入
            lock_dir = file_path + ".lock"
            for _ in range(100):  # 最多重试 100 次，确保并发不冲突
                try:
                    os.mkdir(lock_dir)  # 原子锁
                    try:
                        snapshot_data = {"captured_at": "", "apis": []}
                        if os.path.exists(file_path):
                            with open(file_path, "r", encoding="utf-8") as f:
                                snapshot_data = json.load(f)
                        
                        # 初始化页面加载时的常用公共接口，一次测试套件运行中只捕获一次
                        INIT_API_KEYWORDS = ["generateList", "current", "activityPopup/check", "getUserInfo"]
                        
                        from urllib.parse import urlparse
                        def get_url_path(url_str: str) -> str:
                            try:
                                return urlparse(url_str).path
                            except Exception:
                                return url_str
                                
                        def is_init_api(url_str: str) -> bool:
                            return any(kw in url_str for kw in INIT_API_KEYWORDS)
                            
                        # 过滤掉已存在于整个套件运行快照中的公共初始化接口
                        existing_init_paths = set()
                        for api in snapshot_data["apis"]:
                            api_url = api.get("url", "")
                            if is_init_api(api_url):
                                path = get_url_path(api_url)
                                existing_init_paths.add((api.get("method", ""), path))
                                
                        apis_to_append = []
                        for api in self.captured_apis:
                            api_url = api.get("url", "")
                            method = api.get("method", "")
                            if is_init_api(api_url):
                                path = get_url_path(api_url)
                                if (method, path) in existing_init_paths:
                                    continue
                                existing_init_paths.add((method, path))
                            apis_to_append.append(api)
                        
                        snapshot_data["apis"].extend(apis_to_append)
                        if not snapshot_data["captured_at"]:
                            snapshot_data["captured_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(snapshot_data, f, ensure_ascii=False, indent=2)
                    finally:
                        try:
                            os.rmdir(lock_dir)
                        except:
                            pass
                    break
                except FileExistsError:
                    time.sleep(0.05)
                except Exception as e:
                    logger.error(f"[APICapturer] 写入进程锁文件失败: {e}")
                    time.sleep(0.05)
        else:
            # 独立运行，直接保存，剔除外层冗余 test_case 字段
            snapshot_data = {
                "captured_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "apis": self.captured_apis
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(snapshot_data, f, ensure_ascii=False, indent=2)

        return file_path


class api_capture:
    """
    优雅的上下文管理器，方便通过 `with` 语法来控制捕获生命周期：
    
    with api_capture(page, "test_case_name"):
        # 执行您的页面操作
        login_page.login(email, pwd)
    # 离开代码块时自动保存 API 数据落盘
    """
    def __init__(self, page: Page, test_name: str, version: str = "v1.0.0", target_patterns=None, output_dir: str = "report/api_snapshots"):
        self.page = page
        self.test_name = test_name
        self.version = version
        self.target_patterns = target_patterns
        self.output_dir = output_dir
        self.capturer = None

    def __enter__(self):
        # 检查是否启用了接口数据拦截与对比
        from config.settings import GENERATE_API_COMPARE
        env_val = os.environ.get("GENERATE_API_COMPARE")
        should_capture = True
        if env_val is not None:
            should_capture = (env_val == "1")
        else:
            should_capture = GENERATE_API_COMPARE

        if not should_capture:
            return None

        self.capturer = APICapturer(
            page=self.page, 
            test_name=self.test_name, 
            version=self.version, 
            target_patterns=self.target_patterns
        )
        return self.capturer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.capturer:
            current_path = self.capturer.save_snapshot(output_dir=self.output_dir)
            # 只有在非 Suite 运行模式下（也就是独立单跑某个用例），才在 __exit__ 时自动对比生成
            # 如果是 Suite 运行模式，将在 run.py 最终全局生成，此处不生成
            if current_path and not os.environ.get("API_CAPTURE_RUN_TIMESTAMP"):
                import glob
                from .api_diff_reporter import generate_visual_diff
                
                # 获取目录下属于当前用例的时间戳抓取文件并排序
                search_pattern = os.path.join(self.output_dir, f"test_api_data_{self.test_name}_*.json")
                snapshot_files = glob.glob(search_pattern)
                snapshot_files.sort()  # 排序后，最后一项是本次运行，倒数第二项是上一次运行
                
                if len(snapshot_files) >= 2:
                    previous_path = snapshot_files[-2]
                    latest_path = snapshot_files[-1]
                    
                    import datetime
                    report_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    report_path = os.path.join("report/api_diff_reports", f"api_diff_{self.test_name}_{report_time}.html")
                    generate_visual_diff(previous_path, latest_path, report_path)
                else:
                    pass
