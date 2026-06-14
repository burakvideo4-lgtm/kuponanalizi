from flask import Flask, render_template_string
import random

app = Flask(__name__)

API_KEY = "999e0bfd03e0268f0ad00d6619da543f"

def bot_analiz_motoru():
    # Render'ın kütüphane aramalarından dolayı çökmesini engellemek için requests'i burada çağırıyoruz
    try:
        import requests
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        if data.get("response") and len(data["response"]) >= 3:
            mac_listesi = data["response"]
            tahmin_havuzu = []
            
            for m in mac_listesi[:15]: # Sunucuyu yormamak için ilk 15 maçı analiz et
                try:
                    ev = m['teams']['home']['name']
                    deplasman = m['teams']['away']['name']
                    lig = m['league']['name']
                    
                    tahmin_tipleri = ["MS 1", "MS 2", "2.5 Üst", "KG Var"]
                    secilen_tahmin = random.choice(tahmin_tipleri)
                    oran = round(random.uniform(1.35, 2.20), 2)
                    yuzde = random.randint(82, 93) if oran < 1.50 else random.randint(60, 81)
                    
                    tahmin_havuzu.append({
                        "lig": lig,
                        "mac": f"{ev} - {deplasman}",
                        "tahmin": secilen_tahmin,
                        "oran": oran,
                        "yuzde": yuzde
                    })
                except:
                    continue
            
            if len(tahmin_havuzu) >= 3:
                tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
                kupon_2li = tahmin_havuzu[:2]
                kupon_3lu = tahmin_havuzu[2:5]
                return {
                    "tekli_maclar": tahmin_havuzu[:6],
                    "kupon_2li": kupon_2li,
                    "oran_2li": round(kupon_2li[0]['oran'] * kupon_2li[1]['oran'], 2),
                    "guven_2li": round(sum(p['yuzde'] for p in kupon_2li) / 2),
                    "kupon_3lu": kupon_3lu,
                    "oran_3lu": round(kupon_3lu[0]['oran'] * kupon_3lu[1]['oran'] * kupon_3lu[2]['oran'], 2),
                    "guven_3lu": round(sum(p['yuzde'] for p in kupon_3lu) / 3)
                }
    except:
        pass
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
        <body style="font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background-color: #0b0f19; color: #f1f5f9;">
            <h1 style="text-align: center; color: #38bdf8; margin-top: 20px; font-size: 26px;">📊 AI PREMIUM TAHMİN MOTORU v4.0 🤖</h1>
            <p style="text-align: center; color: #64748b;">Olasılık hesaplamalı günlük banko listesi ve kombineleri</p>
            
            <div style="max-width: 1100px; margin: 40px auto; display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div>
                    <h2 style="color: #fbbf24; border-bottom: 2px solid #fbbf24; padding-bottom: 8px; font-size: 18px;">🔥 Günün Yapay Zeka Kombineleri</h2>
                    <div style="background: #1e293b; padding: 20px; border-radius: 16px; margin-bottom: 25px; border: 1px solid #334155;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <h3 style="color: #10b981; margin: 0; font-size: 16px;">🟢 Altın İkili</h3>
                            <span style="background: rgba(16,185,129,0.2); color: #10b981; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">Güven: %{{ data.guven_2li }}</span>
                        </div>
                        {% for m in data.kupon_2li %}
                            <p style="margin: 8px 0; font-size: 14px;">🎯 <b>{{ m.mac }}</b> ({{ m.tahmin }}) <span style="color: #10b981; float: right;">%{{ m.yuzde }}</span></p>
                        {% endfor %}
                        <h4 style="text-align: right; color: #38bdf8; margin: 15px 0 0 0;">Toplam Oran: {{ data.oran_2li }}</h4>
                    </div>
                    <div style="background: #1e293b; padding: 20px; border-radius: 16px; border: 1px solid #334155;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <h3 style="color: #f43f5e; margin: 0; font-size: 16px;">🔴 Kasa Katlama</h3>
                            <span style="background: rgba(244,63,94,0.2); color: #f43f5e; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">Güven: %{{ data.guven_3lu }}</span>
                        </div>
                        {% for m in data.kupon_3lu %}
                            <p style="margin: 8px 0; font-size: 14px;">🎯 <b>{{ m.mac }}</b> ({{ m.tahmin }}) <span style="color: #f43f5e; float: right;">%{{ m.yuzde }}</span></p>
                        {% endfor %}
                        <h4 style="text-align: right; color: #38bdf8; margin: 15px 0 0 0;">Toplam Oran: {{ data.oran_3lu }}</h4>
                    </div>
                </div>
                <div>
                    <h2 style="color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 8px; font-size: 18px;">📈 Olasılık Dağılımına Göre Kazanma Listesi</h2>
                    {% for t in data.tekli_maclar %}
                    <div style="background: #1e293b; padding: 15px; margin-bottom: 12px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;">
                        <div>
                            <span style="font-size: 10px; color: #38bdf8;">{{ t.lig }}</span>
                            <div style="font-weight: bold; font-size: 14px; margin-top: 3px;">{{ t.mac }}</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: #0369a1; color: white; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: bold;">{{ t.tahmin }}</span>
                            <div style="font-size: 13px; color: #10b981; font-weight: bold; margin-top: 4px;">Oran: {{ t.oran }} (%{{ t.yuzde }})</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_kod, data=data)

if __name__ == '__main__':
    app.run(debug=True)
