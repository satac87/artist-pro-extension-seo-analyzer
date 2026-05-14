import re, httpx
def analyze(url: str) -> dict:
    r = httpx.get(url, timeout=15, follow_redirects=True)
    html = r.text
    title = re.search(r"<title>(.*?)</title>", html, re.I)
    desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
    h1 = len(re.findall(r"<h1[^>]*>", html, re.I))
    img = len(re.findall(r"<img(?!.*?alt=)", html, re.I))
    score = 100
    if not title: score -= 20
    if not desc: score -= 20
    if h1 == 0: score -= 10
    score -= img * 2
    return {"url":url,"status":r.status_code,"title":title.group(1)if title else"MISSING","meta_description":desc.group(1)if desc else"MISSING","h1_count":h1,"images_without_alt":img,"load_time_ms":round(r.elapsed.total_seconds()*1000),"score":max(0,score)}
