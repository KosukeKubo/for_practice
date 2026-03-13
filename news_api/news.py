import requests

url = "https://newsapi.org/v2/everything"

params = {
    "q": "AI",
    "searchIn": "title",
    "sortBy": "publishedAt",
    "apiKey":"c1c5efe25ddd4cd79cbaca8efdba7e9d"
}

response = requests.get(url, params)
data = response.json()

for article in data["articles"][:5]:
    print(f"タイトル : {article["title"]}")
    print(f"URL : {article["url"]}")