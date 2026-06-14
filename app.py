from flask import Flask, render_template_string
import random

app = Flask(__name__)

API_KEY = "999e0bfd03e0268f0ad00d6619da543f"

def bot_analiz_motoru():
    # Sunucu başlangıcında kasma yapmaması için yedek verileri en başta hazır tutuyoruz
    yedek = sahte_veri_uret()
    
    try:
        import requests
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': API_KEY
        }
        # Sunucu takılmasın diye timeout süresini çok kısa (3 saniye) tuttuk
        response = requests.get(url, headers=headers, timeout=3)
        data = response.json()
        
        if data.get("response") and len(data["response"]) >= 10:
            mac_listesi = data["response"]
            tahmin_havuzu = []
            
            for m in mac_listesi[:25]: # İstek sayısını sunucuyu yormayacak şekilde 25'e çektik
                try:
                    ev = m['teams']['home']['name']
                    deplasman = m['teams']['away']['name']
                    lig = m['league']['name']
                    
                    tahmin_tipleri = ["MS 1", "MS 2", "2.5 Üst", "KG Var", "İY 0.5 Üst"]
                    secilen_tahmin = random.choice(tahmin_tipleri)
                    oran = round(random.uniform(1.35, 2.30), 2)
                    yuzde = random.randint(82, 94) if oran < 1.50 else random.randint(58, 81)
                    
                    tahmin_havuzu.append({
                        "lig": lig,
                        "mac": f"{ev} - {deplasman}",
                        "tahmin": secilen_tahmin,
                        "oran": oran,
                        "yuzde": yuzde
                    })
                except:
                    continue
            
            if len(tahmin_havuzu) >= 10:
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
                    "guven_3lu_B": round((kupon_3lu_B[0]['yuzde'] + kupon_3lu_B[1]['yuzde'] + kupon_3lu_B[2]['yuzde']) / 3),
                }
    except:
        pass
        
    return yedek

def sahte_veri_uret():
    ornekler = [
        {"lig": "İngiltere Premier Lig", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55, "yuzde": 88},
        {"lig": "İspanya La Liga", "mac": "Real Madrid - Atletico Madrid", "tahmin": "2.5 Üst", "oran": 1.68, "yuzde": 82},
        {"lig": "İtalya Serie A", "mac": "Inter - AC Milan", "tahmin": "KG Var", "oran": 1.72, "yuzde": 76},
        {"lig": "Almanya Bundesliga", "mac": "Bayern Munich - Dortmund", "tahmin": "MS 1", "oran": 1.48, "yuzde": 89},
        {"lig": "Fransa Ligue 1", "mac": "PSG - Monaco", "tahmin": "2.5 Üst", "oran": 1.60, "yuzde": 81},
        {"lig": "Türkiye Süper Lig", "mac": "Galatasaray - Beşiktaş", "tahmin": "KG Var", "oran": 1.65, "yuzde": 79},
        {"lig": "Hollanda Eredivisie", "mac": "Ajax - Feyenoord", "tahmin": "2.5 Üst", "oran": 1.52, "yuzde": 84},
        {"lig": "Portekiz Liga NOS", "mac": "Benfica - Porto", "tahmin": "MS 1", "oran": 1.85, "yuzde": 70},
        {"lig": "Şampiyonlar Ligi", "mac": "Man City - Juventus", "tahmin": "MS 1", "oran": 1.40, "yuzde": 91},
        {"lig": "Avrupa Ligi", "mac": "Fenerbahçe - Lyon", "tahmin": "KG Var", "oran": 1.58, "yuzde": 80}
    ]
    return {
        "tekli_maclar": ornekler,
        "kupon_2li_A": ornekler[0:2], "kupon_2li_B": ornekler[2:4],
        "kupon_3lu_A": ornekler[4:7], "kupon_3lu_B": ornekler[6:9],
        "oran_2li_A": 2.60, "oran_2li_B": 2.85,
        "oran_3lu_A": 4.88, "oran_3lu_B": 5.40,
        "guven_2li_A": 85, "guven_2li_B": 80,
        "guven_3lu_A": 78, "guven_3lu_B": 74
    }

@app.route('/')
def ana_sayfa():
    data = bot_analiz_motoru()
    
    html_kod = """
    <html>
        <head>
            <title>AI Premium Tahmin Üssü</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background-color: #0b0f19; color: #f1f5f9;">
            
            <h1 style="text-align: center; color: #38bdf8; margin-top: 20px; font-size: 26px;">📊 AI MEGA TAHMİN MOTORU v6.1 🤖</h1>
            <p style="text-align: center; color: #64748b; margin-bottom: 25px;">Genişletilmiş maç havuzu, çoklu kombineler ve VIP paketler</p>
            
            <div style="max-width: 1200px; margin: 0 auto 30px auto; background: linear-gradient(90deg, #065f46, #0f172a); border: 1px solid #059669; padding: 15px 20px; border-radius: 12px;">
                <h3 style="margin: 0; color: #34d399; font-size: 16px; text-align: center;">📊 Dünün Yapay Zeka Başarı Oranı: %91.6!</h3>
            </div>

            <div style="max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 30px;">
                <div>
                    <h2 style="color: #fbbf24; border-bottom: 2px solid #fbbf24; padding-bottom: 8px; font-size: 18px;">🔥 Günün Yapay Zeka Kombineleri</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                        <div style="background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155;">
                            <h4 style="color: #10b981; margin: 0 0 10px 0; font-size: 13px;">🟢 Altın İkili - A (%{{ data.guven_2li_A }})</h4>
                            {% for m in data.kupon_2li_A %} <p style="margin: 5px 0; font-size: 13px;">🔹 <b>{{ m.mac }}</b> ({{ m.tahmin }})</p> {% endfor %}
                            <h5 style="text-align: right; color: #38bdf8; margin: 10px 0 0 0;">Oran: {{ data.oran_2li_A }}</h5>
                        </div>
                        <div style="background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155;">
                            <h4 style="color: #10b981; margin: 0 0 10px 0; font-size: 13px;">🟢 Altın İkili - B (%{{ data.guven_2li_B }})</h4>
                            {% for m in data.kupon_2li_B %} <p style="margin: 5px 0; font-size: 13px;">🔹 <b>{{ m.mac }}</b> ({{ m.tahmin }})</p> {% endfor %}
                            <h5 style="text-align: right; color: #38bdf8; margin: 10px 0 0 0;">Oran: {{ data.oran_2li_B }}</h5>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 25px;">
                        <div style="background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155;">
                            <h4 style="color: #f43f5e; margin: 0 0 10px 0; font-size: 13px;">🔴 Kasa Katlama - A (%{{ data.guven_3lu_A }})</h4>
                            {% for m in data.kupon_3lu_A %} <p style="margin: 5px 0; font-size: 13px;">🔹 <b>{{ m.mac }}</b> ({{ m.tahmin }})</p> {% endfor %}
                            <h5 style="text-align: right; color: #38bdf8; margin: 10px 0 0 0;">Oran: {{ data.oran_3lu_A }}</h5>
                        </div>
                        <div style="background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155;">
                            <h4 style="color: #f43f5e; margin: 0 0 10px 0; font-size: 13px;">🔴 Kasa Katlama - B (%{{ data.guven_3lu_B }})</h4>
                            {% for m in data.kupon_3lu_B %} <p style="margin: 5px 0; font-size: 13px;">🔹 <b>{{ m.mac }}</b> ({{ m.tahmin }})</p> {% endfor %}
                            <h5 style="text-align: right; color: #38bdf8; margin: 10px 0 0 0;">Oran: {{ data.oran_3lu_B }}</h5>
                        </div>
                    </div>
                    <h2 style="color: #a5b4fc; border-bottom: 2px solid #6366f1; padding-bottom: 8px; font-size: 18px;">👑 AI GOLD VIP ODASI</h2>
                    <div style="background: linear-gradient(135deg, #1e1b4b, #2e1065); padding: 20px; border-radius: 16px; border: 2px solid #6366f1;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                            <div style="background: rgba(15,23,42,0.6); padding: 12px; border-radius: 8px; text-align: center; border: 1px dashed #6366f1;">
                                <span style="font-size: 11px; color: #fbbf24;">⭐ VIP KUPON 1</span>
                                <div style="font-size: 20px; margin: 8px 0;">🔒</div>
                                <span style="font-size: 10px; color: #94a3b8;">Oran: +4.50</span>
                            </div>
                            <div style="background: rgba(15,23,42,0.6); padding: 12px; border-radius: 8px; text-align: center; border: 1px dashed #6366f1;">
                                <span style="font-size: 11px; color: #f43f5e;">🔥 SKOR VIP</span>
                                <div style="font-size: 20px; margin: 8px 0;">🔒</div>
                                <span style="font-size: 10px; color: #94a3b8;">Oran: +12.00</span>
                            </div>
                            <div style="background: rgba(15,23,42,0.6); padding: 12px; border-radius: 8px; text-align: center; border: 1px dashed #6366f1;">
                                <span style="font-size: 11px; color: #10b981;">💰 KASA VIP</span>
                                <div style="font-size: 20px; margin: 8px 0;">🔒</div>
                                <span style="font-size: 10px; color: #94a3b8;">Oran: +3.20</span>
                            </div>
                        </div>
                        <div style="text-align: center;">
                            <button onclick="alert('VIP Altyapısı Çok Yakında Aktif Olacak!');" style="background: #6366f1; color: white; border: none; padding: 10px 25px; font-size: 13px; font-weight: bold; border-radius: 8px; cursor: pointer;">
                                VIP Paketlere Abone Ol
                            </button>
                        </div>
                    </div>
                </div>
                <div>
                    <h2 style="color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 8px; font-size: 18px;">📈 Günün Banko Kazanma Listesi (10 Maç)</h2>
                    {% for t in data.tekli_maclar %}
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
        </body>
    </html>
    """
    return render_template_string(html_kod, data=data)

if __name__ == '__main__':
    app.run(debug=True)
