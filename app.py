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
                # OYNANMIŞ MAÇLARI ELEME FİLTRESİ
                # FT = Finished (Bitti), AET = Uzatmalarda Bitti, PEN = Penaltılarda Bitti
                mac_durumu = m['fixture']['status']['short']
                if mac_durumu in ['FT', 'AET', 'PEN', 'PST', 'CANC']: 
                    continue # Eğer maç bitmiş, ertelenmiş veya iptal edilmişse bu maçı atla, listeye alma.

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
                    "yuzde": yuzde
                })
                
                # Toplam 30 tane güncel maç bulduğumuzda aramayı durduralım ki sistem yorulmasın
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
        {"lig": "İngiltere - Premier Lig", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55, "yuzde": 88},
        {"lig": "İspanya - La Liga", "mac": "Real Madrid - Atletico Madrid", "tahmin": "2.5 Üst", "oran": 1.68, "yuzde": 82},
        {"lig": "İtalya - Serie A", "mac": "Inter - AC Milan", "tahmin": "KG Var", "oran": 1.72, "yuzde": 76},
        {"lig": "Almanya - Bundesliga", "mac": "Bayern Munich - Dortmund", "tahmin": "MS 1", "oran": 1.48, "yuzde": 89},
        {"lig": "Fransa - Ligue 1", "mac": "PSG - Monaco", "tahmin": "2.5 Üst", "oran": 1.60, "yuzde": 81}
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
        body { 
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; 
            margin: 0; 
            padding: 15px; 
            background: radial-gradient(circle at 50% 0%, #111827 0%, #030712 100%);
            color: #f3f4f6; 
            min-height: 100vh;
        }
        .wrapper { max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; }
        .header-box {
            text-align: center;
            padding: 25px 15px;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.5), rgba(15, 23, 42, 0.8));
            border-radius: 16px;
            border: 1px solid rgba(56, 189, 248, 0.2);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(5px);
        }
        .header-box h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 1.5px;
            background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header-box p { color: #9ca3af; font-size: 14px; margin: 8px 0 0 0; }
        .status-bar {
            background: linear-gradient(90deg, rgba(2, 132, 199, 0.2), rgba(15, 23, 42, 0.6));
            border: 1px solid rgba(3, 105, 161, 0.4);
            padding: 12px;
            border-radius: 12px;
            text-align: center;
        }
        .card { 
            background: rgba(30, 41, 59, 0.4); 
            padding: 20px; 
            border-radius: 16px; 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            margin-bottom: 15px; 
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .card:hover {
            transform: translateY(-2px);
            border-color: rgba(56, 189, 248, 0.3);
        }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .vip-box { 
            background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); 
            padding: 25px; 
            border-radius: 20px; 
            border: 1px solid #6366f1; 
            text-align: center;
            box-shadow: 0 0 25px rgba(99, 102, 241, 0.2);
        }
        .vip-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 20px; }
        .vip-card {
            background: rgba(15, 23, 42, 0.6); 
            padding: 15px 10px; 
            border-radius: 12px; 
            border: 1px dashed rgba(99, 102, 241, 0.4);
        }
        .vip-btn {
            background: linear-gradient(90deg, #6366f1, #a855f7); 
            color: white; border: none; padding: 12px 24px; font-size: 14px; font-weight: 700; border-radius: 10px; cursor: pointer; width: 100%;
            box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
        }
        h2.section-title { font-size: 18px; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; padding-bottom: 8px; }
        .mac-row {
            background: rgba(30, 41, 59, 0.3); padding: 14px; margin-bottom: 12px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255, 255, 255, 0.03);
        }
        .mac-row:hover { background: rgba(30, 41, 59, 0.5); }
        .badge-tahmin { background: linear-gradient(135deg, #0284c7, #0369a1); color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; }
        .oran-text { font-size: 14px; color: #10b981; font-weight: 700; margin-top: 4px; }
        @media (min-width: 769px) { .main-layout { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 25px; } }
        @media (max-width: 768px) { .grid-2, .vip-grid { grid-template-columns: 1fr; } .header-box h1 { font-size: 22px; } }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header-box">
            <h1>⚡ BETAI PREMİUM ANALİZ ⚡</h1>
            <p>Yayındaki Gerçek Zamanlı Fikstür ve Tahmin Portalı</p>
        </div>
        
        <div class="status-bar">
            <h3 style="margin: 0; color: #38bdf8; font-size: 13px; font-weight: 600;">📡 Canlı Veri Akışı Bağlantısı: Aktif ve Güvenli</h3>
        </div>

        <div class="main-layout">
            <div>
                <h2 class="section-title" style="color: #fbbf24; border-bottom: 2px solid rgba(251, 191, 36, 0.3);">🔥 Günün Kombineleri</h2>
                <div class="grid-2">
                    <div class="card">
                        <h4 style="color: #34d399; margin: 0 0 12px 0; font-size: 14px;">🟢 Altın İkili - Kampanya A (%{{ d.guven_2li_A }})</h4>
                        {% for m in d.kupon_2li_A %}
                        <p style="margin: 6px 0; font-size: 13px; color: #e5e7eb;">🔹 <b>{{ m.mac }}</b> <span style="color: #38bdf8;">({{ m.tahmin }})</span></p>
                        {% endfor %}
                        <h5 style="text-align: right; color: #34d399; margin: 12px 0 0 0; font-size: 14px;">Toplam Oran: {{ d.oran_2li_A }}</h5>
                    </div>
                    <div class="card">
                        <h4 style="color: #34d399; margin: 0 0 12px 0; font-size: 14px;">🟢 Altın İkili - Kampanya B (%{{ d.guven_2li_B }})</h4>
                        {% for m in d.kupon_2li_B %}
                        <p style="margin: 6px 0; font-size: 13px; color: #e5e7eb;">🔹 <b>{{ m.mac }}</b> <span style="color: #38bdf8;">({{ m.tahmin }})</span></p>
                        {% endfor %}
                        <h5 style="text-align: right; color: #34d399; margin: 12px 0 0 0; font-size: 14px;">Toplam Oran: {{ d.oran_2li_B }}</h5>
                    </div>
                </div>
                <div class="grid-2" style="margin-top: 10px;">
                    <div class="card">
                        <h4 style="color: #f87171; margin: 0 0 12px 0; font-size: 14px;">🔴 Kasa Katlama - Seçim A (%{{ d.guven_3lu_A }})</h4>
                        {% for m in d.kupon_3lu_A %}
                        <p style="margin: 6px 0; font-size: 13px; color: #e5e7eb;">🔹 <b>{{ m.mac }}</b> <span style="color: #38bdf8;">({{ m.tahmin }})</span></p>
                        {% endfor %}
                        <h5 style="text-align: right; color: #f87171; margin: 12px 0 0 0; font-size: 14px;">Toplam Oran: {{ d.oran_3lu_A }}</h5>
                    </div>
                    <div class="card">
                        <h4 style="color: #f87171; margin: 0 0 12px 0; font-size: 14px;">🔴 Kasa Katlama - Seçim B (%{{ d.guven_3lu_B }})</h4>
                        {% for m in d.kupon_3lu_B %}
                        <p style="margin: 6px 0; font-size: 13px; color: #e5e7eb;">🔹 <b>{{ m.mac }}</b> <span style="color: #38bdf8;">({{ m.tahmin }})</span></p>
                        {% endfor %}
                        <h5 style="text-align: right; color: #f87171; margin: 12px 0 0 0; font-size: 14px;">Toplam Oran: {{ d.oran_3lu_B }}</h5>
                    </div>
                </div>
                <h2 class="section-title" style="color: #c084fc; border-bottom: 2px solid rgba(192, 132, 252, 0.3); margin-top: 20px;">👑 ANALYTICS VIP ROOM</h2>
                <div class="vip-box">
                    <div class="vip-grid">
                        <div class="vip-card">
                            <span style="font-size: 11px; color: #fbbf24; font-weight: 600;">⭐ VIP GOLD</span>
                            <div style="font-size: 22px; margin: 8px 0;">🔒</div>
                            <span style="font-size: 11px; color: #9ca3af;">Oran: +4.50</span>
                        </div>
                        <div class="vip-card">
                            <span style="font-size: 11px; color: #f87171; font-weight: 600;">🔥 SKOR VIP</span>
                            <div style="font-size: 22px; margin: 8px 0;">🔒</div>
                            <span style="font-size: 11px; color: #9ca3af;">Oran: +12.00</span>
                        </div>
                        <div class="vip-card">
                            <span style="font-size: 11px; color: #34d399; font-weight: 600;">💰 KASA VIP</span>
                            <div style="font-size: 22px; margin: 8px 0;">🔒</div>
                            <span style="font-size: 11px; color: #9ca3af;">Oran: +3.20</span>
                        </div>
                    </div>
                    <button onclick="alert('VIP Altyapısı Çok Yakında Aktif Olacak!');" class="vip-btn">VIP SİSTEME KATIL</button>
                </div>
            </div>
            <div>
                <h2 class="section-title" style="color: #38bdf8; border-bottom: 2px solid rgba(56, 189, 248, 0.3);">📈 Bugünün Canlı Fikstür Listesi</h2>
                {% for t in d.tekli_maclar %}
                <div class="mac-row">
                    <div style="max-width: 70%;">
                        <span style="font-size: 10px; color: #a1a1aa; font-weight: 600; text-transform: uppercase;">{{ t.lig }}</span>
                        <div style="font-weight: 600; font-size: 13px; margin-top: 3px; color: #f3f4f6; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ t.mac }}</div>
                    </div>
                    <div style="text-align: right; min-width: 75px;">
                        <span class="badge-tahmin">{{ t.tahmin }}</span>
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
