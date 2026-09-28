import json
import urllib.request
from bs4 import BeautifulSoup

def crawl():
    # Siteleri oku
    with open('sites.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    
    database = []

    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req, timeout=5).read()
            soup = BeautifulSoup(html, 'html.parser')
            
            title = soup.title.string.strip() if soup.title else url
            
            # Meta description çek
            desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
            desc = desc_tag['content'].strip() if desc_tag and 'content' in desc_tag.attrs else "Açıklama bulunamadı."
            
            database.append({
                "title": title,
                "url": url,
                "desc": desc
            })
            print(f"Başarıyla tarandı: {url}")
        except Exception as e:
            print(f"Hata ({url}): {e}")

    # Sonuçları veritabanına yaz
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    crawl()
