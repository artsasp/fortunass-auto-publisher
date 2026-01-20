"""Topic generation data: MBTI types, love situations, tarot cards, numerology, and oracle cards."""

# Card type options
CARD_TYPES = ["tarot", "numerology", "oracle"]

# 16 MBTI personality types
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# Love and relationship situations (Korean + English for SEO)
LOVE_SITUATIONS = [
    "연애 불안 (relationship anxiety)",
    "밀당 (push-pull dynamics)",
    "애착 유형 (attachment style)",
    "거리감 (emotional distance)",
    "재회 고민 (reconciliation concerns)",
    "이별 후 감정 (post-breakup emotions)",
    "짝사랑 (unrequited love)",
    "권태기 (relationship boredom)",
    "신뢰 문제 (trust issues)",
    "소통 단절 (communication breakdown)",
    "질투와 집착 (jealousy and obsession)",
    "사랑과 자존감 (love and self-esteem)",
    "결혼 고민 (marriage concerns)",
    "연상/연하 관계 (age gap relationship)",
    "장거리 연애 (long-distance relationship)",
    "감정 표현 어려움 (difficulty expressing emotions)",
    "상대방 마음 읽기 (reading partner's mind)",
    "관계 패턴 반복 (repeating relationship patterns)",
    "헤어짐 후 미련 (lingering attachment after breakup)",
    "새로운 시작 고민 (concerns about new beginning)"
]

# 22 Tarot Major Arcana cards
TAROT_MAJOR_ARCANA = [
    "The Fool",
    "The Magician",
    "The High Priestess",
    "The Empress",
    "The Emperor",
    "The Hierophant",
    "The Lovers",
    "The Chariot",
    "Strength",
    "The Hermit",
    "Wheel of Fortune",
    "Justice",
    "The Hanged Man",
    "Death",
    "Temperance",
    "The Devil",
    "The Tower",
    "The Star",
    "The Moon",
    "The Sun",
    "Judgement",
    "The World"
]

# Korean translations for tarot cards (for content)
TAROT_KOREAN = {
    "The Fool": "바보",
    "The Magician": "마법사",
    "The High Priestess": "여사제",
    "The Empress": "여황제",
    "The Emperor": "황제",
    "The Hierophant": "교황",
    "The Lovers": "연인",
    "The Chariot": "전차",
    "Strength": "힘",
    "The Hermit": "은둔자",
    "Wheel of Fortune": "운명의 수레바퀴",
    "Justice": "정의",
    "The Hanged Man": "매달린 사람",
    "Death": "죽음",
    "Temperance": "절제",
    "The Devil": "악마",
    "The Tower": "탑",
    "The Star": "별",
    "The Moon": "달",
    "The Sun": "태양",
    "Judgement": "심판",
    "The World": "세계"
}

# Numerology Numbers (1-9 + Master Numbers)
NUMEROLOGY_NUMBERS = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "11", "22", "33"
]

# Korean meanings for numerology
NUMEROLOGY_KOREAN = {
    "1": "숫자 1 (리더십과 독립)",
    "2": "숫자 2 (조화와 파트너십)",
    "3": "숫자 3 (창의성과 표현)",
    "4": "숫자 4 (안정과 기반)",
    "5": "숫자 5 (변화와 자유)",
    "6": "숫자 6 (사랑과 책임)",
    "7": "숫자 7 (영적 탐구)",
    "8": "숫자 8 (힘과 성취)",
    "9": "숫자 9 (완성과 나눔)",
    "11": "마스터 넘버 11 (직관과 영감)",
    "22": "마스터 넘버 22 (실현과 비전)",
    "33": "마스터 넘버 33 (사랑과 치유)"
}

# Oracle Cards (Relationship & Love themed)
ORACLE_CARDS = [
    "New Beginnings",
    "Trust Your Path",
    "Release and Let Go",
    "Divine Timing",
    "Self Love",
    "Healing Heart",
    "Soul Connection",
    "Inner Wisdom",
    "Transformation",
    "Boundaries",
    "Forgiveness",
    "Clarity",
    "Patience",
    "Courage",
    "Balance",
    "Authenticity",
    "Gratitude",
    "Hope",
    "Surrender",
    "Manifesting Love"
]

# Korean translations for oracle cards
ORACLE_KOREAN = {
    "New Beginnings": "새로운 시작",
    "Trust Your Path": "길을 믿기",
    "Release and Let Go": "놓아주기",
    "Divine Timing": "신성한 타이밍",
    "Self Love": "자기 사랑",
    "Healing Heart": "치유하는 마음",
    "Soul Connection": "영혼의 연결",
    "Inner Wisdom": "내면의 지혜",
    "Transformation": "변화",
    "Boundaries": "경계 설정",
    "Forgiveness": "용서",
    "Clarity": "명확함",
    "Patience": "인내",
    "Courage": "용기",
    "Balance": "균형",
    "Authenticity": "진정성",
    "Gratitude": "감사",
    "Hope": "희망",
    "Surrender": "맡기기",
    "Manifesting Love": "사랑 현실화"
}

# Forbidden words for content validation (no prediction/certainty)
FORBIDDEN_WORDS = [
    "definitely",
    "guaranteed",
    "100%",
    "must happen",
    "will happen",
    "certain",
    "확실히",
    "반드시",
    "틀림없이",
    "보장",
    "무조건",
    "100%"
]
