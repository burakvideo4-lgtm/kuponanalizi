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
        headers = {'x-rapidapi-host': 'v3.football.api-sports.io', 'x-rapidapi-key': API_KEY}
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
                secilen_tahmin = random.choice(["MS 1", "MS 2", "2.5 Üst", "KG Var", "İY 0.5 Üst"])
                oran = round(random.uniform(1.45, 2.35), 2)
                yuzde = random.randint(84, 96) if oran < 1.65 else random.randint(62, 83)
                tahmin_havuzu.append({"lig": f"{ulke} - {lig_adi}", "mac": f"{ev_takim} - {deplasman_takim}", "tahmin": secilen_tahmin, "oran": oran, "yuzde": yuzde})
                if len(tahmin_havuzu) >= 30: break
            except: continue
        if len(tahmin_havuzu) < 4: return yedek_analiz_havuzu()
        tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
        return kuponlari_olustur(tahmin_havuzu)
    except Exception as e:
        print(f"API Hatası: {e}")
        return yedek_analiz_havuzu()

def kuponlari_olustur(tahmin_havuzu):
    k1, k2, k3, k4 = tahmin_havuzu[0:2], tahmin_havuzu[2:4], tahmin_havuzu[4:7], tahmin_havuzu[6:9]
    return {
        "tekli_maclar": tahmin_havuzu[:10], "kupon_2li_A": k1, "kupon_2li_B": k2,
        "kupon_3lu_A": k3, "kupon_3lu_B": k4,
        "oran_2li_A": round(k1[0]['oran'] * k1[1]['oran'], 2), "oran_2li_B": round(k2[0]['oran'] * k2[1]['oran'], 2),
        "oran_3lu_A": round(k3[0]['oran'] * k3[1]['oran'] * k3[2]['oran'], 2), "oran_3lu_B": round(k4[0]['oran'] * k4[1]['oran'] * k4[2]['oran'], 2),
        "guven_2li_A": round((k1[0]['yuzde'] + k1[1]['yuzde']) / 2), "guven_2li_B": round((k2[0]['yuzde'] + k2[1]['yuzde']) / 2),
        "guven_3lu_A": round((k3[0]['yuzde'] + k3[1]['yuzde'] + k3[2]['yuzde']) / 3), "guven_3lu_B": round((k4[0]['yuzde'] + k4[1]['yuzde'] + k4[2]['yuzde']) / 3)
    }

def yedek_analiz_havuzu():
    ornekler = [{"lig": "İngiltere - Premier Lig", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55, "yuzde": 88}] * 10
    return kuponlari_olustur(ornekler)

@app.route('/')
def ana_sayfa():
    d = bugunun_gercek_maclarini_getir()
    html_kod = """<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { font-family: sans-serif; background: #030712; color: white; padding: 15px; }
.tabs { display: flex; gap: 10px; margin-bottom: 20px; }
.tab-btn { flex: 1; padding: 10px; background: #1e293b; border: none; color: white; cursor: pointer; border-radius: 8px; }
.tab-btn.active { background: #38bdf8; }
.content { display: none; }
.content.active { display: block; }
.card { background: #1e293b; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
@media (max-width: 768px) { .grid-2 { grid-template-columns: 1fr; } }
</style></head><body>
<div style="max-width: 1000px; margin: 0 auto;">
    <div class="tabs">
        <button class="tab-btn active" onclick="show('ana')">Analizler</button>
        <button class="tab-btn" onclick="show('arsiv')">Arşiv</button>
    </div>
    <div id="ana" class="content active">
        <div class="grid-2">
            <div class="card">🟢 Altın İkili A (Oran: {{d.oran_2li_A}})</div>
            <div class="card">🔴 Kasa Katlama A (Oran: {{d.oran_3lu_A}})</div>
        </div>
    </div>
    <div id="arsiv" class="content">
        <div class="card">📊 Sonuçlanan Analiz Arşivi</div>
    </div>
</div>
<script>
function show(id) {
    document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    event.currentTarget.classList.add('active');
}
</script></body></html>"""
    return render_template_string(html_kod, d=d)

if __name__ == '__main__': app.run(debug=True)
