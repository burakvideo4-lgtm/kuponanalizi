from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def ana_sayfa():
    maclar = [
        {"mac": "Galatasaray - Fenerbahçe", "tahmin": "2.5 Üst", "oran": "1.65"},
        {"mac": "Real Madrid - Barcelona", "tahmin": "Maç Sonu 1", "oran": "1.80"},
        {"mac": "Liverpool - Arsenal", "tahmin": "Karşılıklı Gol Var", "oran": "1.55"}
    ]
    secilen = random.choice(maclar)
    
    return f"""
    <html>
        <head>
            <title>Canlı Maç Tahmin Botu</title>
            <meta charset="utf-8">
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px; background-color: #f4f4f4;">
            <h1>🤖 Otomatik Maç Tahmin Botu v1.0 🤖</h1>
            <p>Sitemiz şu an internette canlı yayında!</p>
            <div style="background: white; display: inline-block; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); min-width: 300px;">
                <h2>{secilen['mac']}</h2>
                <h3 style="color: green;">Tahmin: {secilen['tahmin']}</h3>
                <p>Oran: {secilen['oran']}</p>
            </div>
            <br><br>
            <button onclick="window.location.reload();" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">Başka Tahmin Getir</button>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
