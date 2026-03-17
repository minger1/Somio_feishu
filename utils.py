import random
import time
from datetime import datetime



# ==================== 工具函数 ====================

# 生成随机邮箱
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




# 生成随机歌名
_used = set()
_counter = 0

PARTS = {
    "mood":  [
        "lost", "broken", "burning", "silent", "fading", "rising", "falling",
        "frozen", "hollow", "restless", "lonely", "wild", "dark", "bright",
        "empty", "stolen", "bleeding", "dreaming", "waking", "scared"
    ],
    "noun":  [
        "stars", "ashes", "echo", "tide", "shadow", "storm", "dust", "flame",
        "shore", "ghost", "road", "rain", "light", "smoke", "wave", "stone",
        "river", "sky", "moon", "fire", "wind", "heart", "soul", "dream"
    ],
    "adj":   [
        "golden", "silver", "last", "first", "old", "new", "cold", "warm",
        "deep", "high", "soft", "hard", "slow", "fast", "long", "short",
        "blue", "red", "pale", "dark"
    ],
    "verb":  [
        "chase", "run", "fall", "burn", "drift", "break", "hide", "find",
        "lose", "leave", "stay", "fight", "fly", "sink", "rise", "fade",
        "hold", "touch", "call", "cry"
    ],
}

PRESETS = [
    "Midnight Echo", "Glass Hearts", "Neon Rain", "Paper Crowns",
    "The Last Signal", "Ghost Train", "Fire Season", "Cold Silence",
    "Empty Roads", "Broken Sky", "Silver Tide", "Pale Moonlight",
    "Storm Chaser", "Fading Lights", "Lost in Static", "The Long Way Home",
    "Burning Bridges", "Hollow Ground", "Running on Empty", "Dead Stars",
    "Under the Same Sky", "Falling Slowly", "Into the Wild", "Gone with the Wind",
]

def get_song() -> str:
    random.seed(time.time_ns())

    style = random.choice(["preset", "mood_noun", "adj_noun", "verb_noun"])

    if style == "preset":
        base = random.choice(PRESETS)
    elif style == "mood_noun":
        base = f"{random.choice(PARTS['mood'])} {random.choice(PARTS['noun'])}"
    elif style == "adj_noun":
        base = f"{random.choice(PARTS['adj'])} {random.choice(PARTS['noun'])}"
    else:
        base = f"{random.choice(PARTS['verb'])} the {random.choice(PARTS['noun'])}"

    suffix = int(time.time_ns() // 1_000_000) % 100  # 毫秒级，2位数，不易重复
    return f"{base} {suffix}"