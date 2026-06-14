from flask import Flask, render_template_string
import requests
import random
from datetime import datetime

app = Flask(__name__)

# API Bilgileri
API_KEY = "999e0bfd03e0268f0ad00d6619da543f"
API_URL = "https://v3.football.api-sports.io/fixtures"

def veri_cek():
    # Canlı veri çekmeye çalış
    try:
        headers = {'x-rapidapi-host': 'v3.football.api-sports.io', 'x-rapidapi-key': API_KEY}
        bugun = datetime.now().strftime('%Y-%m-%d')
        res = requests.get(f"{API_URL}?date={bugun}", headers=headers, timeout=3)
        data = res.json().get("response", [])
        
        if not data: return mock_data() # Veri yoksa örnek veriye dön
        
        # Basit bir formatla döndür
        return {"durum": "canli", "maclar": data[:10]}
    except:
        return mock_data() # Hata olursa örnek veriye dön

def mock_data():
    return {
        "durum": "arsiv",
        "maclar": [
            {"teams": {"home": {"name": "Arsenal"}, "away": {"name": "Chelsea"}}, "league": {"name": "Premier Lig"}},
            {"teams": {"home": {"name": "Real Madrid"}, "away": {"name": "Barcelona"}}, "league": {"name": "La Liga"}},
            {"teams": {"home": {"name": "Milan"}, "away": {"name": "Inter"}}, "league": {"name": "Serie A"}}
        ]
    }

@app.route('/')
def index():
    data = veri_cek()
    
    html = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>BETAI // Smart Portal</title>
    <style>
        body { background: #030712; color: #fff; font-family: sans-serif; padding: 20px; }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab-btn { padding: 10px 20px; background: #1f2937; border: none; color: #fff; border-radius: 5px; cursor: pointer; }
        .tab-btn.active { background: #0ea5e9; }
        .content { display: none; }
        .content.active { display: block; }
        .card { background: #111827; padding: 15px; border-radius: 8px; border: 1px solid #374151; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="tabs">
        <button class="tab-btn active" onclick="show(event, 'bugun')">🔥 Bugün</button>
        <button class="tab-btn" onclick="show(event, 'arsiv')">📊 Arşiv</button>
    </div>

    <div id="bugun" class="content active">
        <h3>Günün Maçları</h3>
        {% for m in data.maclar %}
        <div class="card">{{ m.teams.home.name }} vs {{ m.teams.away.name }} - {{ m.league.name }}</div>
        {% endfor %}
    </div>

    <div id="arsiv" class="content">
        <h3>Analiz Geçmişi</h3>
        <div class="card">Geçmiş kupon verileri burada listelenecek.</div>
    </div>

    <script>
        function show(evt, id) {
            document.querySelectorAll('.content').forEach(c => c.style.display = 'none');
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(id).style.display = 'block';
            evt.currentTarget.classList.add('active');
        }
    </script>
</body>
</html>"""
    return render_template_string(html, data=data)

if __name__ == '__main__':
    app.run(debug=True)
