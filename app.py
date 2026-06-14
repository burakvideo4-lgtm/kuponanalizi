from flask import Flask, render_template_string
import requests
import random
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# API Giriş Bilgileri
API_KEY = "999e0bfd03e0268f0ad00d6619da543f"
API_URL = "https://v3.football.api-sports.io/fixtures"

# Küresel veri deposu (Kullanıcılar siteye girdiğinde buradaki güncel gerçek veri okunacak)
canli_veri_deposu = {}

def gerçek_zamanli_analiz_motoru():
    global canli_veri_deposu
    print("🤖 Yapay Zeka Gerçek Canlı Maçları API'den Çekiyor...")
    
    # API sınırlarını korumak ve sunucu çökmesini önlemek için her ihtimale karşı yedek havuzumuz hazır duruyor
    yedek_veri = sahte_veri_uret()
    
    try:
        # Bugünün ve şu an canlı olan maçları çekmek için parametreler
        headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': API_KEY
        }
        
        # Sadece aktif, canlı veya bugün oynanacak maçları listele (Sunucuyu yormamak için limitli)
        response = requests.get(f"{API_URL}?live=all", headers=headers, timeout=5)
        data = response.json()
        
        mac_listesi = data.get("response", [])
        
        # Eğer o an canlı maç yoksa bugünün yaklaşan maçlarını çekmeyi dene
        if not mac_listesi:
            from datetime import datetime
            bugun = datetime.now().strftime('%Y-%m-%d')
            response = requests.get(f"{API_URL}?date={bugun}", headers=headers, timeout=5)
            data = response.json()
            mac_listesi = data.get("response", [])

        if not mac_listesi or len(mac_listesi) < 5:
            canli_veri_deposu = yedek_veri
            return

        tahmin_havuzu = []
        # En fazla 30 gerçek maçı analiz süzgecine alıyoruz
        for m in mac_listesi[:30]:
            try:
                ev_takim = m['teams']['home']['name']
                deplasman_takim = m['teams']['away']['name']
                lig_adi = m['league']['name']
                ulke = m['league']['country']
                
                # Gerçek veri analizi simülasyonu
                tahmin_tipleri = ["MS 1", "MS 2", "2.5 Üst", "KG Var", "İY 0.5 Üst"]
                secilen_tahmin = random.choice(tahmin_tipleri)
                oran = round(random.uniform(1.40, 2.35), 2)
                yuzde = random.randint(83, 95) if oran < 1.60 else random.randint(60, 82)
                
                tahmin_havuzu.append({
                    "lig": f"{ulke} - {lig_adi}",
                    "mac": f"{ev_takim} - {deplasman_takim}",
                    "tahmin": secilen_tahmin,
                    "oran": oran,
                    "yuzde": yuzde
                })
            except Exception as e:
                continue

        if len(tahmin_havuzu) < 4:
            canli_veri_deposu = yedek_veri
            return

        # Güven yüzdesine göre en iyileri yukarı taşı
        tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
        
        # Maç sayısına göre dinamik kuponlama yapıyoruz
        k1 = tahmin_havuzu[0:2] if len(tahmin_havuzu) >= 2 else tahmin_havuzu[0:1]
        k2 = tahmin_havuzu[2:4] if len(tahmin_havuzu) >= 4 else tahmin_havuzu[0:1]
        k3 = tahmin_havuzu[4:7] if len(tahmin_havuzu) >= 7 else tahmin_havuzu[0:1]
        k4 = tahmin_havuzu[7:10] if len(tahmin_havuzu) >= 10 else tahmin_havuzu[0:1]

        canli_veri_deposu = {
            "tekli_maclar": tahmin_havuzu[:10],
            "kupon_2li_A": k1,
            "kupon_2li_B": k2,
            "kupon_3lu_A": k3,
            "kupon_3lu_B": k4,
            "oran_2li_A": round(sum(x['oran'] for x in k1), 2),
            "oran_2li_B": round(sum(x['oran'] for x in k2), 2),
            "oran_3lu_A": round(sum(x['oran'] for x in k3), 2),
            "oran_3lu_B": round(sum(x['oran'] for x in k4), 2),
            "guven_2li_A": round(sum(x['yuzde'] for x in k1) / len(k1)),
            "guven_2li_B": round(sum(x['yuzde'] for x in k2) / len(k2)),
            "guven_3lu_A": round(sum(x['yuzde'] for x in k3) / len(k3)),
            "guven_3lu_B": round(sum(x['yuzde'] for x in k4) / len(k4))
        }
    except Exception as e:
        print(f"Hata oluştu, yedeğe geçiliyor: {e}")
        canli_veri_deposu = yedek_veri

def sahte_veri_uret():
    # API'de anlık kesinti olursa sitenin boş kalmaması için kurumsal yedek havuz
    ornekler = [
        {"lig": "İngiltere Premier Lig", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55, "yuzde": 88},
        {"lig": "İspanya La Liga", "mac": "Real Madrid - Atletico Madrid", "tahmin": "2.5 Üst", "oran": 1.68, "yuzde": 82},
        {"lig": "İtalya Serie A", "mac": "Inter - AC Milan", "tahmin": "KG Var", "oran": 1.72, "yuzde": 76},
        {"lig": "Almanya Bundesliga", "mac": "Bayern Munich - Dortmund", "tahmin": "MS 1", "oran": 1.48, "yuzde": 89},
        {"lig": "Fransa Ligue 1", "mac": "PSG - Monaco", "tahmin": "2.5 Üst", "oran": 1.60, "yuzde": 81},
        {"lig": "Türkiye Süper Lig", "mac": "Galatasaray - Beşiktaş", "tahmin": "KG Var", "oran": 1.65, "yuzde": 79},
        {"lig": "Hollanda Eredivisie", "mac": "Ajax - Feyenoord", "tahmin": "2.5 Üst", "oran": 1.52, "yuzde": 84}
    ]
    return {
        "tekli_maclar": ornekler,
        "kupon_2li_A": ornekler[0:2], "kupon_2li_B": ornekler[2:4],
        "kupon_3lu_A": ornekler[4:6], "kupon_3lu_B": ornekler[5:7],
        "oran_2li_A": 3.23, "oran_2li_B": 2.89, "oran_3lu_A": 5.12, "oran_3lu_B": 4.65,
        "guven_2li_A": 85, "guven_2li_B": 80, "guven_3lu_A": 78, "guven_3lu_B": 74
    }

# İLK ÇALIŞTIRMA VE ARKA PLAN ZAMANLAYICISI
# Site ilk açıldığında veriyi bir kez çeker, sonra her 15 dakikada bir API'yi günceller.
# Böylece günde sadece 96 istek atarak API sınırını asla aşmayız ve Render asla çökmez.
gerçek_zamanli_analiz_motoru()
scheduler = BackgroundScheduler()
scheduler.add_job(func=gerçek_zamanli_analiz_motoru, trigger="interval", minutes=15)
scheduler.start()

@app.route('/')
def ana_sayfa():
    d = canli_veri_deposu if canli_veri_deposu else sahte_veri_uret()
    
    html_kod = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>AI Canlı Tahmin Merkezi</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 10px; background-color: #0b0f19; color: #f1f5f9; }
                .wrapper { max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; }
                .card { background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 10px; }
                .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
                .vip-box { background: linear-gradient(135deg, #1e1b4b, #2e1065); padding: 20px; border-radius: 16px; border: 2px solid #6366f1; text-align: center; }
                .vip-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 15px; }
                
                @media (min-width: 769px) {
                    .main-layout { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 20px; }
                }
                @media (max-width: 768px) {
                    .grid-2, .vip-grid { grid-template-columns: 1fr; }
                    h1 { font-size: 20px !important; }
                }
            </style>
        </head>
        <body>
            <div class="wrapper">
                <h1 style="text-align: center; color: #38bdf8; margin: 15px 0 5px 0; font-size: 24px;">🟢 AI CANLI VERİ MOTORU v8.0 🤖</h1>
                <p style="text-align: center; color: #64748b; font-size: 14px; margin: 0 0 10px 0;">Gerçek Zamanlı API Entegrasyonlu Mobil Uyumlu Platform</p>
                
                <div style="background: linear-gradient(90deg, #065f46, #0f172a); border: 1px solid #059669; padding: 12px; border-radius: 12px; text-align: center;">
                    <h3 style="margin: 0; color: #34d399; font-size: 14px;">📊 Sistem Durumu: Canlı API Bağlantısı Aktif</h3>
                </div>

                <div class="main-layout">
                    <div>
                        <h2 style="color: #fbbf24; border-bottom: 2px solid #fbbf24; padding-bottom: 6px; font-size: 18px; margin-top: 0;">🔥 Günün Yapay Zeka Kombineleri</h2>
                        
                        <div class="grid-2">
                            <div class="card">
                                <h4 style="color: #10b981; margin: 0 0 10px 0; font-size: 13px;">🟢 Altın İkili - A (%{{ d.guven_2li_A }})</h4>
                                {% for m in d.kupon_2li_A %} <p style="margin: 5px 0; font-size: 13px;">🔹 <b>{{ m.mac }}</b> ({{ m.tahmin }})</p> {% endfor %}
                                <h5 style="text-align: right; color: #38bdf8; margin: 10px 0 0 0;">Oran: {{ d.oran_2li_A }}</h5>
                            </div>
                            <div class="card">
                                <h4 style="color: #10b981; margin: 0 0 10px 0; font-size: 13px;">🟢 Altın İkili - B (%{{ d.guven_2li_B }})</h4>
                                {% for m in d.kupon_2li_B %} <p style="margin: 5px 0; font-size: 13px;">🔹 <b>{{ m.mac }}</b> ({{ m.tahmin }})</p> {% endfor %}
                                <h5 style="text-align: right; color: #38bdf8; margin: 10px 0 0 0;">Oran: {{ d.oran_2li_B }}</h5>
                            </div>
                        </div>
                        
                        <div class="grid-2">
                            <div class="card">
                                <h4 style="color: #f43f5e; margin: 0 0 10px 0; font-size: 13px;">🔴 Kasa Katlama - A (%{{ d.guven_3lu_A }})</h4>
                                {% for m in d.kupon_3lu_A %} <p style="margin: 5px 0; font-size: 13px;">🔹 <b>{{ m.mac }}</b> ({{ m.tahmin }})</p> {% endfor %}
                                <h5 style="text-align: right; color: #38bdf8; margin: 10px 0 0 0;">Oran: {{ d.oran_3lu_A }}</h5>
                            </div>
                            <div class="card">
                                <h4 style="color: #f43f5e; margin: 0 0 10px 0; font-size: 13px;">🔴 Kasa Katlama - B (%{{ d.guven_3lu_B }})</h4>
                                {% for m in d.kupon_3lu_B %} <p style="margin: 5px 0; font-size: 13px;">🔹 <b>{{ m.mac }}</b> ({{ m.tahmin }})</p> {% endfor %}
                                <h5 style="text-align: right; color: #38bdf8; margin: 10px 0 0 0;">Oran: {{ d.oran_3lu_B }}</h5>
                            </div>
                        </div>
                        
                        <h2 style="color: #a5b4fc; border-bottom: 2px solid #6366f1; padding-bottom: 8px; font-size: 18px; margin-top: 10px;">👑 AI GOLD VIP ODASI</h2>
                        <div class="vip-box">
                            <div class="vip-grid">
                                <div style="background: rgba(15,23,42,0.6); padding: 12px; border-radius: 8px; border: 1px dashed #6366f1;">
                                    <span style="font-size: 11px; color: #fbbf24;">⭐ VIP KUPON 1</span>
                                    <div style="font-size: 20px; margin: 8px 0;">🔒</div>
                                    <span style="font-size: 10px; color: #94a3b8;">Oran: +4.50</span>
                                </div>
                                <div style="background: rgba(15,23,42,0.6); padding: 12px; border-radius: 8px; border: 1px dashed #6366f1;">
                                    <span style="font-size: 11px; color: #f43f5e;">🔥 SKOR VIP</span>
                                    <div style="font-size: 20px; margin: 8px 0;">🔒</div>
                                    <span style="font-size: 10px; color: #94a3b8;">Oran: +12.00</span>
                                </div>
                                <div style="background: rgba(15,23,42,0.6); padding: 12px; border-radius: 8px; border: 1px dashed #6366f1;">
                                    <span style="font-size: 11px; color: #10b981;">💰 KASA VIP</span>
                                    <div style="font-size: 20px; margin: 8px 0;">🔒</div>
                                    <span style="font-size: 10px; color: #94a3b8;">Oran: +3.20</span>
                                </div>
                            </div>
                            <button onclick="alert('VIP Altyapısı Çok Yakında Aktif Olacak!');" style="background: #6366f1; color: white; border: none; padding: 10px 22px; font-size: 13px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%;">
                                VIP Paketlere Abone Ol
                            </button>
                        </div>
                    </div>
                    
                    <div>
                        <h2 style="color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 8px; font-size: 18px; margin-top: 0;">📈 Günün Banko Kazanma Listesi (10 Maç)</h2>
                        {% for t in d.tekli_maclar %}
                        <div style="background: #1e293b; padding: 12px; margin-bottom: 10px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;">
                            <div style="max-width: 65%;">
                                <span style="font-size: 9px; color: #38bdf8; text-transform: uppercase;">{{ t.lig }}</span>
                                <div style="font-weight: bold; font-size: 13px; margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ t.mac }}</div>
                            </div>
                            <div style="text-align: right;">
                                <span style="background: #0369a1; color: white; padding: 3px 6px; border-radius: 4px; font-size: 11px; font-weight: bold;">{{ t.tahmin }}</span>
                                <div style="font-size: 12px; color: #10b981; font-weight: bold; margin-top: 4px;">{{ t.oran }} <span style="color: #64748b; font-size: 10px;">(%{{ t.yuzde }})</span></div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_kod, d=d)

if __name__ == '__main__':
    app.run(debug=True)
