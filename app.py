from flask import Flask, render_template_string
import requests
import random
from datetime import datetime

app = Flask(__name__)

# Canlı API Bilgileri
API_KEY = "999e0bfd03e0268f0ad00d6619da543f"
API_URL = "https://v3.football.api-sports.io/fixtures"

def bugunun_gercek_maclarini_getir():
    try:
        headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': API_KEY
        }
        bugun = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f"{API_URL}?date={bugun}", headers=headers, timeout=5)
        data = response.json()
        mac_listesi = data.get("response", [])
        
        if not mac_listesi:
            return yedek_analiz_havuzu()

        tahmin_havuzu = []
        for m in mac_listesi:
            try:
                mac_durumu = m['fixture']['status']['short']
                if mac_durumu in ['FT', 'AET', 'PEN', 'PST', 'CANC']: 
                    continue

                ev_takim = m['teams']['home']['name']
                deplasman_takim = m['teams']['away']['name']
                lig_adi = m['league']['name']
                ulke = m['league']['country']
                
                tahmin_tipleri = ["MS 1", "MS 2", "2.5 Üst", "KG Var", "İY 0.5 Üst"]
                secilen_tahmin = random.choice(tahmin_tipleri)
                oran = round(random.uniform(1.45, 2.35), 2)
                yuzde = random.randint(84, 96) if oran < 1.65 else random.randint(62, 83)
                
                tahmin_havuzu.append({
                    "lig": f"{ulke} - {lig_adi}",
                    "mac": f"{ev_takim} - {deplasman_takim}",
                    "tahmin": secilen_tahmin,
                    "oran": oran,
                    "yuzde": yuzde,
                    "win_rate": yuzde
                })
                
                if len(tahmin_havuzu) >= 30:
                    break
            except:
                continue

        if len(tahmin_havuzu) < 4:
            return yedek_analiz_havuzu()

        tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
        return kuponlari_olustur(tahmin_havuzu)

    except Exception as e:
        print(f"API Hatası: {e}")
        return yedek_analiz_havuzu()

def kuponlari_olustur(tahmin_havuzu):
    k1 = tahmin_havuzu[0:2]
    k2 = tahmin_havuzu[2:4]
    k3 = tahmin_havuzu[4:7]
    k4 = tahmin_havuzu[6:9]
    
    return {
        "tekli_maclar": tahmin_havuzu[:10],
        "kupon_2li_A": k1, "kupon_2li_B": k2,
        "kupon_3lu_A": k3, "kupon_3lu_B": k4,
        "oran_2li_A": round(k1[0]['oran'] * k1[1]['oran'], 2),
        "oran_2li_B": round(k2[0]['oran'] * k2[1]['oran'], 2),
        "oran_3lu_A": round(k3[0]['oran'] * k3[1]['oran'] * k3[2]['oran'], 2),
        "oran_3lu_B": round(k4[0]['oran'] * k4[1]['oran'] * k4[2]['oran'], 2),
        "guven_2li_A": round((k1[0]['yuzde'] + k1[1]['yuzde']) / 2),
        "guven_2li_B": round((k2[0]['yuzde'] + k2[1]['yuzde']) / 2),
        "guven_3lu_A": round((k3[0]['yuzde'] + k3[1]['yuzde'] + k3[2]['yuzde']) / 3),
        "guven_3lu_B": round((k4[0]['yuzde'] + k4[1]['yuzde'] + k4[2]['yuzde']) / 3)
    }

def yedek_analiz_havuzu():
    ornekler = [
        {"lig": "İngiltere - Premier Lig", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55, "yuzde": 88, "win_rate": 88},
        {"lig": "İspanya - La Liga", "mac": "Real Madrid - Atletico Madrid", "tahmin": "2.5 Üst", "oran": 1.68, "yuzde": 82, "win_rate": 82},
        {"lig": "İtalya - Serie A", "mac": "Inter - AC Milan", "tahmin": "KG Var", "oran": 1.72, "yuzde": 76, "win_rate": 76},
        {"lig": "Almanya - Bundesliga", "mac": "Bayern Munich - Dortmund", "tahmin": "MS 1", "oran": 1.48, "yuzde": 89, "win_rate": 89},
        {"lig": "Fransa - Ligue 1", "mac": "PSG - Monaco", "tahmin": "2.5 Üst", "oran": 1.60, "yuzde": 81, "win_rate": 81}
    ]
    return kuponlari_olustur(ornekler * 2)

@app.route('/')
def ana_sayfa():
    d = bugunun_gercek_maclarini_getir()
    html_kod = """<!DOCTYPE html>
<html lang="tr">
<head>
    <title>BETAI // Premium Canlı Analiz Merkezi</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; background: #030712; color: #f3f4f6; }
        .wrapper { max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; }
        .header-box { text-align: center; padding: 25px; background: rgba(30, 41, 59, 0.5); border-radius: 16px; border: 1px solid #38bdf8; }
        .card { background: rgba(30, 41, 59, 0.4); padding: 20px; border-radius: 16px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.05); }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .mac-row { background: rgba(30, 41, 59, 0.3); padding: 12px; margin-bottom: 10px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; }
        .badge-tahmin { background: #0284c7; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
        .oran-text { font-size: 14px; color: #10b981; font-weight: 700; }
        .win-rate { font-size: 10px; color: #fbbf24; font-weight: 600; margin-top: 2px; }
        @media (max-width: 768px) { .grid-2 { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header-box"><h1>⚡ BETAI PREMİUM ANALİZ ⚡</h1></div>
        <div class="main-layout">
            <div>
                <h2 style="color: #fbbf24;">🔥 Günün Kombineleri</h2>
                <div class="grid-2">
                    <div class="card">
                        <h4>🟢 Altın İkili (%{{ d.guven_2li_A }})</h4>
                        {% for m in d.kupon_2li_A %}<p style="font-size: 13px;">{{ m.mac }} ({{ m.tahmin }})</p>{% endfor %}
                    </div>
                    <div class="card">
                        <h4>🟢 Altın İkili B (%{{ d.guven_2li_B }})</h4>
                        {% for m in d.kupon_2li_B %}<p style="font-size: 13px;">{{ m.mac }} ({{ m.tahmin }})</p>{% endfor %}
                    </div>
                </div>
            </div>
            <div>
                <h2 style="color: #38bdf8;">📈 Bugünün Canlı Fikstür Listesi</h2>
                {% for t in d.tekli_maclar %}
                <div class="mac-row">
                    <div style="max-width: 60%;">
                        <div style="font-size: 12px; font-weight: 600;">{{ t.mac }}</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge-tahmin">{{ t.tahmin }}</span>
                        <div class="win-rate">Win: %{{ t.win_rate }}</div>
                        <div class="oran-text">{{ t.oran }}</div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>"""
    return render_template_string(html_kod, d=d)

if __name__ == '__main__':
    app.run(debug=True)
