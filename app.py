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
        return response.json().get("response", [])[:12]
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
            :root { --bg: #0f172a; --card: #1e293b; --accent: #38bdf8; --text: #f1f5f9; }
            body { background: var(--bg); color: var(--text); font-family: 'Inter', system-ui, sans-serif; margin: 0; padding: 20px; }
            
            .nav-tabs { display: flex; gap: 10px; margin-bottom: 25px; background: var(--card); padding: 5px; border-radius: 12px; }
            .tab-btn { flex: 1; padding: 12px; border: none; background: transparent; color: #94a3b8; font-weight: 600; border-radius: 8px; cursor: pointer; transition: 0.3s; }
            .tab-btn.active { background: var(--accent); color: white; }
            
            .tab-content { display: none; }
            .tab-content.active { display: block; }
            
            .match-card { background: var(--card); padding: 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid var(--accent); display: flex; justify-content: space-between; align-items: center; }
            .league-name { font-size: 10px; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; }
            .team-names { font-weight: 700; margin-top: 5px; }
        </style>
    </head>
    <body>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab(event, 'bugun')">🔥 Canlı</button>
            <button class="tab-btn" onclick="switchTab(event, 'arsiv')">📈 Analiz</button>
        </div>

        <div id="bugun" class="tab-content active">
            {% if maclar %}
                {% for m in maclar %}
                <div class="match-card">
                    <div>
                        <div class="league-name">{{ m.league.name }}</div>
                        <div class="team-names">{{ m.teams.home.name }} vs {{ m.teams.away.name }}</div>
                    </div>
                    <div style="font-size: 12px;">{{ m.fixture.status.short }}</div>
                </div>
                {% endfor %}
            {% else %}
                <div style="text-align: center; color: #64748b;">Bugün veri akışı bulunamadı.</div>
            {% endif %}
        </div>

        <div id="arsiv" class="tab-content">
            <div class="match-card">
                <div>Kasa Katlama (Kazanılan)</div>
                <div style="color: #22c55e;">+3.45 Oran</div>
            </div>
        </div>

        <script>
            function switchTab(evt, name) {
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.getElementById(name).classList.add('active');
                evt.currentTarget.classList.add('active');
            }
        </script>
    </body>
    </html>
    ''', maclar=maclar)

if __name__ == '__main__':
    app.run(debug=True)
