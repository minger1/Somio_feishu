import pytest
from pages.effect_page import EffectPage
from utils import logger, get_song
from data.test_data import TEST_EFFECT_PROMPT

class TestEffectCreateSound:
    """Sound Effect (音效生成) 模式生成音效的功能测试集"""

    def test_effect_mode_generation_basic(self, logged_in_page):
        """
        [用例描述]：测试音效生成模式的基本流程：
        1. 切换到音效生成 Tab
        2. 输入音效提示词描述
        3. 在高级选项中设置音效名称
        4. 点击 Create 按钮开始生成
        5. 在 Library 的 Sounds 列表下等待生成成功
        """
        logger.info("开始测试音效生成模式基本功能 (仅输入 Prompt 和歌名)")
        ep = EffectPage(logged_in_page)
        effect_name = get_song(prefix="SFX", model="")

        # 1. 切换 Tab
        ep.switch_to_effect_tab()
        
        # 2. 输入提示词
        ep.input_prompt(TEST_EFFECT_PROMPT)
        
        # 3. 在高级选项中设置音效/歌曲名称
        ep.set_song_name(effect_name)
        
        # 4. 点击创作
        ep.click_create()
        
        # 5. 验证生成结果
        success = ep.wait_for_generation_success(title=effect_name, timeout=360000)
        assert success, f"音效 '{effect_name}' 生成超时或失败"
        logger.success("音效生成基本功能用例测试完毕")
