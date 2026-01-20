"""Weekly fortune prompt template for MBTI types."""

from datetime import datetime, timedelta


def get_weekly_fortune_prompt(mbti: str, week_start: str, week_end: str) -> str:
    """Generate prompt for weekly fortune content.

    Args:
        mbti: MBTI personality type
        week_start: Week start date (YYYY-MM-DD)
        week_end: Week end date (YYYY-MM-DD)

    Returns:
        Formatted prompt string
    """
    return f"""You are a professional psychological counselor and life coach specializing in MBTI psychology.

Your task is to write a COMPLETE, high-quality, SEO-optimized weekly forecast in Korean for:
- MBTI Type: {mbti}
- Week Period: {week_start} ~ {week_end}

⚠️ CRITICAL REQUIREMENTS:
1. Write the COMPLETE article from start to finish - DO NOT stop mid-sentence
2. This is a psychological guidance perspective, NOT fortune-telling
3. Use emojis (💜, 🌸, ✨, 🎯, 💭, 🌿, 🔮, 💫) instead of ** markdown bold
4. Every section must be complete with proper endings
5. ABSOLUTELY NO future prediction, fate claims, or certainty statements
6. Focus on self-awareness, potential opportunities, and personal growth
7. Frame as "tendencies to be aware of" NOT "what will happen"

FORMATTING RULES:
- DO NOT use ** for bold text
- Use emojis to emphasize sections
- Section titles use ## (keep these)
- Tone: encouraging, reflective, empowering (NOT mystical, NOT predictive)

ARTICLE STRUCTURE (WRITE EVERYTHING COMPLETELY):

## SEO Metadata (Write at the very beginning)

META_DESCRIPTION: [Write 60-110 character meta description]
- Include keywords: {mbti}, 이주의 운세, 주간 운세, MBTI 운세
- Example: "{mbti} 유형을 위한 이번 주 심리 운세입니다. 관계, 업무, 자기계발 측면의 심리적 경향과 조언."

OG_TITLE: [Write Open Graph title - same as H1 or slightly modified]

OG_DESCRIPTION: [Write 100-150 character description for social sharing]

IMAGE_ALT: [Write alt text for featured image]
- Example: "{mbti} 유형을 위한 이번 주 운세, 심리적 성장과 자기 인식"

INTERNAL_LINKS: [Write 3-4 natural anchor text phrases]
- Example 1: "{mbti} 연애 패턴"
- Example 2: "{mbti} 유형의 강점"
- Example 3: "MBTI 심리 분석"
- Example 4: "주간 자기계발 팁"

---

## Title (SEO-optimized H1)
Example format: "[{mbti} 유형] 이번 주 운세 ({week_start}~{week_end}) - 심리 상담 관점"

## Introduction (100-150 words)
- Warm greeting for the week
- Brief overview of this week's psychological themes for {mbti}
- Emphasize this is about self-awareness and potential opportunities, NOT predictions
- Mention that all choices and outcomes depend on the individual

## H2: 💜 이번 주 전반적인 심리 흐름
- Describe the overall psychological tendencies for {mbti} this week
- What emotions or mental states they might experience
- Frame as "~할 수 있습니다", "~하는 경향이 있습니다"
- 150-200 words
- **MUST insert 1st internal link:** (e.g., "[{mbti} 유형의 강점]을 활용하는 한 주")

## H2: 🌸 관계 운세 (연애·인간관계)
Write 2-3 subsections:

✨ 연애 & 사랑
- Relationship tendencies and communication tips for {mbti} this week
- Frame as possibilities and awareness points, NOT certainties
- 100-150 words

💫 친구 & 동료
- Social dynamics and interpersonal advice
- 100-150 words
- **MUST insert 2nd internal link:** (e.g., "[{mbti} 연애 패턴]을 이해하기")

## H2: 🎯 업무 & 학업 운세
- Work/study focus areas for {mbti} this week
- Productivity tips aligned with MBTI strengths
- Challenges to be aware of and how to approach them
- Frame as "주의할 점", "집중하면 좋은 영역"
- 150-200 words

## H2: 🌿 자기계발 & 성장 포인트
- Personal growth opportunities this week
- Habits or practices that align with {mbti} psychology
- Self-care recommendations
- 150-200 words
- **MUST insert 3rd internal link:** (e.g., "[MBTI 심리 분석]으로 자기 이해")

## H2: 🔮 이번 주 행운의 키워드
Present 3-5 symbolic keywords for the week:

💫 키워드 1: [단어]
(1-2 sentences explaining the psychological significance)

✨ 키워드 2: [단어]
(1-2 sentences)

🌸 키워드 3: [단어]
(1-2 sentences)

## H2: 💭 이번 주 스스로에게 던지는 질문

Create 2 deep self-reflection questions:

🌿 질문 1: [질문 내용]
(1-2 sentences of context)

🌿 질문 2: [질문 내용]
(1-2 sentences of context)
**MUST insert 4th internal link:** (e.g., "[주간 자기계발 팁]으로 성장하기")

## Closing Message (100 words)
- Encouraging message for {mbti}
- Remind that they have agency and choice
- Positive, empowering tone

## DISCLAIMER (MANDATORY - MUST INCLUDE THIS)
⚠️ 이 주간 운세는 심리 상담 관점의 참고 자료일 뿐, 실제 선택과 결과는 모두 본인에게 달려 있습니다. 모든 가능성은 여러분의 행동과 선택에 의해 만들어집니다.

SEO & QUALITY REQUIREMENTS:
- Write SEO metadata at the very beginning
- Use H2 headings properly with keywords
- **CRITICAL: Insert 3-4 internal link anchor texts in brackets [앵커텍스트]**
- Write in warm, encouraging Korean tone
- Total length: 1,500-1,800 words
- NO fortune-telling language, NO predictions

TONE EXAMPLES:
✓ GOOD: "이번 주 {mbti} 유형은 ~를 경험할 수 있습니다"
✓ GOOD: "~에 주의를 기울이면 도움이 될 수 있습니다"
✓ GOOD: "~하는 경향이 있으니 스스로를 관찰해보세요"

✗ BAD: "반드시 ~하게 될 것입니다"
✗ BAD: "이번 주 ~가 일어납니다"
✗ BAD: "운명적으로 ~를 만나게 됩니다"

⚠️ FINAL REMINDER:
- Write SEO metadata FIRST
- Write the COMPLETE article from title to disclaimer
- Include 3-4 internal link anchor texts in brackets
- Use emojis (not **) for emphasis
- Frame everything as psychological tendencies and self-awareness, NOT predictions

Now write the complete weekly forecast following this structure exactly. Make sure to finish every sentence and include the disclaimer."""
