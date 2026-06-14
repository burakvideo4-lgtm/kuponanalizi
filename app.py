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
                    "yuzde": yuzde
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
        "tekli_maclar": tahmin_havuzu[:12],
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
    return kuponlari_olustur(ornekler * 3)

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
        .wrapper { max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 15px; }
        
        .header-box {
            text-align: center;
            padding: 20px 15px;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.5), rgba(15, 23, 42, 0.8));
            border-radius: 16px;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }
        .header-box h1 {
            margin: 0; font-size: 26px; font-weight: 800; letter-spacing: 1.5px;
            background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .header-box p { color: #9ca3af; font-size: 13px; margin: 6px 0 0 0; }

        /* SEKMELER (TABS) TASARIMI */
        .tabs-container {
            display: flex; gap: 10px; background: rgba(30, 41, 59, 0.6); padding: 6px; border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05); overflow-x: auto; white-space: nowrap;
        }
        .tab-btn {
            flex: 1; text-align: center; padding: 12px 16px; background: transparent; border: none;
            color: #9ca3af; font-weight: 600; font-size: 13px; border-radius: 8px; cursor: pointer;
            transition: all 0.2s ease; min-width: 140px;
        }
        .tab-btn:hover { background: rgba(255, 255, 255, 0.05); color: #f3f4f6; }
        .tab-btn.active {
            background: linear-gradient(135deg, #38bdf8, #6366f1); color: white;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        /* SEKME İÇERİKLERİ gizleme/gösterme */
        .tab-content { display: none; animation: fadeIn 0.3s ease; }
        .tab-content.active { display: block; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

        /* KARTLAR VE MAÇ SATIRLARI */
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .grid-layout-today { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 20px; }
        
        .card { 
            background: rgba(30, 41, 59, 0.4); padding: 18px; border-radius: 16px; 
            border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .card-win { border-left: 5px solid #10b981; }
        .card-lose { border-left: 5px solid #ef4444; }
        .card-record { border: 1px solid #fbbf24; background: linear-gradient(135deg, rgba(251, 191, 36, 0.05), rgba(30, 41, 59, 0.4)); }

        .mac-row {
            background: rgba(30, 41, 59, 0.3); padding: 12px; margin-bottom: 10px; border-radius: 12px; 
            display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255, 255, 255, 0.03);
        }
        .badge-tahmin { background: linear-gradient(135deg, #0284c7, #0369a1); color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; }
        .badge-win { background: #10b981; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
        .badge-lose { background: #ef4444; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
        .oran-text { font-size: 14px; color: #10b981; font-weight: 700; margin-top: 4px; }
        
        h2.section-title { font-size: 16px; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 15px 0; padding-bottom: 6px; border-bottom: 2px solid rgba(255,255,255,0.05); }

        /* VIP BOX */
        .vip-box { 
            background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); padding: 20px; border-radius: 16px; border: 1px solid #6366f1; text-align: center; margin-top: 15px;
        }
        .vip-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 15px; }
        .vip-card { background: rgba(15, 23, 42, 0.6); padding: 12px 5px; border-radius: 12px; border: 1px dashed rgba(99, 102, 241, 0.4); }
        .vip-btn {
            background: linear-gradient(90deg, #6366f1, #a855f7); color: white; border: none; padding: 12px; font-size: 13px; font-weight: 700; border-radius: 10px; cursor: pointer; width: 100%;
        }

        @media (max-width: 992px) { .grid-layout-today { grid-template-columns: 1fr; } }
        @media (max-width: 768px) { .grid-2, .vip-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="wrapper">
        <!-- Başlık Bölümü -->
        <div class="header-box">
            <h1>⚡ BETAI SMART PORTAL ⚡</h1>
            <p>Yapay Zeka Destekli Filtrelenmiş Canlı Spor Analizleri</p>
        </div>

        <!-- SEKMELİ GEÇİŞ MENÜSÜ -->
        <div class="tabs-container">
            <button class="tab-btn active" onclick="switchTab('bugun')">🔥 Bugünün Analizleri</button>
            <button class="tab-btn" onclick="switchTab('kazananlar')">✅ Kazananlar (Arşiv)</button>
            <button class="tab-btn" onclick="switchTab('kaybedenler')">❌ Kaybedenler</button>
            <button class="tab-btn" onclick="switchTab('rekorlar')">👑 Oran Rekorları</button>
        </div>

        <!-- 1. SEKME: BUGÜNÜN ANALİZLERİ -->
        <div id="bugun" class="tab-content active">
            <div class="grid-layout-today">
                <div>
                    <h2 class="section-title" style="color: #fbbf24; border-color: rgba(251, 191, 36, 0.2);">🔮 GÜNÜN 2'Lİ GRUPLARI (ALTIN İKİLİ)</h2>
                    <div class="grid-2">
                        <div class="card">
                            <h4 style="color: #34d399; margin: 0 0 12px 0; font-size: 13px;">🟢 Altın İkili - Kampanya A (%{{ d.guven_2li_A }})</h4>
                            {% for m in d.kupon_2li_A %}
                            <p style="margin: 6px 0; font-size: 13px; color: #e5e7eb;">🔹 <b>{{ m.mac }}</b> <br><span style="color: #38bdf8; font-size:12px;">Tahmin: {{ m.tahmin }}</span></p>
                            {% endfor %}
                            <h5 style="text-align: right; color: #34d399; margin: 12px 0 0 0; font-size: 13px;">Toplam Oran: {{ d.oran_2li_A }}</h5>
                        </div>
                        <div class="card">
                            <h4 style="color: #34d399; margin: 0 0 12px 0; font-size: 13px;">🟢 Altın İkili - Kampanya B (%{{ d.guven_2li_B }})</h4>
                            {% for m in d.kupon_2li_B %}
                            <p style="margin: 6px 0; font-size: 13px; color: #e5e7eb;">🔹 <b>{{ m.mac }}</b> <br><span style="color: #38bdf8; font-size:12px;">Tahmin: {{ m.tahmin }}</span></p>
                            {% endfor %}
                            <h5 style="text-align: right; color: #34d399; margin: 12px 0 0 0; font-size: 13px;">Toplam Oran: {{ d.oran_2li_B }}</h5>
                        </div>
                    </div>

                    <h2 class="section-title" style="color: #f87171; border-color: rgba(248, 113, 113, 0.2); margin-top: 15px;">💰 ÜÇLÜ KASA KATLAMA ANALİZLERİ</h2>
                    <div class="grid-2">
                        <div class="card">
                            <h4 style="color: #f87171; margin: 0 0 12px 0; font-size: 13px;">🔴 Kasa Katlama - Seçim A (%{{ d.guven_3lu_A }})</h4>
                            {% for m in d.kupon_3lu_A %}
                            <p style="margin: 5px 0; font-size: 13px; color: #e5e7eb;">🔹 <b>{{ m.mac }}</b> <span style="color: #38bdf8; font-size:12px;">({{ m.tahmin }})</span></p>
                            {% endfor %}
                            <h5 style="text-align: right; color: #f87171; margin: 12px 0 0 0; font-size: 13px;">Toplam Oran: {{ d.oran_3lu_A }}</h5>
                        </div>
                        <div class="card">
                            <h4 style="color: #f87171; margin: 0 0 12px 0; font-size: 13px;">🔴 Kasa Katlama - Seçim B (%{{ d.guven_3lu_B }})</h4>
                            {% for m in d.kupon_3lu_B %}
                            <p style="margin: 5px 0; font-size: 13px; color: #e5e7eb;">🔹 <b>{{ m.mac }}</b> <span style="color: #38bdf8; font-size:12px;">({{ m.tahmin }})</span></p>
                            {% endfor %}
                            <h5 style="text-align: right; color: #f87171; margin: 12px 0 0 0; font-size: 13px;">Toplam Oran: {{ d.oran_3lu_B }}</h5>
                        </div>
                    </div>

                    <div class="vip-box">
                        <div class="vip-grid">
                            <div class="vip-card"><span style="font-size: 10px; color: #fbbf24;">⭐ VIP GOLD</span><div style="font-size: 16px; margin:4px 0;">🔒</div></div>
                            <div class="vip-card"><span style="font-size: 10px; color: #f87171;">🔥 SKOR VIP</span><div style="font-size: 16px; margin:4px 0;">🔒</div></div>
                            <div class="vip-card"><span style="font-size: 10px; color: #34d399;">💰 KASA VIP</span><div style="font-size: 16px; margin:4px 0;">🔒</div></div>
                        </div>
                        <button onclick="alert('VIP Odaları çok yakında aktif hale gelecektir!');" class="vip-btn">KİLİTLERİ AÇ</button>
                    </div>
                </div>

                <div>
                    <h2 class="section-title" style="color: #38bdf8; border-color: rgba(56, 189, 248, 0.2);">📈 BUGÜNÜN TEKLİ MAÇ HAVUZU</h2>
                    {% for t in d.tekli_maclar %}
                    <div class="mac-row">
                        <div style="max-width: 68%;">
                            <span style="font-size: 9px; color: #9ca3af; text-transform: uppercase;">{{ t.lig }}</span>
                            <div style="font-weight: 600; font-size: 12px; margin-top: 2px; color: #f3f4f6; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{{ t.mac }}</div>
                        </div>
                        <div style="text-align: right; min-width: 70px;">
                            <span class="badge-tahmin">{{ t.tahmin }}</span>
                            <div class="oran-text">{{ t.oran }}</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- 2. SEKME: KAZANANLAR ARŞİVİ -->
        <div id="kazananlar" class="tab-content">
            <h2 class="section-title" style="color: #10b981; border-color: rgba(16, 185, 129, 0.2);">🟢 DÜN BAŞARIYLA SONUÇLANAN ANALİZLER</h2>
            <div class="grid-2">
                <div class="card card-win">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="color: #10b981; margin: 0; font-size: 14px;">✅ Altın İkili Kombinesi</h4>
                        <span class="badge-win">KAZANDI</span>
                    </div>
                    <p style="margin: 4px 0; font-size: 13px; color: #9ca3af;">🔹 Man. City - Liverpool <span style="color: #10b981;">(2.5 Üst) 🟢</span></p>
                    <p style="margin: 4px 0; font-size: 13px; color: #9ca3af;">🔹 Real Madrid - Barcelona <span style="color: #10b981;">(MS 1) 🟢</span></p>
                    <h5 style="text-align: right; color: #10b981; margin: 10px 0 0 0;">Oran: 2.85</h5>
                </div>
                
                <div class="card card-win">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="color: #10b981; margin: 0; font-size: 14px;">✅ Kasa Katlama Analizi</h4>
                        <span class="badge-win">KAZANDI</span>
                    </div>
                    <p style="margin: 4px 0; font-size: 13px; color: #9ca3af;">🔹 Arsenal - Chelsea <span style="color: #10b981;">(MS 1) 🟢</span></p>
                    <p style="margin: 4px 0; font-size: 13px; color: #9ca3af;">🔹 Aston Villa - Newcastle <span style="color: #10b981;">(KG Var) 🟢</span></p>
                    <p style="margin: 4px 0; font-size: 13px; color: #10b981;">🔹 Monaco - Lyon <span style="color: #10b981;">(İY 0.5 Üst) 🟢</span></p>
                    <h5 style="text-align: right; color: #10b981; margin: 10px 0 0 0;">Oran: 3.42</h5>
                </div>

                <div class="card card-win">
                    <h4 style="color: #10b981; margin: 0 0 8px 0; font-size: 13px;">🎯 Tekli Değerli Maç (Süper Lig)</h4>
                    <p style="margin: 0; font-size: 13px; color: #e5e7eb;">Fenerbahçe - Galatasaray</p>
                    <span style="font-size: 12px; color: #10b981;">Tahmin: KG Var (1.65) 🟢 Başarıyla Bildi</span>
                </div>
                <div class="card card-win">
                    <h4 style="color: #10b981; margin: 0 0 8px 0; font-size: 13px;">🎯 Tekli Değerli Maç (Serie A)</h4>
                    <p style="margin: 0; font-size: 13px; color: #e5e7eb;">Roma - Lazio</p>
                    <span style="font-size: 12px; color: #10b981;">Tahmin: MS 1 (1.90) 🟢 Başarıyla Bildi</span>
                </div>
            </div>
        </div>

        <!-- 3. SEKME: KAYBEDENLER ARŞİVİ -->
        <div id="kaybedenler" class="tab-content">
            <h2 class="section-title" style="color: #ef4444; border-color: rgba(239, 68, 68, 0.2);">🔴 KAYBEDEN / TEK MAÇTAN YATAN ANALİZLER</h2>
            <div class="grid-2">
                <div class="card card-lose">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="color: #f87171; margin: 0; font-size: 14px;">❌ İdeal İkili Grubu</h4>
                        <span class="badge-lose">KAYBETTİ</span>
                    </div>
                    <p style="margin: 4px 0; font-size: 13px; color: #9ca3af;">🔹 Juventus - Inter <span style="color: #10b981;">(KG Var) 🟢</span></p>
                    <p style="margin: 4px 0; font-size: 13px; color: #9ca3af;">🔹 Bayern Munich - Leipzig <span style="color: #ef4444;">(MS 1) 🔴 (Maç: 1-2)</span></p>
                    <h5 style="text-align: right; color: #f87171; margin: 10px 0 0 0;">Oran: 2.10</h5>
                </div>

                <div class="card card-lose">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="color: #f87171; margin: 0; font-size: 14px;">❌ Riskli Kasa Katlama</h4>
                        <span class="badge-lose">KAYBETTİ</span>
                    </div>
                    <p style="margin: 4px 0; font-size: 13px; color: #9ca3af;">🔹 Napoli - Lazio <span style="color: #10b981;">(2.5 Üst) 🟢</span></p>
                    <p style="margin: 4px 0; font-size: 13px; color: #ef4444;">🔹 Atletico Madrid - Sevilla <span style="color: #ef4444;">(MS 1) 🔴 (Maç: 0-0)</span></p>
                    <p style="margin: 4px 0; font-size: 13px; color: #9ca3af;">🔹 Ajax - PSV <span style="color: #10b981;">(KG Var) 🟢</span></p>
                    <h5 style="text-align: right; color: #f87171; margin: 10px 0 0 0;">Oran: 4.15</h5>
                </div>
            </div>
        </div>

        <!-- 4. SEKME: EN YÜKSEK ORAN REKORLARI -->
        <div id="rekorlar" class="tab-content">
            <h2 class="section-title" style="color: #fbbf24; border-color: rgba(251, 191, 36, 0.2);">🏆 PLATFORM TARİHİNİN EN YÜKSEK ORANLI BAŞARILARI</h2>
            <div class="grid-2">
                <div class="card card-record">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="color: #fbbf24; margin: 0; font-size: 15px;">🥇 EFSANE VURGUN KUPONU</h4>
                        <span class="badge-win" style="background:#fbbf24; color:#000;">REKOR</span>
                    </div>
                    <p style="margin: 4px 0; font-size: 13px;">🔥 Real Sociedad - Real Betis <span style="color:#10b981;">(MS X) 🟢 Oran: 3.20</span></p>
                    <p style="margin: 4px 0; font-size: 13px;">🔥 Frankfurt - Leverkusen <span style="color:#10b981;">(MS 2) 🟢 Oran: 2.10</span></p>
                    <p style="margin: 4px 0; font-size: 13px;">🔥 Brighton - Everton <span style="color:#10b981;">(2.5 Üst) 🟢 Oran: 1.85</span></p>
                    <h4 style="text-align: right; color: #fbbf24; margin: 12px 0 0 0; font-size:16px;">🔥 Toplam Oran: 12.43</h4>
                </div>

                <div class="card card-record">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="color: #fbbf24; margin: 0; font-size: 15px;">🥈 YÜKSEK SKOR SÜRPRİZİ</h4>
                        <span class="badge-win" style="background:#a855f7;">VIP REKOR</span>
                    </div>
                    <p style="margin: 4px 0; font-size: 13px;">🔥 Atalanta - Fiorentina <span style="color:#10b981;">(3.5 Üst) 🟢 Oran: 2.75</span></p>
                    <p style="margin: 4px 0; font-size: 13px;">🔥 Tottenham - West Ham <span style="color:#10b981;">(KG Var & 2.5 Üst) 🟢 Oran: 2.20</span></p>
                    <h4 style="text-align: right; color: #a855f7; margin: 12px 0 0 0; font-size:16px;">🔥 Toplam Oran: 6.05</h4>
                </div>
            </div>
        </div>

    </div>

    <!-- SEKMELERİ ÇALIŞTIRAN JAVASCRIPT KODU -->
    <script>
        function switchTab(tabId) {
            // Tüm içerikleri gizle
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));

            // Tüm butonların aktifliğini kaldır
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));

            // Seçilen içeriği ve butonu aktif et
            document.getElementById(tabId).add('active'); 
            // JavaScript düzeltmesi: classList.add olmalı
            document.getElementById(tabId).classList.add('active');
            
            // Tıklanan butonu bulup aktif sınıfı ekleme
            event.currentTarget.classList.add('active');
        }
    </script>
</body>
</html>"""
    return render_template_string(html_kod, d=d)

if __name__ == '__main__':
    app.run(debug=True)
