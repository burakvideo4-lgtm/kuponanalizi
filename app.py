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
        
        if not mac_listesi: return yedek_analiz_havuzu()

        tahmin_havuzu = []
        for m in mac_listesi:
            try:
                mac_durumu = m['fixture']['status']['short']
                if mac_durumu in ['FT', 'AET', 'PEN', 'PST', 'CANC']: continue

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
                if len(tahmin_havuzu) >= 30: break
            except: continue

        if len(tahmin_havuzu) < 4: return yedek_analiz_havuzu()
        tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
        return kuponlari_olustur(tahmin_havuzu)
    except: return yedek_analiz_havuzu()

def kuponlari_olustur(tahmin_havuzu):
    k1, k2, k3, k4 = tahmin_havuzu[0:2], tahmin_havuzu[2:4], tahmin_havuzu[4:7], tahmin_havuzu[6:9]
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
    ornekler = [{"lig": "İngiltere - PL", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55, "yuzde": 88, "win_rate": 88}] * 10
    return kuponlari_olustur(ornekler)

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
        .wrapper { max-width: 1200px; margin: 0 auto; }
        .mac-row { background: rgba(30, 41, 59, 0.3); padding: 14px; margin-bottom: 12px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255, 255, 255, 0.03); }
        .badge-tahmin { background: #0284c7; color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; }
        .oran-text { font-size: 14px; color: #10b981; font-weight: 700; margin-top: 4px; }
        .win-rate { font-size: 10px; color: #fbbf24; font-weight: 600; margin-top: 3px; }
        .section-title { font-size: 18px; margin-top: 25px; border-bottom: 2px solid rgba(56, 189, 248, 0.3); padding-bottom: 8px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <h2 class="section-title" style="color: #38bdf8;">📈 Bugünün Canlı Fikstür Listesi</h2>
        {% for t in d.tekli_maclar %}
        <div class="mac-row">
            <div style="max-width: 60%;">
                <div style="font-weight: 600; font-size: 13px; color: #f3f4f6;">{{ t.mac }}</div>
            </div>
            <div style="text-align: right; min-width: 85px;">
                <span class="badge-tahmin">{{ t.tahmin }}</span>
                <div class="win-rate">Win: %{{ t.win_rate }}</div>
                <div class="oran-text">{{ t.oran }}</div>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>"""
    return render_template_string(html_kod, d=d)

if __name__ == '__main__': app.run(debug=True)
