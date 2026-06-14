from flask import Flask, render_template_string
import random

app = Flask(__name__)

def sahte_veri_uret():
    # Devasa ve kaliteli bir maç havuzu (Her yenilemede farklı kombinasyon yapacak)
    havuz = [
        {"lig": "İngiltere Premier Lig", "mac": "Arsenal - Chelsea"},
        {"lig": "İspanya La Liga", "mac": "Real Madrid - Atletico Madrid"},
        {"lig": "İtalya Serie A", "mac": "Inter - AC Milan"},
        {"lig": "Almanya Bundesliga", "mac": "Bayern Munich - Dortmund"},
        {"lig": "Fransa Ligue 1", "mac": "PSG - Monaco"},
        {"lig": "Türkiye Süper Lig", "mac": "Galatasaray - Beşiktaş"},
        {"lig": "Hollanda Eredivisie", "mac": "Ajax - Feyenoord"},
        {"lig": "Portekiz Liga NOS", "mac": "Benfica - Porto"},
        {"lig": "Şampiyonlar Ligi", "mac": "Man City - Juventus"},
        {"lig": "Avrupa Ligi", "mac": "Fenerbahçe - Lyon"},
        {"lig": "İngiltere Premier Lig", "mac": "Liverpool - Man United"},
        {"lig": "İspanya La Liga", "mac": "Barcelona - Real Sociedad"},
        {"lig": "Türkiye Süper Lig", "mac": "Fenerbahçe - Trabzonspor"},
        {"lig": "Almanya Bundesliga", "mac": "Leipzig - Leverkusen"},
        {"lig": "İtalya Serie A", "mac": "Juventus - Napoli"}
    ]
    
    # Havuzdan rastgele 10 maç seçiyoruz
    secilen_maclar = random.sample(havuz, 10)
    tahmin_tipleri = ["MS 1", "MS 2", "2.5 Üst", "KG Var", "İY 0.5 Üst"]
    
    tahmin_havuzu = []
    for m in secilen_maclar:
        oran = round(random.uniform(1.35, 2.30), 2)
        yuzde = random.randint(82, 94) if oran < 1.50 else random.randint(58, 81)
        tahmin_havuzu.append({
            "lig": m["lig"],
            "mac": m["mac"],
            "tahmin": random.choice(tahmin_tipleri),
            "oran": oran,
            "yuzde": yuzde
        })
        
    tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
    
    kupon_2li_A = tahmin_havuzu[0:2]
    kupon_2li_B = tahmin_havuzu[2:4]
    kupon_3lu_A = tahmin_havuzu[4:7]
    kupon_3lu_B = tahmin_havuzu[7:10]
    
    return {
        "tekli_maclar": tahmin_havuzu[:10],
        "kupon_2li_A": kupon_2li_A,
        "kupon_2li_B": kupon_2li_B,
        "kupon_3lu_A": kupon_3lu_A,
        "kupon_3lu_B": kupon_3lu_B,
        "oran_2li_A": round(kupon_2li_A[0]['oran'] * kupon_2li_A[1]['oran'], 2),
        "oran_2li_B": round(kupon_2li_B[0]['oran'] * kupon_2li_B[1]['oran'], 2),
        "oran_3lu_A": round(kupon_3lu_A[0]['oran'] * kupon_3lu_A[1]['oran'] * kupon_3lu_A[2]['oran'], 2),
        "oran_3lu_B": round(kupon_3lu_B[0]['oran'] * kupon_3lu_B[1]['oran'] * kupon_3lu_B[2]['oran'], 2),
        "guven_2li_A": round((kupon_2li_A[0]['yuzde'] + kupon_2li_A[1]['yuzde']) / 2),
        "guven_2li_B": round((kupon_2li_B[0]['yuzde'] + kupon_2li_B[1]['yuzde']) / 2),
        "guven_3lu_A": round((kupon_3lu_A[0]['yuzde'] + kupon_3lu_A[1]['yuzde'] + kupon_3lu_A[2]['yuzde']) / 3),
        "guven_3lu_B": round((kupon_3lu_B[0]['yuzde'] + kupon_3lu_B[1]['yuzde'] + kupon_3lu_B[2]['yuzde']) / 3)
    }

@app.route('/')
def ana_sayfa():
    d = sahte_veri_uret()
    
    html_kod = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>AI Premium Tahmin Üssü</title>
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
                <h1 style="text-align: center; color: #38bdf8; margin: 15px 0 5px 0; font-size: 24px;">📊 AI MEGA TAHMİN MOTORU v7.2 🤖</h1>
                <p style="text-align: center; color: #64748b; font-size: 14px; margin: 0 0 10px 0;">Mobil Uyumlu Akıllı Bahis Platformu</p>
                
                <div style="background: linear-gradient(90deg, #065f46, #0f172a); border: 1px solid #059669; padding: 12px; border-radius: 12px; text-align: center;">
                    <h3 style="margin: 0; color: #34d399; font-size: 14px;">📊 Dünün Yapay Zeka Başarı Oranı: %91.6!</h3>
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
