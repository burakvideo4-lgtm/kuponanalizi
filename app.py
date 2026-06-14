from flask import Flask, render_template_string
import requests
import random
from datetime import datetime

app = Flask(__name__)

API_KEY = "999e0bfd03e0268f0ad00d6619da543f"

def bot_analiz_motoru():
    bugun = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={bugun}"
    
    headers = {
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'x-rapidapi-key': API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if not data.get("response") or len(data["response"]) < 3:
            return sahte_veri_uret()
            
        mac_listesi = data["response"]
        tahmin_havuzu = []
        
        for m in mac_listesi:
            ev = m['teams']['home']['name']
            deplasman = m['teams']['away']['name']
            lig = m['league']['name']
            
            tahmin_tipleri = ["MS 1", "MS 2", "2.5 Üst", "KG Var"]
            secilen_tahmin = random.choice(tahmin_tipleri)
            
            # Gerçekçi oran ve buna bağlı mantıklı kazanma yüzdesi hesabı
            oran = round(random.uniform(1.35, 2.20), 2)
            
            # Oran düştükçe kazanma yüzdesi artar mantığı (Yapay zeka simülasyonu)
            if oran < 1.50:
                yuzde = random.randint(82, 93)
            elif oran < 1.80:
                yuzde = random.randint(70, 81)
            else:
                yuzde = random.randint(55, 69)
            
            tahmin_havuzu.append({
                "lig": lig,
                "mac": f"{ev} - {deplasman}",
                "tahmin": secilen_tahmin,
                "oran": oran,
                "yuzde": yuzde
            })
            
        # Yüzdesi en yüksek olanları (en güvenlileri) başa alıyoruz
        tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
        
        kupon_2li = tahmin_havuzu[:2] if len(tahmin_havuzu) >= 2 else tahmin_havuzu
        kupon_3lu = tahmin_havuzu[2:5] if len(tahmin_havuzu) >= 5 else tahmin_havuzu
        
        oran_2li = round(kupon_2li[0]['oran'] * kupon_2li[1]['oran'], 2) if len(kupon_2li) == 2 else 2.10
        oran_3lu = round(kupon_3lu[0]['oran'] * kupon_3lu[1]['oran'] * kupon_3lu[2]['oran'], 2) if len(kupon_3lu) == 3 else 4.50
        
        # Kuponların ortalama güven yüzdesi
        guven_2li = round(sum(p['yuzde'] for p in kupon_2li) / len(kupon_2li)) if kupon_2li else 0
        guven_3lu = round(sum(p['yuzde'] for p in kupon_3lu) / len(kupon_3lu)) if kupon_3lu else 0
        
        return {
            "tekli_maclar": tahmin_havuzu[:6],
            "kupon_2li": kupon_2li,
            "oran_2li": oran_2li,
            "guven_2li": guven_2li,
            "kupon_3lu": kupon_3lu,
            "oran_3lu": oran_3lu,
            "guven_3lu": guven_3lu
        }
        
    except Exception as e:
        return sahte_veri_uret()

def sahte_veri_uret():
    ornekler = [
        {"lig": "İngiltere Premier Lig", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55, "yuzde": 88},
        {"lig": "İspanya La Liga", "mac": "Real Madrid - Atletico Madrid", "tahmin": "2.5 Üst", "oran": 1.68, "yuzde": 82},
        {"lig": "İtalya Serie A", "mac": "Inter - AC Milan", "tahmin": "KG Var", "oran": 1.72, "yuzde": 76},
        {"lig": "Almanya Bundesliga", "mac": "Bayern Munich - Dortmund", "tahmin": "MS 1", "oran": 1.48, "yuzde": 89},
        {"lig": "Fransa Ligue 1", "mac": "PSG - Monaco", "tahmin": "2.5 Üst", "oran": 1.60, "yuzde": 81},
        {"lig": "Türkiye Trendyol Süper Lig", "mac": "Galatasaray - Beşiktaş", "tahmin": "KG Var", "oran": 1.65, "yuzde": 79}
    ]
    return {
        "tekli_maclar": ornekler,
        "kupon_2li": ornekler[:2],
        "oran_2li": 2.60,
        "guven_2li": 85,
        "kupon_3lu": ornekler[2:5],
        "oran_3lu": 4.88,
        "guven_3lu": 78
    }

@app.route('/')
def ana_sayfa():
    data = bot_analiz_motoru()
    
    html_kod = """
    <html>
        <head>
            <title>AI Analiz & Kupon Motoru</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #0b0f19; color: #f1f5f9;">
            
            <h1 style="text-align: center; color: #38bdf8; margin-top: 20px; font-size: 28px;">📊 AI PREMIUM TAHMİN MOTORu v4.0 🤖
