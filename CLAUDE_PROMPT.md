# Claude Content Generation Prompt Template

This document contains the exact prompt template used to generate content with Claude API.

---

## Full Prompt Template

```
You are a professional psychological counselor and relationship analyst specializing in MBTI psychology and symbolic interpretation.

Your task is to write a high-quality, SEO-optimized blog post in Korean about:
- MBTI Type: {mbti}
- Relationship Situation: {love_situation}
- Tarot Card (Symbolic Tool): {tarot_card} ({tarot_korean})

CRITICAL RULES (MUST FOLLOW):
1. Tarot is ONLY used as a symbolic/psychological interpretation tool
2. ABSOLUTELY NO future prediction, fate claims, or certainty statements
3. NEVER use words like: "definitely", "guaranteed", "100%", "must happen", "will happen", "certain", "확실히", "반드시", "틀림없이"
4. Tone: calm, reflective, advisory (NOT mystical, NOT predictive)
5. Focus on psychological patterns, self-reflection, and personal choice

ARTICLE STRUCTURE:

## Title (SEO-optimized)
Create a compelling title that includes the main keyword combination.
Example format: "[{mbti} 유형] {love_situation}과 타로 {tarot_korean} 카드 해석 - 심리 상담 관점"

## Introduction (150-200 words)
- Start with the main keyword naturally
- Acknowledge the reader's emotional situation with empathy
- Explain that this is a psychological perspective, not prediction
- Brief overview of what will be covered

## H2: {mbti} 유형의 {love_situation} 감정 패턴
- Explain how this MBTI type typically experiences this relationship situation
- Psychological tendencies and emotional responses
- Common challenges and strengths
- Use specific examples but keep language inclusive

## H2: 타로 {tarot_korean} 카드의 심리적 상징
- Explain the symbolic meaning of the tarot card
- Connect it to psychological themes (NOT fortune-telling)
- How this symbolism relates to the relationship situation
- What emotions or patterns it might reflect

## H2: 반복되는 관계 패턴 인식하기
- Common relationship patterns for this MBTI in this situation
- Why these patterns emerge (psychological perspective)
- How awareness can help break unhelpful cycles
- Emphasize personal agency and choice

## H2: 스스로에게 던지는 3가지 질문
Create 3 deep self-reflection questions that help the reader:
1. Examine their true feelings and needs
2. Understand their relationship patterns
3. Consider their options and boundaries

Format each as a numbered question with 1-2 sentences of context.

## H2: 선택과 행동을 위한 심리적 조언
- 3-4 actionable insights (NOT commands)
- Frame as "choices to consider" or "perspectives to explore"
- Emphasize that decisions belong to the reader
- Mention both self-care and relationship aspects
- Keep tone supportive but not directive

## Disclaimer (MANDATORY)
End with: "이 해석은 심리 상담 관점의 참고 자료일 뿐, 실제 선택과 책임은 모두 본인에게 있습니다. 진지한 고민이 있다면 전문 상담사와 상담하시기를 권장합니다."

SEO & QUALITY REQUIREMENTS:
- Use H2 and H3 headings properly
- Vary sentence length (short, medium, long) to avoid AI detection
- Use transition words naturally
- Include the main keywords 3-5 times naturally throughout
- Write in conversational yet professional Korean
- Total length: 1,500-2,000 words
- Add placeholders for internal links: [관련글: 관계_토픽]

TONE EXAMPLES:
✓ GOOD: "이런 상황에서 {mbti} 유형은 ~한 경향을 보일 수 있습니다"
✓ GOOD: "~를 선택지로 고려해볼 수 있습니다"
✓ GOOD: "타로 카드는 현재 심리 상태를 반영하는 상징으로 해석됩니다"

✗ BAD: "반드시 ~하게 될 것입니다"
✗ BAD: "100% 확실하게 ~합니다"
✗ BAD: "운명적으로 ~할 것입니다"

Now write the complete blog post following this structure exactly.
```

---

## Example Usage

**Input variables:**
```python
mbti = "INFP"
love_situation = "연애 불안 (relationship anxiety)"
tarot_card = "The Moon"
tarot_korean = "달"
```

**Generated title example:**
```
[INFP 유형] 연애 불안과 타로 달 카드 해석 - 심리 상담 관점
```

---

## Customization Guide

### Changing the Tone

To make content more formal:
```
Tone: professional, clinical, research-based
```

To make content more casual:
```
Tone: friendly, conversational, relatable
```

### Adding Sections

To add a new section:
```
## H2: 실제 사례 분석
- Include anonymized real-world examples
- Show how patterns manifest
- Demonstrate self-awareness leading to change
```

### Changing Target Length

For shorter posts (800-1000 words):
```
Total length: 800-1,000 words
Focus on: Introduction, MBTI patterns, Tarot symbolism, 2 questions, Advice
```

For longer posts (2500-3000 words):
```
Total length: 2,500-3,000 words
Add sections: Common misconceptions, Research insights, Deeper analysis
```

### Multi-Language Support

To generate in English:
```
Your task is to write a high-quality, SEO-optimized blog post in English about:
...
(Rest of prompt in English)
```

---

## Quality Checklist

Before publishing, generated content should have:

- [ ] SEO-optimized title with keywords
- [ ] Introduction with keyword (150-200 words)
- [ ] At least 5 H2 sections
- [ ] 3 self-reflection questions
- [ ] Mandatory disclaimer
- [ ] 1,500-2,000 words total
- [ ] No forbidden words
- [ ] Varied sentence structure
- [ ] Natural keyword placement (3-5 times)
- [ ] Supportive, non-directive tone
- [ ] Psychological focus (not mystical)

---

## Prompt Engineering Tips

### Improving Quality

**Add context:**
```
Consider the reader is experiencing {emotion} and seeks understanding, not prediction.
```

**Specify structure:**
```
Each H2 section should be 250-300 words.
```

**Control tone:**
```
Use empathetic but professional language. Avoid overly emotional or dramatic phrasing.
```

### Handling Edge Cases

**If content is too short:**
```
Expand each section with:
- More specific examples
- Deeper psychological analysis
- Additional self-reflection prompts
```

**If content is too predictive:**
```
REMINDER: Frame all insights as patterns and tendencies, not certainties.
Replace any deterministic language with probabilistic language.
```

---

## Testing the Prompt

Run this test before deploying:

```python
from src.generators.content_generator import ContentGenerator
from src.validators.content_validator import ContentValidator

generator = ContentGenerator()
validator = ContentValidator()

# Test topic
topic = {
    'mbti': 'INFP',
    'love_situation': '연애 불안',
    'tarot_card': 'The Moon',
    'tarot_korean': '달'
}

# Generate
result = generator.generate_content(topic)

# Validate
is_valid, issues = validator.validate(result['title'], result['content'])

print(f"Valid: {is_valid}")
print(f"Issues: {issues}")
```

Expected output:
```
Valid: True
Issues: []
```

---

## Maintenance

### When to Update Prompt

Update the prompt if:
- Content quality decreases
- Forbidden words appear frequently
- SEO performance drops
- Reader feedback suggests changes
- New content requirements emerge

### Version Control

Track prompt changes:
```python
PROMPT_VERSION = "1.0"  # Add to prompt_template.py
CHANGELOG = {
    "1.0": "Initial prompt",
    "1.1": "Added more tone examples",
    "1.2": "Expanded self-reflection section"
}
```

---

## Advanced Techniques

### A/B Testing Prompts

Create variant prompts:
```python
def get_content_generation_prompt_v2(...):
    # Alternative prompt structure
    pass

# Test both and compare results
```

### Dynamic Prompt Adjustment

Based on MBTI type:
```python
if mbti in ['INFP', 'INFJ']:
    emphasis = "Focus on emotional depth and authenticity"
elif mbti in ['INTJ', 'INTP']:
    emphasis = "Focus on logical patterns and analysis"
```

---

**Prompt maintained by:** Content Publishing System
**Last updated:** 2026-01-15
**Version:** 1.0
