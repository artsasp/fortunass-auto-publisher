# Automated Content Publishing System
## Tarot × Love × MBTI

A fully automated, zero-human-interaction content publishing system that generates high-quality, SEO-optimized psychological content and publishes to WordPress.

**Key Features:**
- 🤖 Fully automated (GitHub Actions)
- 🎯 Unique topic generation (MBTI × Love × Tarot)
- 🔒 Safety filters (no predictions/certainty)
- ♻️ Duplicate prevention (SQLite tracking)
- 🔄 Retry logic with fallback
- 📊 Comprehensive logging

---

## 📋 TABLE OF CONTENTS

1. [System Architecture](#system-architecture)
2. [Quick Start](#quick-start)
3. [Topic Combinations](#topic-combinations)
4. [Content Generation Rules](#content-generation-rules)
5. [Usage](#usage)
6. [GitHub Actions Setup](#github-actions-setup)
7. [Configuration](#configuration)
8. [SaaS Expansion Notes](#saas-expansion-notes)

---

## 🏗️ SYSTEM ARCHITECTURE

```
Topic Generator → Content Generator → Validator → WordPress Publisher → Database
     ↓                  ↓                ↓              ↓                  ↓
  (SQLite)         (Claude API)    (Safety)       (REST API)          (Tracking)
```

**Pipeline Flow:**
1. **Topic Generation**: Random selection with duplicate checking
2. **Content Generation**: Claude API with specialized prompt
3. **Content Validation**: Safety filters + SEO checks
4. **Auto-sanitization**: Replace forbidden words if found
5. **WordPress Publishing**: REST API with retry logic
6. **Database Tracking**: Save to SQLite + commit to repo

**Total Unique Combinations:** 16 (MBTI) × 20 (Love) × 22 (Tarot) = **7,040 unique posts**

---

## 🚀 QUICK START

### 1. Clone Repository

```bash
git clone <your-repo>
cd content-publisher
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

Required credentials:
- **Anthropic API Key**: Get from https://console.anthropic.com
- **WordPress Site URL**: Your WordPress site
- **WordPress Username**: Admin username
- **WordPress App Password**: Generate in WordPress > Users > Profile > Application Passwords

### 4. Run Locally

```bash
# Publish as draft
python main.py --status draft

# Publish immediately
python main.py --status publish

# Schedule for 3 hours from now
python main.py --status future --schedule-hours 3

# View statistics
python main.py --stats
```

---

## 🎲 TOPIC COMBINATIONS

### MBTI Types (16)
INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP

### Love Situations (20)
- 연애 불안 (relationship anxiety)
- 밀당 (push-pull dynamics)
- 애착 유형 (attachment style)
- 거리감 (emotional distance)
- 재회 고민 (reconciliation concerns)
- 이별 후 감정 (post-breakup emotions)
- 짝사랑 (unrequited love)
- 권태기 (relationship boredom)
- 신뢰 문제 (trust issues)
- 소통 단절 (communication breakdown)
- And 10 more...

### Tarot Major Arcana (22)
The Fool, The Magician, The High Priestess, The Empress, The Emperor, The Hierophant, The Lovers, The Chariot, Strength, The Hermit, Wheel of Fortune, Justice, The Hanged Man, Death, Temperance, The Devil, The Tower, The Star, The Moon, The Sun, Judgement, The World

---

## 📝 CONTENT GENERATION RULES

### ✅ REQUIRED
- Psychological counselor perspective
- Tarot as symbolic interpretation tool
- Calm, reflective, advisory tone
- SEO-optimized structure (H2/H3)
- 3 self-reflection questions
- Mandatory disclaimer

### ❌ FORBIDDEN
- Future prediction
- Fate/destiny claims
- Certainty statements
- Words: "definitely", "guaranteed", "100%", "must happen", "will happen", "확실히", "반드시", "틀림없이"

### Article Structure
1. **SEO Title** with main keyword
2. **Introduction** (150-200 words)
3. **MBTI Emotional Patterns** (H2)
4. **Tarot Symbolic Meaning** (H2)
5. **Repeating Relationship Patterns** (H2)
6. **3 Self-Reflection Questions** (H2)
7. **Psychological Guidance** (H2)
8. **Disclaimer** (mandatory)

**Target Length:** 1,500-2,000 words

---

## 💻 USAGE

### Local Execution

```bash
# Basic usage (draft)
python main.py

# Publish immediately
python main.py --status publish

# Schedule for future
python main.py --status future --schedule-hours 6

# Disable auto-sanitization
python main.py --no-sanitize

# View statistics
python main.py --stats
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--status` | Post status (draft/publish/future) | draft |
| `--schedule-hours` | Hours from now to schedule | None |
| `--no-sanitize` | Disable auto-sanitization | False |
| `--stats` | Show statistics and exit | False |

---

## ⚙️ GITHUB ACTIONS SETUP

### 1. Add Repository Secrets

Go to **Settings → Secrets and variables → Actions** and add:

- `ANTHROPIC_API_KEY`
- `WORDPRESS_SITE_URL`
- `WORDPRESS_USERNAME`
- `WORDPRESS_APP_PASSWORD`

### 2. Automated Publishing

The workflow runs automatically:
- **Schedule**: Daily at 9 AM KST (00:00 UTC)
- **Status**: Publishes directly (not draft)

Edit `.github/workflows/publish-content.yml` to change schedule:

```yaml
schedule:
  - cron: '0 0 * * *'  # Daily at 00:00 UTC
```

Cron examples:
- Every 6 hours: `0 */6 * * *`
- Twice daily (6 AM, 6 PM KST): `0 21,9 * * *`
- Weekly on Monday: `0 0 * * 1`

### 3. Manual Trigger

1. Go to **Actions** tab
2. Select **Automated Content Publishing**
3. Click **Run workflow**
4. Choose status and schedule options
5. Click **Run workflow**

### 4. Database Persistence

The SQLite database is automatically:
- Cached between runs
- Committed back to repository
- Tracked for duplicate prevention

**No external database needed!**

---

## 📊 CONFIGURATION

### Project Structure

```
content-publisher/
├── .github/workflows/
│   └── publish-content.yml      # GitHub Actions workflow
├── src/
│   ├── data/
│   │   └── topic_data.py        # MBTI, Love, Tarot data
│   ├── generators/
│   │   ├── topic_generator.py   # Topic generation
│   │   ├── content_generator.py # Claude API integration
│   │   └── prompt_template.py   # Content prompt
│   ├── validators/
│   │   └── content_validator.py # Safety filters
│   ├── publishers/
│   │   └── wordpress_publisher.py # WordPress REST API
│   ├── utils/
│   │   ├── database.py          # SQLite manager
│   │   └── logger.py            # Structured logging
│   └── orchestrator.py          # Main pipeline
├── data/
│   └── published_topics.db      # SQLite database
├── logs/
│   └── YYYY-MM-DD.log          # Daily logs (JSON)
├── main.py                      # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

### Customization

**Change MBTI types:**
Edit `src/data/topic_data.py` → `MBTI_TYPES`

**Change love situations:**
Edit `src/data/topic_data.py` → `LOVE_SITUATIONS`

**Add forbidden words:**
Edit `src/data/topic_data.py` → `FORBIDDEN_WORDS`

**Modify content prompt:**
Edit `src/generators/prompt_template.py` → `get_content_generation_prompt()`

**Change categories/tags logic:**
Edit `src/orchestrator.py` → `_get_categories()` and `_get_tags()`

---

## 🚀 SAAS EXPANSION NOTES

### Multi-Tenant Architecture

**Database per tenant:**
```python
db = TopicDatabase(f"data/tenant_{tenant_id}.db")
```

**WordPress credentials per tenant:**
```python
publisher = WordPressPublisher(
    site_url=tenant.wp_url,
    username=tenant.wp_user,
    app_password=tenant.wp_pass
)
```

### API Service Layer

```python
# FastAPI endpoint
@app.post("/api/publish")
async def publish_content(tenant_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_publisher, tenant_id)
    return {"status": "scheduled"}
```

### Scaling Considerations

1. **Rate Limiting**: Add rate limiter for Claude API
2. **Queue System**: Use Celery/RQ for background jobs
3. **Monitoring**: Add Sentry for error tracking
4. **Analytics**: Track success rates per tenant
5. **Webhooks**: Notify on publish success/failure
6. **Custom Prompts**: Allow tenant-specific prompt templates
7. **Billing**: Track API usage per tenant

### Database Migration

**For production SaaS:**
- Replace SQLite with PostgreSQL
- Add tenant_id to all tables
- Implement database connection pooling

```python
# PostgreSQL schema
CREATE TABLE published_topics (
    tenant_id UUID NOT NULL,
    mbti TEXT NOT NULL,
    love_situation TEXT NOT NULL,
    tarot_card TEXT NOT NULL,
    ...
    PRIMARY KEY (tenant_id, mbti, love_situation, tarot_card)
);
```

### Authentication & Multi-Tenancy

```python
# Tenant model
class Tenant:
    tenant_id: str
    wp_site_url: str
    wp_username: str
    wp_app_password: str
    anthropic_api_key: str  # Or shared key
    publish_schedule: str    # Cron expression
    status_preference: str   # draft/publish/future
    active: bool
```

### Feature Flags

```python
FEATURES = {
    'auto_sanitize': True,
    'schedule_publishing': True,
    'category_mapping': True,
    'custom_prompts': False  # Premium feature
}
```

### Monitoring Dashboard

Track per tenant:
- Total posts published
- Success rate
- API costs (Claude + WordPress)
- Remaining topic combinations
- Errors and retries

---

## 📈 STATISTICS

View anytime:

```bash
python main.py --stats
```

Output:
```
==================================================
Publishing Statistics
==================================================
Total published: 42
By status: {'publish': 38, 'draft': 3, 'failed': 1}
Success rate: 97.62%
==================================================
```

---

## 🔧 TROUBLESHOOTING

**Issue**: Content validation failed
- Check logs in `logs/YYYY-MM-DD.log`
- Review forbidden words list
- Enable auto-sanitization

**Issue**: WordPress publishing failed
- Verify WordPress REST API is enabled
- Check Application Password is correct
- Ensure username has publish permissions

**Issue**: Claude API error
- Verify API key is valid
- Check API usage limits
- Review rate limiting

**Issue**: Database locked
- SQLite is single-writer
- GitHub Actions handles commits
- Don't run locally while Actions is running

---

## 📜 LICENSE

MIT License

---

## 🤝 CONTRIBUTING

This is a private monetization project. For SaaS inquiries, contact the owner.

---

**Built with Claude Sonnet 4.5**
