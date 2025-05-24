import openai
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# API anahtarını ortam değişkeninden al
api_key = os.getenv("OPENAI_API_KEY")

# Yeni API istemcisi ile bağlantı kur
client = openai.OpenAI(api_key=api_key)

def reklam_olustur(urun_tipi, renk, fiyat):
    prompt = f"""Tesettür kadın giyim sektöründe {urun_tipi}, rengi {renk}, fiyatı {fiyat} olan bir ürün için 3 farklı reklam metni öner:
1. Duygusal anlatımlı
2. Kampanya odaklı
3. Kısa ve vurucu"""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

# Test
print(reklam_olustur("Triko Elbise", "Gri", "799 TL"))
