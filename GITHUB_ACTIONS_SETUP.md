# GitHub Actions 자동 발행 설정 가이드

이 가이드는 GitHub Actions를 사용하여 매일 오전 10시와 오후 6시에 자동으로 콘텐츠를 발행하도록 설정하는 방법을 설명합니다.

## 📅 자동 발행 스케줄

- **오전 10시 (KST)**: 일반 콘텐츠 발행 + 월요일에는 주간 운세 발행
- **오후 6시 (KST)**: 일반 콘텐츠 발행

## 🔑 1단계: GitHub Secrets 설정

GitHub 저장소에서 API 키와 WordPress 인증 정보를 안전하게 저장해야 합니다.

### 설정 방법:

1. **GitHub 저장소 페이지로 이동**
   - https://github.com/artsaap/fortunass-auto-publisher

2. **Settings > Secrets and variables > Actions**로 이동

3. **"New repository secret" 버튼 클릭**

4. **다음 Secrets를 하나씩 추가:**

   | Secret 이름 | 설명 | 예시 값 |
   |------------|------|--------|
   | `ANTHROPIC_API_KEY` | Claude API 키 | `sk-ant-api03-xxxxx...` |
   | `OPENAI_API_KEY` | OpenAI API 키 (DALL-E 이미지 생성) | `sk-proj-xxxxx...` |
   | `WORDPRESS_URL` | WordPress 사이트 URL | `http://fortunass.mycafe24.com` |
   | `WORDPRESS_USERNAME` | WordPress 관리자 사용자명 | `admin` |
   | `WORDPRESS_APP_PASSWORD` | WordPress Application Password | `xxxx xxxx xxxx xxxx` |

### WordPress Application Password 생성 방법:

1. WordPress 관리자 페이지 로그인
2. **사용자 > 프로필**로 이동
3. **Application Passwords** 섹션 찾기
4. 새 이름 입력 (예: "GitHub Actions")
5. **Add New Application Password** 클릭
6. 생성된 비밀번호 복사 (공백 포함해서 복사)

## 🚀 2단계: 저장소에 푸시

```bash
cd content-publisher
git add .
git commit -m "Setup GitHub Actions for auto-publishing"
git push -u origin main
```

## ✅ 3단계: GitHub Actions 확인

1. **GitHub 저장소 페이지 > Actions 탭**으로 이동
2. **"Auto Publish Content"** workflow 확인
3. 설정된 스케줄:
   - 매일 오전 10시 (KST)
   - 매일 오후 6시 (KST)

## 🧪 4단계: 수동 테스트 (선택사항)

자동 실행 전에 수동으로 테스트할 수 있습니다:

1. **Actions > Auto Publish Content** 선택
2. **"Run workflow"** 버튼 클릭
3. **"Run workflow"** 확인
4. 실행 로그에서 결과 확인

## 📊 실행 결과 확인

GitHub Actions가 실행되면:
- ✅ 새 콘텐츠가 WordPress에 자동 발행됩니다
- ✅ 데이터베이스 (`data/published_topics.db`)가 자동으로 업데이트됩니다
- ✅ 로그 파일이 생성되고 저장소에 커밋됩니다
- ✅ Artifacts에서 상세 로그를 다운로드할 수 있습니다

## 🔧 문제 해결

### Secrets가 설정되지 않은 경우
```
Error: Missing environment variables: ANTHROPIC_API_KEY
```
→ GitHub Secrets가 올바르게 설정되었는지 확인하세요.

### WordPress 인증 실패
```
Error: Authentication failed
```
→ WordPress Application Password가 올바르게 생성되고 입력되었는지 확인하세요.

### 저장소에 push 권한이 없는 경우
```
Error: Permission denied
```
→ Settings > Actions > General > Workflow permissions에서
   "Read and write permissions"를 활성화하세요.

## 📝 주의사항

- `.env` 파일은 절대 GitHub에 푸시하지 마세요 (`.gitignore`에 포함되어 있음)
- API 키는 반드시 GitHub Secrets로만 관리하세요
- 로컬에서 테스트할 때는 `.env` 파일을 사용하고, GitHub Actions에서는 Secrets를 사용합니다

## 🎯 추가 기능

### 스케줄 변경하기

`.github/workflows/auto-publish.yml` 파일의 cron 설정을 수정:

```yaml
schedule:
  - cron: '0 1 * * *'   # 10 AM KST (01:00 UTC)
  - cron: '0 9 * * *'   # 6 PM KST (09:00 UTC)
```

cron 형식: `분 시 일 월 요일` (UTC 기준)

### 수동 실행

언제든지 Actions 탭에서 "Run workflow" 버튼으로 수동 실행 가능합니다.

---

## ✨ 완료!

이제 Claude Code를 실행하지 않아도 매일 자동으로 콘텐츠가 발행됩니다! 🎉
