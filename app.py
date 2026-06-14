from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

# API Bilgileri
API_KEY = "999e0bfd03e0268f0ad00d6619da543f"
HEADERS = {'x-rapidapi-host': 'v3.football.api-sports.io', 'x-rapidapi-key': API_KEY}

def get_live_matches():
    try:
        bugun = datetime.now().strftime('%Y-%m-%d')
        url = f"https://v3.football.api-sports.io/fixtures?date={bugun}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json().get("response", [])
        
        # Sadece ilk 10 maçı alalım ki liste çok uzamasın
        return data[:10]
    except:
        return []

@app.route('/')
def index():
    maclar = get_live_matches()
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #030712; color: #fff; font-family: sans-serif; padding: 15px; }
            .tabs { display: flex; gap: 5px; margin-bottom: 20px; border-bottom: 1px solid #374151; padding-bottom: 10px; }
            button { padding: 10px; background: #1f2937; border: none; color: white; border-radius: 5px; cursor: pointer; flex: 1; }
            .active-btn { background: #0ea5e9 !important; }
            .tab-pane { display: none; }
            .active-pane { display: block; }
            .card { background: #111827; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #374151; }
        </style>
    </head>
    <body>
        <div class="tabs">
            <button onclick="openTab(event, 'bugun')" class="active-btn" id="defaultOpen">Bugünün Maçları</button>
            <button onclick="openTab(event, 'arsiv')">Analizler</button>
        </div>

        <div id="bugun" class="tab-pane active-pane">
            {% if maclar %}
                {% for m in maclar %}
                <div class="card">
                    <strong>{{ m.teams.home.name }} vs {{ m.teams.away.name }}</strong><br>
                    <small style="color: #9ca3af;">{{ m.league.name }}</small>
                </div>
                {% endfor %}
            {% else %}
                <div class="card">Bugün canlı maç bulunamadı veya API bağlantısı kesik.</div>
            {% endif %}
        </div>

        <div id="arsiv" class="tab-pane">
            <div class="card">Buraya ileride kazanan/kaybeden analizlerini ekleyeceğiz.</div>
        </div>

        <script>
            function openTab(evt, name) {
                document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active-pane'));
                document.querySelectorAll('button').forEach(b => b.classList.remove('active-btn'));
                document.getElementById(name).classList.add('active-pane');
                evt.currentTarget.classList.add('active-btn');
            }
        </script>
    </body>
    </html>
    ''', maclar=maclar)

if __name__ == '__main__':
    app.run(debug=True)
