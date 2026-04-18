import feedparser
import json
import os
from datetime import datetime

# Configuración de los feeds RSS a monitorear
FEEDS = {
    "Tecnología": [
        "https://feeds.feedburner.com/TechCrunch/",
        "https://www.theverge.com/rss/index.xml"
    ],
    "Noticias": [
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best"
    ],
    "Agricultura": [
        "https://www.fao.org/news/rss-feeds/en/",
        "https://phys.org/rss-feed/biology-news/agriculture/"
    ]
}

def parse_feeds():
    news_items = []
    
    for category, urls in FEEDS.items():
        print(f"--- Procesando categoría: {category} ---")
        for url in urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]: # Limitar a las últimas 10 noticias por fuente
                    # Extraer imagen si existe en media:content o enclosure
                    img_url = ""
                    if 'media_content' in entry:
                        img_url = entry.media_content[0]['url']
                    elif 'links' in entry:
                        for link in entry.links:
                            if 'image' in link.get('type', ''):
                                img_url = link.href
                                break
                    
                    news_items.append({
                        "category": category,
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.get('summary', '')[:200] + "...",
                        "published": entry.get('published', datetime.now().strftime("%Y-%m-%d")),
                        "thumbnail": img_url if img_url else "https://picsum.photos/seed/news/400/250"
                    })
            except Exception as e:
                print(f"Error parseando {url}: {e}")
                
    # Ordenar por fecha (intentar parsear, si no mantener orden)
    return news_items

def save_data(data):
    # Asegurar que el directorio de datos existe
    if not os.path.exists("data"):
        os.makedirs("data")
        
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Base de datos actualizada con {len(data)} noticias.")

if __name__ == "__main__":
    articles = parse_feeds()
    save_data(articles)
