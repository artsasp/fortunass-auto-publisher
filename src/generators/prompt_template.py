"""Claude API prompt templates for content generation."""


def get_content_generation_prompt(mbti: str, love_situation: str, tarot_card: str, tarot_korean: str, card_type: str = "tarot") -> str:
    """Generate prompt for Claude API.

    Args:
        mbti: MBTI personality type
        love_situation: Love/relationship situation
        tarot_card: Card name (English) - can be tarot, numerology, or oracle
        tarot_korean: Card name (Korean)
        card_type: Type of card (tarot, numerology, oracle)

    Returns:
        Formatted prompt string
    """
    # Determine card type description
    if card_type == "numerology":
        card_desc = f"수비학 {tarot_korean}"
        tool_type = "Numerology Number (Symbolic Tool)"
        card_intro = f"Numerology Number: {tarot_card} ({tarot_korean})"
    elif card_type == "oracle":
        card_desc = f"오라클 카드 {tarot_korean}"
        tool_type = "Oracle Card (Symbolic Tool)"
        card_intro = f"Oracle Card: {tarot_card} ({tarot_korean})"
    else:  # tarot (default)
        card_desc = f"타로 {tarot_korean} 카드"
        tool_type = "Tarot Card (Symbolic Tool)"
        card_intro = f"Tarot Card: {tarot_card} ({tarot_korean})"

    return f"""You are a professional psychological counselor and relationship analyst specializing in MBTI psychology and symbolic interpretation.

Your task is to write a COMPLETE, high-quality, SEO-optimized blog post in Korean about:
- MBTI Type: {mbti}
- Relationship Situation: {love_situation}
- {tool_type}: {card_intro}

⚠️ CRITICAL REQUIREMENTS:
1. Write the COMPLETE article from start to finish - DO NOT stop mid-sentence
2. MUST include the disclaimer at the end (mandatory)
3. Use emojis (💜, 🌸, ✨, 🎯, 💭, 🌿, 🔮, 💫) instead of ** markdown bold
4. Every section must be complete with proper endings

FORMATTING RULES:
- DO NOT use ** for bold text
- Use emojis to emphasize sections (e.g., "🌸 관계에서의 투명성" instead of "**관계에서의 투명성**")
- Section titles use ## (keep these)
- Use 이모티콘 to make content warm and engaging

CRITICAL RULES (MUST FOLLOW):
1. Tarot is ONLY used as a symbolic/psychological interpretation tool
2. ABSOLUTELY NO future prediction, fate claims, or certainty statements
3. NEVER use words like: "definitely", "guaranteed", "100%", "must happen", "will happen", "certain", "확실히", "반드시", "틀림없이"
4. Tone: calm, reflective, advisory (NOT mystical, NOT predictive)
5. Focus on psychological patterns, self-reflection, and personal choice

ARTICLE STRUCTURE (WRITE EVERYTHING COMPLETELY):

## SEO Metadata (Write at the very beginning)

META_DESCRIPTION: [Write 60-110 character meta description]
- Include keywords: {mbti}, {love_situation}, {tarot_korean}, 타로 심리, 상징
- Informational tone, no emotional excess
- Example: "{mbti} {love_situation} 심리 패턴을 타로 {tarot_korean} 카드의 상징으로 해석합니다. 심리 상담 관점의 관계 분석."

OG_TITLE: [Write Open Graph title - same as H1 or slightly modified]

OG_DESCRIPTION: [Write 100-150 character description for social sharing]

IMAGE_ALT: [Write alt text for featured image]
- Describe the symbolic imagery related to {tarot_korean} and {love_situation}
- Example: "{love_situation} 상황에서 타로 {tarot_korean} 카드를 바라보는 {mbti} 유형, 심리적 성찰"

INTERNAL_LINKS: [Write 3-4 natural anchor text phrases for internal linking]
- Example 1: "{mbti} 연애 패턴"
- Example 2: "관계에서 반복되는 심리 패턴"
- Example 3: "타로 카드로 보는 관계 심리"
- Example 4: "{love_situation} 극복 방법"

---

## Title (SEO-optimized H1)
Create a compelling title that includes the main keyword combination and the word "상징".
Example format: "[{mbti} 유형] {love_situation}과 {card_desc}의 상징 - 심리 상담 관점"

## Introduction (150-200 words)
- Start with the main keyword naturally and mention "상징" early
- Acknowledge the reader's emotional situation with empathy
- Explain that this tool ({card_desc}) is a symbolic tool for psychological reflection (심리적 성찰을 위한 상징적 도구)
- Brief overview emphasizing symbolic interpretation, not prediction
- Use phrases like "상징으로 바라본", "상징적 관점에서" in the introduction

## H2: {mbti} 유형의 {love_situation} 감정 패턴 (SEO-friendly heading)
- Include keywords naturally: {mbti}, {love_situation}, 심리 패턴
- Explain how this MBTI type typically experiences this relationship situation
- Psychological tendencies and emotional responses
- Common challenges and strengths
- Use specific examples but keep language inclusive
- Use emojis like 💜, 🌸 to separate subsections
- **MUST insert 1st internal link:** Naturally insert anchor text in brackets (e.g., "[{mbti} 연애 패턴]에 대해 더 알아보기")

## H2: {card_desc}의 심리적 상징 해석
- Include keywords: {card_desc}, 심리적 상징, 관계 심리
- Explain the symbolic meaning of this card/number
- Connect it to psychological themes (NOT fortune-telling or prediction)
- How this symbolism relates to the relationship situation
- What emotions or patterns it might reflect
- Use 🔮, ✨ emojis for emphasis
- Emphasize: "상징으로 해석하면", "상징적 의미"

## H2: 반복되는 관계 패턴 인식하기
- Include keywords: 관계 패턴, 심리 분석
- Common relationship patterns for this MBTI in this situation
- Why these patterns emerge (psychological perspective)
- How awareness can help break unhelpful cycles
- Emphasize personal agency and choice
- Use 🎯, 💭 emojis
- **MUST insert 2nd internal link:** Naturally insert anchor text in brackets (e.g., "[관계에서 반복되는 심리 패턴]을 이해하는 방법")

## H2: 스스로에게 던지는 3가지 질문
Create 3 deep self-reflection questions that help the reader:

🌿 질문 1: [질문 내용]
(1-2 sentences of context)

🌿 질문 2: [질문 내용]
(1-2 sentences of context)

🌿 질문 3: [질문 내용]
(1-2 sentences of context)
**MUST insert 3rd internal link here:** (e.g., "이러한 질문은 [{love_situation} 극복 방법]을 찾는 데 도움이 됩니다.")

## H2: 선택과 행동을 위한 심리적 조언

Write 3-4 complete subsections with emojis:

🌸 [조언 제목]
(Complete explanation - DO NOT cut off mid-sentence. Finish the thought completely.)

💫 [조언 제목]
(Complete explanation with proper ending)

✨ [조언 제목]
(Complete explanation with proper ending)

💜 [조언 제목]
(Complete explanation with proper ending)
**MUST insert 4th internal link here:** (e.g., "[타로 카드로 보는 관계 심리]를 통한 자기 이해에 도움이 됩니다.")

Each advice section should:
- Be 3-4 complete sentences
- Frame as "choices to consider" or "perspectives to explore"
- Emphasize that decisions belong to the reader
- Have a clear beginning, middle, and END

## DISCLAIMER (MANDATORY - MUST INCLUDE THIS)
⚠️ 이 해석은 심리 상담 관점의 참고 자료일 뿐, 실제 선택과 책임은 모두 본인에게 있습니다. 진지한 고민이 있다면 전문 상담사와 상담하시기를 권장합니다.

SEO & QUALITY REQUIREMENTS:
- Write SEO metadata at the very beginning (META_DESCRIPTION, OG_TITLE, OG_DESCRIPTION, IMAGE_ALT, INTERNAL_LINKS)
- Use H2 headings properly with keywords (keep ##)
- Include "상징" keyword naturally 3-5 times throughout
- **CRITICAL: Insert 3-4 internal link anchor texts in brackets [앵커텍스트] throughout the content**
  - 1st link in "감정 패턴" section
  - 2nd link in "반복되는 관계 패턴" section
  - 3rd link after "3가지 질문" section
  - 4th link in "심리적 조언" section
- Vary sentence length (short, medium, long)
- Use transition words naturally
- Write in conversational yet professional Korean (informational tone, no emotional excess)
- Total length: 1,800-2,200 words
- NO clickbait, NO exaggeration in headings

TONE EXAMPLES:
✓ GOOD: "이런 상황에서 {mbti} 유형은 ~한 경향을 보일 수 있습니다"
✓ GOOD: "~를 선택지로 고려해볼 수 있습니다"
✓ GOOD: "타로 카드는 현재 심리 상태를 반영하는 상징으로 해석됩니다"

✗ BAD: "반드시 ~하게 될 것입니다"
✗ BAD: "100% 확실하게 ~합니다"
✗ BAD: "운명적으로 ~할 것입니다"

⚠️ FINAL REMINDER:
- Write SEO metadata FIRST (META_DESCRIPTION: 60-110자, OG_TITLE, OG_DESCRIPTION: 100-150자, IMAGE_ALT, INTERNAL_LINKS: 3-4개)
- Then write separator line: ---
- Write the COMPLETE article from title to disclaimer
- DO NOT stop mid-sentence or mid-paragraph
- Every section must have proper conclusions
- **CRITICAL: Include 3-4 internal link anchor texts in brackets [앵커텍스트] throughout the content**
- The disclaimer MUST be included at the end
- Use emojis (not **) for emphasis
- Maintain "타로 = 심리 상징" perspective throughout

Now write the complete blog post following this structure exactly. Make sure to finish every sentence and include the disclaimer."""
