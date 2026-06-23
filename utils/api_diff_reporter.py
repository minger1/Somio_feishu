import os
import json
import difflib
from utils.logger import logger

def mask_tokens(obj):
    """
    直接返回原始数据，不进行任何 Token 信息的遮掩或屏蔽，真实显示完整 Token 数值。
    """
    return obj

def to_pretty_json_lines(obj) -> list:
    """
    屏蔽 token 后，将对象转换为漂亮格式化的按行排列字符串列表
    """
    if obj is None:
        return ["{}"]
    masked_obj = mask_tokens(obj)
    if isinstance(masked_obj, str):
        return masked_obj.splitlines()
    return json.dumps(masked_obj, ensure_ascii=False, indent=2).splitlines()

def generate_visual_diff(baseline_path: str, current_path: str, report_path: str = "report/api_diff_reports/api_diff_report.html") -> bool:
    """
    读取两份 JSON 快照，生成经过智能接口对齐、Token 过滤、高颜值的局部比对报告。
    """
    if not os.path.exists(baseline_path):
        logger.error(f"[DiffReporter] 未找到上一次接口文件: {baseline_path}")
        return False
    if not os.path.exists(current_path):
        logger.error(f"[DiffReporter] 未找到本次最新捕获文件: {current_path}")
        return False

    # 1. 加载两次捕获的完整 JSON 对象
    try:
        with open(baseline_path, "r", encoding="utf-8") as f:
            baseline_data = json.load(f)
        with open(current_path, "r", encoding="utf-8") as f:
            current_data = json.load(f)
    except Exception as e:
        logger.error(f"[DiffReporter] 解析 JSON 失败: {e}")
        return False

    # 2. 提取公共元数据与动态用例识别
    apis_baseline = baseline_data.get("apis", [])
    apis_current = current_data.get("apis", [])

    # 动态分析内层每个接口属于哪一个用例，以此智能断定是否是合并套件运行
    unique_cases = set(api.get("test_case") for api in apis_current if api and api.get("test_case"))
    if len(unique_cases) == 1:
        test_case = list(unique_cases)[0]
    elif len(unique_cases) > 1:
        test_case = "Combined Suite Run"
    else:
        test_case = "Unknown TestCase"

    prev_time = baseline_data.get("captured_at", "N/A")
    curr_time = current_data.get("captured_at", "N/A")

    if test_case == "Combined Suite Run":
        test_case_item_html = ""
    else:
        test_case_item_html = f"""
                    <div class="overview-item">
                        <div class="overview-label">测试用例名称 (Test Case)</div>
                        <div class="overview-val">{test_case}</div>
                    </div>
        """

    # 3. 智能对齐对策：利用 (test_case, method, normalized_url, occurrence_index) 作为键对齐接口列表，杜绝跨用例错位比对
    # 去除 query 参数进行对齐，防止动态参数（如 visitor_id）干扰接口匹配
    def align_apis(api_list, fallback_test_case):
        mapped = {}
        counts = {}
        for api in api_list:
            if not api:
                continue
            tc = api.get("test_case", fallback_test_case)
            m = api.get("method", "UNKNOWN")
            u = api.get("url", "UNKNOWN")
            
            from urllib.parse import urlparse
            try:
                parsed_url = urlparse(u)
                normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            except Exception:
                normalized_url = u

            key_base = (tc, m, normalized_url)
            counts[key_base] = counts.get(key_base, 0) + 1
            key = (tc, m, normalized_url, counts[key_base])
            mapped[key] = api
        return mapped

    mapped_base = align_apis(apis_baseline, baseline_data.get("test_case", "Baseline TestCase"))
    mapped_curr = align_apis(apis_current, test_case)

    # 抓取并集所有的键，保证顺序（先上一次的，再新增的）
    all_keys = list(mapped_base.keys())
    for k in mapped_curr.keys():
        if k not in all_keys:
            all_keys.append(k)

    differ = difflib.HtmlDiff(wrapcolumn=65)
    
    from collections import defaultdict
    case_to_cards = defaultdict(list)
    case_order = []

    for idx, key in enumerate(all_keys, start=1):
        tc, method, normalized_url, occurrence = key
        if tc not in case_order:
            case_order.append(tc)
            
        api_base = mapped_base.get(key)
        api_curr = mapped_curr.get(key)

        # 获取实际用来显示的完整 URL（带 Query 参数，优先用当前的，其次用基准的）
        display_url = ""
        if api_curr:
            display_url = api_curr.get("url", normalized_url)
        elif api_base:
            display_url = api_base.get("url", normalized_url)
        else:
            display_url = normalized_url

        # 状态分析：持续请求、新增请求、缺失请求
        if api_base and api_curr:
            state_badge = '<span class="badge state-active">🔄 持续校验 (ACTIVE)</span>'
            status = api_curr.get("status", 200)
            headers_base = api_base.get("request_headers")
            headers_curr = api_curr.get("request_headers")
            req_base = api_base.get("request_payload")
            req_curr = api_curr.get("request_payload")
            res_base = api_base.get("response_body")
            res_curr = api_curr.get("response_body")
        elif api_base and not api_curr:
            # 缺失/未请求情况
            state_badge = '<span class="badge state-missing">⚠️ 缺失/未请求 (MISSING)</span>'
            status = api_base.get("status", "N/A")
            headers_base = api_base.get("request_headers")
            headers_curr = None
            req_base = api_base.get("request_payload")
            req_curr = None  # 右边变空，全红高亮
            res_base = api_base.get("response_body")
            res_curr = None  # 右边变空，全红高亮
        else:
            # 新增请求情况
            state_badge = '<span class="badge state-new">✨ 新增请求 (NEW)</span>'
            status = api_curr.get("status", 200)
            headers_base = None
            headers_curr = api_curr.get("request_headers")
            req_base = None  # 左边为空，全绿高亮
            req_curr = api_curr.get("request_payload")
            res_base = None  # 左边为空，全绿高亮
            res_curr = api_curr.get("response_body")

        # 将请求头、传参和回包进行 pretty print
        headers_base_lines = to_pretty_json_lines(headers_base)
        headers_curr_lines = to_pretty_json_lines(headers_curr)
        req_base_lines = to_pretty_json_lines(req_base)
        req_curr_lines = to_pretty_json_lines(req_curr)
        res_base_lines = to_pretty_json_lines(res_base)
        res_curr_lines = to_pretty_json_lines(res_curr)

        # 局部渲染比对表格
        headers_table = differ.make_table(headers_base_lines, headers_curr_lines, context=False)
        req_table = differ.make_table(req_base_lines, req_curr_lines, context=False)
        res_table = differ.make_table(res_base_lines, res_curr_lines, context=False)

        # 配色设置
        badge_class = f"badge-{method.lower()}"
        
        card_html = f"""
        <div class="api-card">
            <!-- 接口基本信息区 -->
            <div class="api-card-header">
                <span class="badge {badge_class}">{method}</span>
                <span class="api-url">{display_url}</span>
                {state_badge}
                <span class="badge badge-status">HTTP {status}</span>
            </div>
            
            <div class="api-card-body">
                <!-- 请求头区域 -->
                <div class="section-container">
                    <h3 class="section-title">
                        <span class="section-icon">🔑</span> 请求头比对 (Request Headers)
                    </h3>
                    <div class="diff-table-wrapper">
                        {headers_table}
                    </div>
                </div>

                <!-- 传参区域 -->
                <div class="section-container">
                    <h3 class="section-title">
                        <span class="section-icon">📥</span> 传参比对 (Request Payload)
                    </h3>
                    <div class="diff-table-wrapper">
                        {req_table}
                    </div>
                </div>

                <!-- 入参/回包区域 -->
                <div class="section-container">
                    <h3 class="section-title">
                        <span class="section-icon">📤</span> 入参/回包比对 (Response Body)
                    </h3>
                    <div class="diff-table-wrapper">
                        {res_table}
                    </div>
                </div>
            </div>
        </div>
        """
        case_to_cards[tc].append(card_html)

    # 4. 按用例出现的天然顺序，将同一用例的所有接口卡片完美包裹并进行章节大标题聚类
    api_cards_html = ""
    for tc in case_order:
        cards = case_to_cards[tc]
        api_cards_html += f"""
        <div class="case-section">
            <h2 class="case-title">
                <span class="case-icon">📋</span> 用例：{tc}
            </h2>
            <div class="case-cards-container">
                {"".join(cards)}
            </div>
        </div>
        """

    # 4. 生成超豪华视觉设计的整体大报告模板
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>API Contract Diff Report</title>
        <style type="text/css">
            body {{ 
                font-family: 'Outfit', 'Inter', -apple-system, sans-serif; 
                margin: 0; 
                padding: 40px 20px; 
                background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                min-height: 100vh;
                color: #1f2937;
            }}
            .container {{
                max-width: 1500px;
                margin: 0 auto;
            }}
            
            /* 概览卡片 */
            .overview-card {{
                background: #ffffff;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.05);
                padding: 24px 30px;
                margin-bottom: 40px;
                border-left: 6px solid #6366f1;
            }}
            .overview-title {{
                margin: 0 0 15px 0;
                font-size: 22px;
                color: #111827;
                font-weight: 700;
            }}
            .overview-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
            }}
            .overview-item {{
                background: #f9fafb;
                padding: 12px 18px;
                border-radius: 8px;
                border: 1px solid #f3f4f6;
            }}
            .overview-label {{
                font-size: 12px;
                color: #6b7280;
                margin-bottom: 4px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .overview-val {{
                font-size: 15px;
                font-weight: 600;
                color: #374151;
            }}

            /* 用例大标题章节样式 */
            .case-section {{
                margin-top: 50px;
                margin-bottom: 30px;
            }}
            .case-title {{
                font-size: 22px;
                color: #1f2937;
                font-weight: 800;
                padding-bottom: 12px;
                border-bottom: 3px solid #6366f1;
                margin-bottom: 24px;
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .case-icon {{
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
                color: #ffffff;
                width: 32px;
                height: 32px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                box-shadow: 0 4px 10px rgba(99,102,241,0.35);
            }}

            /* 接口主卡片 */
            .api-card {{
                background: #ffffff;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.04);
                margin-bottom: 50px; /* 每个接口间有明显的间隔 */
                border: 1px solid rgba(0,0,0,0.02);
                overflow: hidden;
            }}
            
            /* 接口头部明显标识 (升级为高贵的浅清蓝) */
            .api-card-header {{
                background: #e0f2fe; /* 清新浅蓝色 */
                border-bottom: 2px solid #bae6fd; /* 浅蓝分界线 */
                padding: 16px 24px;
                display: flex;
                align-items: center;
                gap: 15px;
                color: #1e3a8a;
            }}
            .api-url {{
                font-family: 'Consolas', monospace;
                font-size: 14px;
                font-weight: bold;
                color: #0369a1; /* 深邃海蓝色 */
                flex-grow: 1;
                word-break: break-all;
            }}
            
            /* 方法类型徽章 */
            .badge {{
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1px;
                text-transform: uppercase;
                white-space: nowrap;
            }}
            .badge-post {{
                background-color: #0284c7; /* 经典深天蓝 */
                color: #ffffff;
            }}
            .badge-get {{
                background-color: #0d9488; /* 典雅青绿色 */
                color: #ffffff;
            }}
            .badge-put {{
                background-color: #d97706;
                color: #ffffff;
            }}
            .badge-delete {{
                background-color: #dc2626;
                color: #ffffff;
            }}
            .badge-status {{
                background-color: #f1f5f9; /* 柔和白灰 */
                color: #475569; /* 中性深灰字 */
                border: 1px solid #cbd5e1;
            }}
            
            /* 请求状态标志 */
            .state-active {{
                background-color: rgba(99, 102, 241, 0.15);
                color: #4f46e5;
                border: 1px solid rgba(99, 102, 241, 0.3);
            }}
            .state-new {{
                background-color: rgba(16, 185, 129, 0.15);
                color: #059669;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }}
            .state-missing {{
                background-color: rgba(239, 68, 68, 0.15);
                color: #dc2626;
                border: 1px solid rgba(239, 68, 68, 0.3);
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.6; }}
                100% {{ opacity: 1; }}
            }}
            
            /* 接口内部明显区域划分 */
            .api-card-body {{
                padding: 30px;
                background-color: #ffffff;
            }}
            .section-container {{
                margin-bottom: 30px; /* 传参和入参明显的区域区隔 */
            }}
            .section-container:last-child {{
                margin-bottom: 0;
            }}
            .section-title {{
                font-size: 16px;
                font-weight: bold;
                color: #374151;
                margin: 0 0 15px 0;
                padding-bottom: 8px;
                border-bottom: 2px solid #f3f4f6;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            /* 局部 difflib 对比表格美化 */
            .diff-table-wrapper {{
                border-radius: 8px;
                overflow: hidden;
                border: 1px solid #e5e7eb;
            }}
            table.diff {{ 
                border-collapse: collapse; 
                border: none; 
                width: 100%; 
                background-color: #ffffff; 
            }}
            table.diff td {{ 
                font-family: 'Fira Code', 'Consolas', 'Courier New', monospace; 
                font-size: 13px; 
                padding: 4px 10px; 
                line-height: 1.4;
            }}
            th.diff_header, td.diff_header {{ 
                background-color: #f9fafb; 
                text-align: right; 
                color: #9ca3af; 
                font-weight: 500; 
                width: 40px; 
                border-right: 1px solid #e5e7eb; 
                user-select: none;
                padding-right: 8px !important;
            }}
            .diff_next {{ display: none; }} /* 隐藏跳转链接 */
            
            /* 柔和、辨识度极高的修改高亮 */
            .diff_add {{ background-color: #d1fae5 !important; color: #065f46; font-weight: bold; }} /* 新增标绿 */
            .diff_chg {{ background-color: #fef3c7 !important; color: #92400e; font-weight: bold; }} /* 修改标黄 */
            .diff_sub {{ background-color: #fee2e2 !important; color: #991b1b; font-weight: bold; }} /* 删除标红 */
            
            td.diff_header + td {{ border-right: 1px solid #e5e7eb; }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- 头部运行元数据展示（彻底剔除时间对比差异） -->
            <div class="overview-card">
                <h1 class="overview-title">🚀 接口契约自动化审计报告</h1>
                <div class="overview-grid">
                    {test_case_item_html}
                    <div class="overview-item">
                        <div class="overview-label">较早运行时间 (Data 1)</div>
                        <div class="overview-val">{prev_time}</div>
                    </div>
                    <div class="overview-item">
                        <div class="overview-label">最新运行时间 (Data 2)</div>
                        <div class="overview-val">{curr_time}</div>
                    </div>
                    <div class="overview-item">
                        <div class="overview-label">总对齐接口维度</div>
                        <div class="overview-val">{len(all_keys)} 个对齐接口节点</div>
                    </div>
                </div>
            </div>

            <!-- 所有接口的对比卡片列表 -->
            {api_cards_html}
        </div>
    </body>
    </html>
    """

    # 5. 保存精心打磨的可视化对比报告
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    logger.success(f"[DiffReporter] 接口对比报告已成功生成: {report_path}")
    return True
