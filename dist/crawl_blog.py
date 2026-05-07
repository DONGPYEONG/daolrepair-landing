import urllib.request
import json
import re
import time

BLOG_ID = "applerepair2"

def fetch_url(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Referer': 'https://blog.naver.com/',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  오류: {e}")
        return ""

def get_post_list():
    posts = []
    print("글 목록 수집 중...")
    for page in range(1, 20):
        url = f"https://blog.naver.com/{BLOG_ID}?Redirect=Log&amp;logNo=0&currentPage={page}"
        url2 = f"https://blog.naver.com/PostList.naver?blogId={BLOG_ID}&currentPage={page}"

        for u in [url2, url]:
            html = fetch_url(u)
            if not html:
                continue

            # 여러 패턴으로 logNo 찾기
            lognos = re.findall(r'logNo=(\d{8,})', html)
            lognos += re.findall(r'"logNo":"(\d{8,})"', html)
            lognos += re.findall(r'log_no=(\d{8,})', html)
            lognos = list(dict.fromkeys(lognos))  # 중복 제거

            titles_raw = re.findall(r'"title"\s*:\s*"([^"]{2,100})"', html)

            if lognos:
                for i, logno in enumerate(lognos):
                    if not any(p['logno'] == logno for p in posts):
                        title = titles_raw[i] if i < len(titles_raw) else f"글_{logno}"
                        posts.append({"logno": logno, "title": title})
                print(f"  {page}페이지: 누적 {len(posts)}개")
                break

        if page > 3 and len(posts) == 0:
            break
        time.sleep(0.8)

    return posts

def get_post_content(logno):
    urls = [
        f"https://blog.naver.com/{BLOG_ID}/{logno}",
        f"https://m.blog.naver.com/{BLOG_ID}/{logno}",
    ]
    for url in urls:
        html = fetch_url(url)
        if not html:
            continue
        # 스크립트/스타일 제거
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        # 본문 영역 추출 시도
        body_match = re.search(r'se-main-container.*?</div>', html, re.DOTALL)
        if body_match:
            html = body_match.group(0)
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 100:
            return text[:3000]
    return ""

def main():
    print(f"=== 다올리페어 블로그 크롤링 시작 ===")
    print(f"블로그: blog.naver.com/{BLOG_ID}\n")

    # 방법 1: 글 목록 자동 수집
    posts = get_post_list()

    # 방법 2: 글 목록 못 찾으면 직접 입력 안내
    if not posts:
        print("\n자동 수집이 안 됩니다.")
        print("블로그에서 글 번호(logNo)를 직접 입력해주세요.")
        print("예: blog.naver.com/applerepair2/223456789 → 223456789 이 숫자")
        print("글 번호를 쉼표로 구분해서 입력하세요 (엔터로 완료):")
        raw = input("> ").strip()
        if raw:
            lognos = [x.strip() for x in raw.split(',') if x.strip().isdigit()]
            posts = [{"logno": l, "title": f"글_{l}"} for l in lognos]

    if not posts:
        print("글을 찾지 못했습니다.")
        return

    print(f"\n총 {len(posts)}개 글 발견")
    print("본문 수집 중...")

    results = []
    for i, post in enumerate(posts):
        print(f"  [{i+1}/{len(posts)}] {post['title'][:40]}")
        content = get_post_content(post['logno'])
        results.append({
            "title": post['title'],
            "url": f"https://blog.naver.com/{BLOG_ID}/{post['logno']}",
            "content": content
        })
        time.sleep(1)

    # JSON 저장
    with open("blog_data.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 요약 텍스트 저장
    with open("blog_summary.txt", 'w', encoding='utf-8') as f:
        f.write(f"다올리페어 블로그 분석 데이터 — 총 {len(results)}개 글\n\n")
        for r in results:
            f.write(f"=== {r['title']} ===\n")
            f.write(f"URL: {r['url']}\n")
            f.write(f"{r['content'][:500]}\n\n")

    print(f"\n✅ 완료! {len(results)}개 글 저장됨")
    print(f"파일: blog_summary.txt, blog_data.json")

if __name__ == "__main__":
    main()
