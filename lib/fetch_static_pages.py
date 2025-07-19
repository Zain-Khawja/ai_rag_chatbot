import requests
import json
from bs4 import BeautifulSoup

PAGES = {
    "Home": "https://aaasafedubai.com/",
    "About Us": "https://aaasafedubai.com/about-us/",
    "Privacy Policy": "https://aaasafedubai.com/privacy-policy/",
    "Terms & Conditions": "https://aaasafedubai.com/terms-and-conditions/",
    "Contact Us": "https://aaasafedubai.com/contact/",
}

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n").strip()

def fetch_pages():
    data = []
    for title, url in PAGES.items():
        print(f"Fetching {title}...")
        res = requests.get(url)
        if res.status_code == 200:
            content = clean_html(res.text)
            data.append({
                "title": title,
                "body": content
            })
        else:
            print(f"Failed: {url} - {res.status_code}")
    with open("static_pages.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    fetch_pages()
