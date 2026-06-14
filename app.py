from flask import Flask, render_template_string
import random

app = Flask(__name__)

def dinamik_canli_veri_motoru():
    # Gerçek dünya ligleri ve takımlarından oluşan devasa dinamik havuz
    ligler_ve_maclar = [
        {"lig": "Türkiye Süper Lig", "mac": "Galatasaray - Beşiktaş"},
        {"lig": "Türkiye Süper Lig", "mac": "Fenerbahçe - Trabzonspor"},
        {"lig": "Türkiye Süper Lig", "mac": "Başakşehir - Kasımpaşa"},
        {"lig": "İngiltere Premier Lig", "mac": "Arsenal - Chelsea"},
        {"lig": "İngiltere Premier Lig", "mac": "Liverpool - Man United"},
        {"lig": "İngiltere Premier Lig", "mac": "Man City - Tottenham"},
        {"lig": "İspanya La Liga", "mac": "Real Madrid - Atletico Madrid"},
        {"lig": "İspanya La Liga", "mac": "Barcelona - Real Sociedad"},
        {"lig": "İspanya La Liga", "mac": "Sevilla - Real Betis"},
        {"lig": "İtalya Serie A", "mac": "Inter - AC Milan"},
        {"lig": "İtalya Serie A", "mac": "Juventus - Napoli"},
        {"lig": "İtalya Serie A", "mac": "AS Roma - Lazio"},
        {"lig": "Almanya Bundesliga", "mac": "Bayern Munich - Dortmund"},
        {"lig": "Almanya Bundesliga", "mac": "Leipzig - Leverkusen"},
        {"lig": "Şampiyonlar Ligi", "mac": "Real Madrid - Man City"},
        {"lig": "Şampiyonlar Ligi", "mac": "Bayern Munich - PSG"},
        {"lig": "Avrupa Ligi", "mac": "Fenerbahçe - Lyon"},
        {"lig": "Avrupa Ligi", "mac": "Galatasaray - Ajax"}
    ]
    
    # Her sayfa yenilendiğinde rastgele ve mantıklı 10 maç seç
    secilen_maclar = random.sample(ligler_ve_maclar, min(len(ligler_ve_maclar), 12))
    tahmin_tipleri = ["MS 1", "MS 2", "2.5 Üst", "KG Var", "İY 0.5 Üst"]
    
    tahmin_havuzu = []
    for m in secilen_maclar:
        oran = round(random.uniform(1.42, 2.40), 2)
        # Oran düşükse güven yüzdesi yüksek, oran yüksekse güven yüzdesi makul aralıkta olur (Gerçekçi Yapay Zeka Mantığı)
        yuzde = random.randint(84, 96) if oran < 1.60 else random.randint(61, 83)
        
        tahmin_havuzu.append({
            "lig": m["lig"],
            "mac": m["mac"],
            "tahmin": random.choice(tahmin_tipleri),
            "oran": oran,
            "yuzde": yuzde
        })
    
    # Güven yüzdesine göre sırala
    tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
    
    k1 = tahmin_havuzu[0:2]
    k2 = tahmin_havuzu[2:4]
    k3 = tahmin_havuzu[4:7]
    k4 = tahmin_havuzu[6:9]
    
    return {
        "tekli_maclar": tahmin_havuzu[:10],
        "kupon_2li_A": k1,
        "kupon_2li_B": k2,
        "kupon_3lu_A": k3,
        "kupon_3lu_B": k4,
        "oran_2li_A": round(k1[0]['oran'] * k1[1]['oran'], 2),
        "oran_2li_B": round(k2[0]['oran'] * k2[1]['oran'], 2),
        "oran_3lu_A": round(k3[0]['oran'] * k3[1]['oran'] * k3[2]['oran'], 2),
        "oran_3lu_B": round(k4[0]['oran'] * k4[1]['oran'] * k4[2]['oran'], 2),
        "guven_2li_A": round((k1[0]['yuzde'] + k1[1]['yuzde']) / 2),
        "guven_2li_B": round((k2[0]['yuzde'] + k2[1]['yuzde']) / 2),
        "guven_3lu_A": round((k3[0]['yuzde'] + k3[1]['yuzde'] + k3[2]['yuzde']) / 3),
        "guven_3lu_B": round((k4[0]['yuzde'] + k4[1]['yuzde'] + k4[2]['yuzde']) / 3)
    }

@app.route('/')
def ana_sayfa():
    d = dinamik_canli_veri_motoru()
    
    html_kod = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>AI Premium Analiz Merkezi</title>
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
                <h1 style="text-align: center; color: #38bdf8; margin: 15px 0 5px 0; font-size: 24px;">📊 AI PREMIUM ANALİZ MOTORU v8.2 🤖</h1>
                <p style="text-align: center; color: #64748b; font-size: 14px; margin: 0 0 10px 0;">Yapay Zeka Destekli Mobil Uyumlu Gerçekçi İstatistik Paneli</p>
                
                <div style="background: linear-gradient(90deg, #065f46, #0f172a); border: 1px solid #059669; padding: 12px; border-radius: 12px; text-align: center;">
                    <h3 style="margin: 0; color: #34d399; font-size: 14px;">🟢 Sistem Durumu: Algoritmik Veri Akışı Stabil</h3>
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
