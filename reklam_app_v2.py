import streamlit as st
import openai
import os
from dotenv import load_dotenv
import random
import pandas as pd

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def avantaj_excel_yukle(dosya_adi, kategori_etiketi=None):
    df = pd.read_excel(dosya_adi)
    if kategori_etiketi:
        df = df[df['kategori'] == kategori_etiketi]
    return df['varyasyon_metni'].tolist()

st.title("🧠 Reklam Metni Üretici v2 – Tesettür Giyim")

st.subheader("📌 Temel Bilgiler")
site = st.text_input("Web Siteniz (örn: www.meysadesign.com)")
kategori = st.selectbox("Kategori", [
    "Tüm Ürünler", "En Yeniler", "Üst Giyim", "Alt Giyim", "Dış Giyim", "Takımlar", "Elbiseler",
    "Tesettür Triko", "Bluz", "Jile", "Sweat", "Hırka", "Gömlek", "Kazak", "Tunik",
    "Pantolon", "Eşofman Altı", "Etek", "Jean", "Kürk", "Ceket", "Mont", "Yelek",
    "Kaban", "Trençkot", "Kimono", "Merserize", "Triko Takım", "Triko Elbise",
    "Abiye", "Ferace", "Namaz Elbisesi", "Son Kalanlar"
])
urun_adi = st.text_input("Ürün İsmi (Opsiyonel)", "")

kampanya_donemi = st.selectbox("Kampanya Dönemi (Opsiyonel)", [
    "Belirtilmedi", "Ramazan", "Bayram", "Yılbaşı", "11.11 İndirimi",
    "Kasım Fırsatları", "Anneler Günü", "Kadınlar Günü", "Ramazan Bayramı",
    "Kurban Bayramı", "Sevgililer Günü", "1 Mayıs İşçi Bayramı",
    "29 Ekim Cumhuriyet Bayramı", "23 Nisan Ulusal Egemenlik ve Çocuk Bayramı",
    "24 Kasım Öğretmenler Günü", "Kandil Günleri", "Kadir Gecesi",
    "Kış Sezonu", "Yaz İndirimi"
])
kampanya_turu = st.text_input("Kampanya Türü (2 al 1 öde, %X indirim, vb.) (Opsiyonel)", "")

st.subheader("📌 Teslimat & İade Avantajları")
iade_var = st.radio("İade veya değişim mevcut mu?", ("Evet", "Hayır"))
iade_suresi = ""
if iade_var == "Evet":
    iade_suresi = st.text_input("İade / Değişim süresi (gün olarak girin)", "14")

aynigun_kargo = st.checkbox("Aynı gün kargo seçeneği sunuluyor mu?")
kapida_odeme = st.checkbox("Kapıda ödeme mevcut mu?")
ucretsiz_kargo = st.radio("Ücretsiz kargo politikası:", ("Yok", "Tüm siparişlerde ücretsiz", "Belirli tutar üzeri ücretsiz"))
kargo_limit = ""
if ucretsiz_kargo == "Belirli tutar üzeri ücretsiz":
    kargo_limit = st.text_input("Kaç TL üzeri ücretsiz olsun?", "750")

st.subheader("📌 Reklam Metni Özellikleri")
metin_sayisi = st.slider("Kaç farklı reklam metni oluşturulsun?", 1, 10, 5)

if st.button("🎯 Metinleri Oluştur"):
    with st.spinner("Metinler DPU-AI ile hazırlanıyor..."):
        kampanya_notu = f"{kampanya_donemi} dönemi kampanyası" if kampanya_donemi != "Belirtilmedi" else ""
        kampanya_aciklama = kampanya_turu if kampanya_turu else f"{kategori} için genel kampanya"

        teknik_ozet_listesi = []

        for _ in range(metin_sayisi):
            avantajlar = []
            if iade_var == "Evet":
                iade_list = avantaj_excel_yukle("avantaj_iade.xlsx")
                avantajlar += [secenek.replace("{gun}", iade_suresi) for secenek in random.sample(iade_list, k=min(2, len(iade_list)))]

            if aynigun_kargo:
                kargo_list = avantaj_excel_yukle("avantaj_kargo.xlsx")
                avantajlar += random.sample(kargo_list, k=min(2, len(kargo_list)))

            if kapida_odeme:
                odeme_list = avantaj_excel_yukle("avantaj_odeme.xlsx")
                avantajlar += random.sample(odeme_list, k=min(2, len(odeme_list)))

            if ucretsiz_kargo != "Yok":
                kargo_ucretsiz_list = avantaj_excel_yukle("avantaj_ucretsiz_kargo.xlsx")
                avantajlar += [secenek.replace("{limit}", kargo_limit) for secenek in random.sample(kargo_ucretsiz_list, k=min(2, len(kargo_ucretsiz_list)))]

            cta_list = avantaj_excel_yukle("avantaj_cta.xlsx")
            avantajlar += [random.choice(cta_list).replace("{site}", site)]

            random.shuffle(avantajlar)
            teknik_ozet = "\n".join([f"- {a}" for a in avantajlar])
            teknik_ozet_listesi.append(teknik_ozet)

        prompt = f"""
Sen deneyimli bir dijital reklam metni yazarı olarak aşağıdaki verilerle {metin_sayisi} farklı reklam metni üret:

ÜRÜN: {kategori}
ÜRÜN ADI: {urun_adi if urun_adi else 'Ürün adı belirtilmedi'}
KAMPANYA: {kampanya_aciklama}
KAMPANYA DÖNEMİ: {kampanya_notu if kampanya_notu else 'Belirtilmedi'}

Kurallar:
- Her metin farklı ton ve yaklaşımla yazılmalı (duygusal, fırsatçı, mizahi, sade, vurucu)
- Başlıklar emojiyle başlamalı
- Metin sonunda teslimat ve ödeme avantajlarını her seferinde değiştirerek, alt alta, sıralaması karışık, uzunluğu değişen ve farklı kelimelerle ifade edilmiş şekilde yaz
- Bu avantajlar metin içinde tekrar eden değil, yaratıcı, çeşitlendirilmiş cümleler veya madde madde olabilir
- Avantajların her biri emoji ile başlamalı
- Metin sonunda {site} adresine yönlendirici bir cümle olmalı

TEKNİK DETAYLAR:
{chr(10).join(teknik_ozet_listesi)}
"""

        response1 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.success("✅ Reklam Metinleri Oluştu!")
        reklam_metinleri = response1.choices[0].message.content
        st.text_area("📝 Reklam Metinleri", value=reklam_metinleri, height=400)
