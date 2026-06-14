from flask import Flask, render_template_string
import requests
import random
from datetime import datetime

app = Flask(__name__)

# Senin API anahtarın
API_KEY = "999e0bfd03e0268f0ad00d6619da543f"

def maclari_ve_tahminleri_getir():
    bugun = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={bugun}"
    
    headers = {
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'x-rapidapi-key': API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Eğer API'den maç geldiyse
        if data.get("response"):
            mac_listesi = data["response"]
            
            # Rastgele 3 tane maç seçelim (başlangıç için filtreleme)
            secilen_maclar = random.sample(mac_listesi, min(len(mac_listesi), 3))
            
            tahmin_sonuclari = []
            tahmin_secenekleri = ["Maç Sonu 1", "Maç Sonu 2", "2.5 Üst", "2.5 Alt", "Karşılıklı Gol Var"]
            
            for m in secilen_maclar:
                ev = m['teams']['home']['name']
                deplasman = m['teams']['away']['name']
                lig = m['league']['name']
                
                # Şimdilik rastgele tahmin üretiyoruz, algoritmayı buraya yazacağız
                tahmin = random.choice(tahmin_secenekleri)
                oran = round(random.uniform(1.40, 2.10), 2)
                
                tahmin_sonuclari.append({
                    "lig": lig,
                    "mac": f"{ev} - {deplasman}",
                    "tahmin": tahmin,
                    "oran": oran
                })
            return tahmin_sonuclari
        else:
            return [{"lig": "Sistem", "mac": "Bugün için uygun maç bulunamadı veya API limiti doldu.", "tahmin": "-", "oran": "-"}]
            
    except Exception as e:
        return [{"lig": "Hata", "mac": f"Bağlantı hatası: {str(e)}", "tahmin": "-", "oran": "-"}]

@app.route('/')
def ana_sayfa():
    tahminler = maclari_ve_tahminleri_getir()
    
    # HTML Tasarımı (Daha şık ve dinamik liste hali)
    html_kod = """
    <html>
        <head>
            <title>Yapay Zeka Maç Tahmin Botu</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 20px; background-color: #f0f2f5;">
            <h1 style="color: #1a1a1a; margin-top: 30px;">🤖 Otomatik Maç Tahmin Botu v2.0 🤖</h1>
            <p style="color: #666;">API ile canlı çekilen günün maç tahminleri aşağıdadır:</p>
            
            <div style="max-width: 600px; margin: 0 auto; text-align: left;">
                {% for t in tahminler %}
                <div style="background: white; padding: 20px; margin-bottom: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #2ecc71;">
                    <span style="font-size: 12px; color: #999; text-transform: uppercase; font-weight: bold;">{{ t.lig }}</span>
                    <h3 style="margin: 5px 0 10px 0; color: #2c3e50;">{{ t.mac }}</h3>
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #fdfefe; padding: 10px; border-radius: 6px; border: 1px dashed #ddd;">
                        <span style="font-weight: bold; color: #27ae60;">Tahmin: {{ t.tahmin }}</span>
                        <span style="background: #e8f8f5; color: #117a65; padding: 5px 10px; border-radius: 4px; font-weight: bold;">Oran: {{ t.oran }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <br>
            <button onclick="window.location.reload();" style="padding: 12px 25px; font-size: 16px; background-color: #3498db; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.3s;">
                Tahminleri Yenile
            </button>
        </body>
    </html>
    """
    return render_template_string(html_kod, tahminler=tahminler)

if __name__ == '__main__':
    app.run(debug=True)
