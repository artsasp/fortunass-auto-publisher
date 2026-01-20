# Tistory 연동 설정 가이드

## 1. Tistory Access Token 발급

### Step 1: Tistory 앱 등록
1. https://www.tistory.com/guide/api/manage/register 접속
2. 로그인
3. 앱 등록:
   - 서비스명: Content Publisher
   - 설명: 자동 콘텐츠 발행 시스템
   - 서비스 URL: http://localhost
   - Callback: http://localhost/callback

### Step 2: Client ID 및 Secret 확인
앱 등록 후 받은:
- Client ID (App ID)
- Secret Key

### Step 3: Access Token 발급

#### 방법 1: 브라우저로 직접 발급
```
https://www.tistory.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http://localhost/callback&response_type=code
```

1. 위 URL에서 `{CLIENT_ID}`를 본인의 Client ID로 변경
2. 브라우저에서 접속
3. 권한 승인
4. Redirect된 URL에서 `code` 파라미터 복사
   예: `http://localhost/callback?code=XXXXX`

5. Access Token 받기:
```bash
curl "https://www.tistory.com/oauth/access_token?client_id={CLIENT_ID}&client_secret={SECRET_KEY}&redirect_uri=http://localhost/callback&code={CODE}&grant_type=authorization_code"
```

결과:
```
access_token=XXXXXXXXXXXXXXX
```

#### 방법 2: Python으로 발급
```python
import requests

# Step 1: Authorization Code 받기 (브라우저에서 수동)
auth_url = f"https://www.tistory.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http://localhost/callback&response_type=code"
print(f"브라우저로 이동: {auth_url}")
code = input("Code 입력: ")

# Step 2: Access Token 받기
token_url = "https://www.tistory.com/oauth/access_token"
params = {
    "client_id": CLIENT_ID,
    "client_secret": SECRET_KEY,
    "redirect_uri": "http://localhost/callback",
    "code": code,
    "grant_type": "authorization_code"
}

response = requests.get(token_url, params=params)
print(response.text)  # access_token=XXXXX
```

## 2. .env 파일 설정

```bash
cp .env.example .env
```

`.env` 파일 편집:
```env
# Claude API
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Tistory
TISTORY_ACCESS_TOKEN=your_access_token_here
TISTORY_BLOG_NAME=myblog

# 공개 설정 (0=비공개, 3=공개)
TISTORY_VISIBILITY=0
```

**TISTORY_BLOG_NAME:**
- Tistory 블로그 주소가 `https://myblog.tistory.com` 이면
- `TISTORY_BLOG_NAME=myblog`

## 3. 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
python main.py
```

## 4. 실행 흐름

```
main.py
 ├─ 1. Topic 생성 (MBTI × Love × Tarot)
 ├─ 2. Claude API 호출 → 콘텐츠 생성
 ├─ 3. SEO 검증 + 자동 sanitize
 ├─ 4. Markdown → HTML 변환
 └─ 5. Tistory Open API로 발행 ✅
        ↓
   Tistory 블로그에 자동 포스팅
```

## 5. Tistory API 참고

### 글쓰기 API
- Endpoint: `POST https://www.tistory.com/apis/post/write`
- Parameters:
  - `access_token`: 필수
  - `blogName`: 필수
  - `title`: 필수
  - `content`: 필수 (HTML)
  - `visibility`: 0(비공개), 1(보호), 3(공개)
  - `category`: 카테고리 ID (선택)
  - `tag`: 쉼표로 구분된 태그 (선택)

### 카테고리 조회 API
- Endpoint: `GET https://www.tistory.com/apis/category/list`
- Parameters:
  - `access_token`: 필수
  - `blogName`: 필수
  - `output`: json

## 6. 문제 해결

### "Invalid access token"
→ Access token 재발급 필요

### "Blog does not exist"
→ TISTORY_BLOG_NAME 확인

### "Permission denied"
→ 앱 권한 재승인 필요

## 7. 공개 발행

비공개에서 공개로 변경:
```env
TISTORY_VISIBILITY=3
```

## 참고 링크
- Tistory Open API: https://tistory.github.io/document-tistory-apis/
- 앱 관리: https://www.tistory.com/guide/api/manage/list
