# SETUP GUIDE

Complete step-by-step setup instructions for the Automated Content Publishing System.

---

## PREREQUISITES

- Python 3.11+
- Git
- Anthropic API key
- WordPress site with admin access
- GitHub account (for automation)

---

## LOCAL SETUP

### Step 1: Clone and Install

```bash
# Clone repository
git clone <your-repository-url>
cd content-publisher

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get API Credentials

#### Anthropic API Key

1. Go to https://console.anthropic.com
2. Create account or log in
3. Navigate to API Keys
4. Create new key
5. Copy the key (starts with `sk-ant-api03-`)

#### WordPress Application Password

1. Log into WordPress admin
2. Go to **Users → Your Profile**
3. Scroll to **Application Passwords**
4. Enter name: "Content Publisher"
5. Click **Add New Application Password**
6. **COPY THE PASSWORD IMMEDIATELY** (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)
7. You won't be able to see it again

### Step 3: Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

Fill in your credentials:
```env
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
WORDPRESS_SITE_URL=https://yourblog.com
WORDPRESS_USERNAME=your_wp_username
WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

**Important:** Never commit `.env` to git!

### Step 4: Test Locally

```bash
# Test with draft first
python main.py --status draft

# Check if it worked
python main.py --stats
```

If successful, you should see:
- Database created at `data/published_topics.db`
- Logs created in `logs/`
- Draft post in your WordPress admin

---

## GITHUB ACTIONS SETUP

### Step 1: Push to GitHub

```bash
# Initialize git (if not already)
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Automated content publishing system"

# Add remote
git remote add origin <your-github-repo-url>

# Push
git push -u origin main
```

### Step 2: Add GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret:

| Secret Name | Value |
|-------------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `WORDPRESS_SITE_URL` | Your WordPress site URL |
| `WORDPRESS_USERNAME` | Your WordPress username |
| `WORDPRESS_APP_PASSWORD` | Your WordPress app password |

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab
2. If prompted, click **I understand my workflows, go ahead and enable them**
3. You should see **Automated Content Publishing** workflow

### Step 4: Test Workflow

#### Manual Test:
1. Click **Actions** tab
2. Click **Automated Content Publishing**
3. Click **Run workflow**
4. Select:
   - Branch: `main`
   - Post status: `draft` (for testing)
5. Click **Run workflow**
6. Wait for completion (1-2 minutes)
7. Check your WordPress for new draft post

#### Check Logs:
1. Click on the workflow run
2. Click **publish** job
3. Review each step's output
4. Download artifacts if needed

### Step 5: Configure Schedule

Edit `.github/workflows/publish-content.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Change this
```

**Common schedules:**
- Daily at 9 AM KST: `0 0 * * *`
- Twice daily: `0 0,12 * * *`
- Every 6 hours: `0 */6 * * *`
- Weekly on Monday: `0 0 * * 1`
- Weekdays only: `0 0 * * 1-5`

Use https://crontab.guru/ to generate cron expressions.

---

## WORDPRESS SETUP

### Enable REST API

The REST API is enabled by default in WordPress 4.7+, but verify:

1. Go to **Settings → Permalinks**
2. Select any option EXCEPT "Plain"
3. Click **Save Changes**

### Test REST API

```bash
curl https://your-blog.com/wp-json/wp/v2/posts
```

Should return JSON (not 404).

### Verify Permissions

Your WordPress user needs:
- `publish_posts` capability
- `edit_posts` capability
- `upload_files` capability

Admin and Editor roles have these by default.

---

## VERIFICATION CHECKLIST

- [ ] Local test successful (draft created)
- [ ] Database created (`data/published_topics.db`)
- [ ] Logs created (`logs/*.log`)
- [ ] GitHub repository created
- [ ] GitHub secrets added (all 4)
- [ ] GitHub Actions enabled
- [ ] Manual workflow test successful
- [ ] WordPress post visible
- [ ] Categories and tags created correctly
- [ ] Content validation passed
- [ ] No forbidden words in content

---

## MAINTENANCE

### Daily Checks (Optional)

```bash
# Check statistics
python main.py --stats

# View recent logs
tail -f logs/$(date +%Y-%m-%d).log
```

### Weekly Checks

1. Review published posts in WordPress
2. Check GitHub Actions success rate
3. Monitor API costs (Anthropic dashboard)

### Monthly Checks

1. Review database growth: `python main.py --stats`
2. Check remaining topic combinations
3. Review content quality manually (sample 5-10 posts)
4. Adjust forbidden words if needed

---

## TROUBLESHOOTING

### "Missing required environment variables"

**Problem:** Environment variables not set

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check contents
cat .env

# Ensure no spaces around =
# GOOD: ANTHROPIC_API_KEY=sk-ant-...
# BAD:  ANTHROPIC_API_KEY = sk-ant-...
```

### "Content validation failed"

**Problem:** Generated content contains forbidden words

**Solution:**
- Auto-sanitization is enabled by default
- Check logs for specific words found
- Add more replacements in `src/validators/content_validator.py`

### "WordPress publishing failed: 401 Unauthorized"

**Problem:** Invalid credentials

**Solution:**
1. Regenerate WordPress Application Password
2. Update `.env` locally
3. Update GitHub secret `WORDPRESS_APP_PASSWORD`
4. Ensure no extra spaces in password

### "WordPress publishing failed: 404 Not Found"

**Problem:** REST API not accessible

**Solution:**
1. Check WordPress URL is correct (no trailing slash)
2. Verify REST API is enabled
3. Test: `curl https://your-blog.com/wp-json/wp/v2/posts`

### "Claude API rate limit exceeded"

**Problem:** Too many requests

**Solution:**
- Reduce GitHub Actions frequency
- Add rate limiting in code
- Upgrade Anthropic plan

### "Database locked"

**Problem:** Concurrent access to SQLite

**Solution:**
- Don't run locally while GitHub Actions is running
- Wait for Actions to complete
- SQLite is single-writer

---

## SCALING

### Increasing Frequency

To publish multiple times per day:

```yaml
# 4 times daily (every 6 hours)
schedule:
  - cron: '0 */6 * * *'
```

**Cost estimate:**
- Claude API: ~$0.015 per post (at 2000 tokens)
- Daily (1 post): ~$0.45/month
- 4x daily: ~$1.80/month

### Monitoring Costs

**Anthropic Dashboard:**
1. Go to https://console.anthropic.com
2. Check **Usage** section
3. Monitor token consumption

**Calculate cost:**
```
Cost per post = (Input tokens + Output tokens) × Price per token
Input: ~1000 tokens × $0.003/1K = $0.003
Output: ~2000 tokens × $0.015/1K = $0.030
Total: ~$0.033 per post
```

---

## BACKUP & RECOVERY

### Backup Database

```bash
# Manual backup
cp data/published_topics.db data/backup_$(date +%Y%m%d).db

# Automated backup (add to cron)
0 0 * * 0 cp data/published_topics.db data/backup_$(date +%Y%m%d).db
```

### Restore Database

```bash
# Restore from backup
cp data/backup_20260115.db data/published_topics.db
```

### Export Published Topics

```bash
# SQLite to CSV
sqlite3 data/published_topics.db -header -csv "SELECT * FROM published_topics" > export.csv
```

---

## NEXT STEPS

1. **Monitor first week**: Check posts daily
2. **Refine content**: Adjust prompt if needed
3. **SEO optimization**: Add more internal links
4. **Analytics**: Set up Google Analytics
5. **Monetization**: Add ads, affiliate links
6. **Scaling**: Increase frequency if successful

---

## SUPPORT

- Check logs: `logs/YYYY-MM-DD.log`
- Review GitHub Actions output
- Inspect database: `sqlite3 data/published_topics.db`
- Test components individually

For SaaS expansion, refer to README.md → SaaS Expansion Notes.
