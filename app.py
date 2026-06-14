from flask import Flask, render_template_string
import requests
import random
from datetime import datetime

app = Flask(__name__)

# API ve Data yapısı aynı kalıyor, sadece HTML/JS kısmını güncelliyoruz
def get_data_mock():
    # Mock data üretimi (API yerine hızlı kontrol için)
    return {
        "guven_2li_A": 88, "guven_2li_B": 82, "guven_3lu_A": 75, "guven_3lu_B": 70,
        "oran_2li_A": 2.85, "oran_2li_B": 2.40, "oran_3lu_A": 4.50, "oran_3lu_B": 3.90,
        "tekli_maclar": [{"lig": "Premier Lig", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55}],
        "kupon_2li_A": [{"mac": "Real - Barca", "tahmin": "2.5 Üst"}, {"mac": "City - Liverpool", "tahmin": "MS 1"}],
        "kupon_2li_B": [{"mac": "Milan - Inter", "tahmin": "KG Var"}, {"mac": "PSG - Monaco", "tahmin": "MS 1"}],
        "kupon_3lu_A": [{"mac": "Roma - Lazio", "tahmin": "2.5 Üst"}, {"mac": "Lyon - Nice", "tahmin": "MS 1"}, {"mac": "Ajax - Feyenoord", "tahmin": "MS 1"}],
        "kupon_3lu_B": [{"mac": "Benfica - Porto", "tahmin": "KG Var"}, {"mac": "Sporting - Braga", "tahmin": "MS 1"}, {"mac": "Boca - River", "tahmin": "2.5 Üst"}]
    }

@app.route('/')
def ana_sayfa():
    d = get_data_mock()
    
    html_kod = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BETAI // Smart Portal</title>
    <style>
        body { font-family: sans-serif; background: #030712; color: #f3f4f6; margin: 0; padding: 15px; }
        .wrapper { max-width: 900px; margin: 0 auto; }
        .tabs-container { display: flex; gap: 5px; background: #1e293b; padding: 5px; border-radius: 10px; overflow-x: auto; }
        .tab-btn { flex: 1; padding: 10px; border: none; background: transparent; color: #9ca3af; cursor: pointer; border-radius: 6px; font-weight: bold; white-space: nowrap; }
        .tab-btn.active { background: #38bdf8; color: white; }
        .tab-content { display: none; padding-top: 20px; }
        .tab-content.active { display: block; }
        .card { background: #111827; padding: 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #374151; }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="tabs-container">
            <button class="tab-btn active" onclick="openTab(event, 'bugun')">🔥 Bugün</button>
            <button class="tab-btn" onclick="openTab(event, 'kazananlar')">✅ Kazananlar</button>
            <button class="tab-btn" onclick="openTab(event, 'kaybedenler')">❌ Kaybedenler</button>
            <button class="tab-btn" onclick="openTab(event, 'rekorlar')">👑 Rekorlar</button>
        </div>

        <div id="bugun" class="tab-content active">
            <h2>Günün Analizleri</h2>
            <div class="card">İçerik burada...</div>
        </div>
        <div id="kazananlar" class="tab-content">
            <h2>Kazananlar Arşivi</h2>
            <div class="card">Tebrikler, her şey yolunda!</div>
        </div>
        <div id="kaybedenler" class="tab-content">
            <h2>Kaybedenler</h2>
            <div class="card">Yarın yeni bir gün!</div>
        </div>
        <div id="rekorlar" class="tab-content">
            <h2>Oran Rekorları</h2>
            <div class="card">Tarihi başarılar...</div>
        </div>
    </div>

    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tab-btn");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
    </script>
</body>
</html>"""
    return render_template_string(html_kod, d=d)

if __name__ == '__main__':
    app.run(debug=True)
