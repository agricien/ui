import requests
url = "https://agricien-my.sharepoint.com/:f:/p/edgar_mendez/IgBZVjiP8iH8T5-RWYIelhgQAf2HJ1IftQkF7T2TWPNTR4U?e=tDuSgV&download=1"
try:
    r = requests.get(url, timeout=10)
    print(f"Status Code: {r.status_code}")
    print(f"Content-Type: {r.headers.get('Content-Type')}")
    print(f"Content length: {len(r.content)}")
    print(f"First 100 bytes: {r.content[:100]}")
except Exception as e:
    print(f"Error: {e}")
