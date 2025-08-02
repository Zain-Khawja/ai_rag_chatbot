# fetch_static_pages.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import requests, json
from bs4 import BeautifulSoup

PAGES = {
    "Home": "https://aaasafedubai.com/",
    "About Us": "https://aaasafedubai.com/about-us/",
    "Privacy Policy": "https://aaasafedubai.com/privacy-policy/",
    "Terms & Conditions": "https://aaasafedubai.com/terms-and-conditions/",
    "Contact Us": "https://aaasafedubai.com/contact/",
}

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
os.makedirs(data_dir, exist_ok=True)

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove navigation, footer, and other non-content elements
    for element in soup.select("nav, footer, header, .menu, .navigation, .footer, .header"):
        element.decompose()
        
    # Find main content area
    main_content = soup.find("main") or soup.find("article") or soup.find("div", class_="content")
    if main_content:
        content = main_content
    else:
        content = soup
        
    # Clean up whitespace and formatting
    text = content.get_text(separator="\n").strip()
    # Remove multiple newlines
    text = "\n".join(line.strip() for line in text.split("\n") if line.strip())
    return text

def fetch_pages():
    data = []
    for title, url in PAGES.items():
        print(f"Fetching {title}...")
        res = requests.get(url)
        if res.status_code == 200:
            content = clean_html(res.text)
            data.append({"title": title, "body": content})
        else:
            print(f"Failed: {url} - {res.status_code}")

    with open(os.path.join(data_dir, "static_pages.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    fetch_pages()
