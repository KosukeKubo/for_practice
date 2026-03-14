import requests
import os

def get_news(key_word: str="AI", n: int=5):
    url = "https://newsapi.org/v2/everything"
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
    
    params = {
        "q": key_word,
        "searchIn": "title",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    print(f"{data=}")

    # Discordに送るための「1つのメッセージ（文字列）」を組み立てる
    message = f"📢 今日の【{key_word}】ニュース上位{n}件をお届けします！\n\n"
    
    # data["articles"]が空の場合のエラー回避
    articles = data.get("articles", [])
    print(f"{articles=}")
    for article in articles[:n]:
        title = article["title"]
        url = article["url"]
        message += f"🔹 {title}\n{url}\n\n"

    return message

def send_discord(message_text):
    DISCORD_URL = os.environ.get("DISCORD_AI_NEWS_COLLECTOR_URL")
    
    data = {
        "content": message_text
    }
    
    response = requests.post(DISCORD_URL, json=data)
    
    if response.status_code == 204:
        print("Discordへの送信に成功しました。")
    else:
        print(f"送信失敗: {response.status_code}")

if __name__ == "__main__":
    # 1. ニュースを取得して文字列にまとめる
    content = get_news("AI", 5)
    
    # 2. まとめた文字列を送信する
    send_discord(content)
