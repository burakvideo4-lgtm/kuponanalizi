from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "999e0bfd03e0268f0ad00d6619da543f"
API_URL = "https://v3.football.api-sports.io/fixtures"

DURUM_ETIKETLERI = {
    "NS": ("Başlamadı", "#6b7280"),
    "1H": ("1. Yarı", "#10b981"),
    "HT": ("Devre Arası", "#f59e0b"),
    "2H": ("2. Yarı", "#10b981"),
    "ET": ("Uzatma", "#f59e0b"),
    "P":  ("Penaltı", "#f59e0b"),
    "FT": ("Bitti", "#3b82f6"),
    "AET": ("Bitti (UZ)", "#3b82f6"),
    "PEN": ("Bitti (PEN)", "#3b82f6"),
    "PST": ("Ertelendi", "#ef4444"),
    "CANC": ("İptal", "#ef4444"),
    "SUSP": ("Askıya Alındı", "#ef4444"),
    "INT": ("Yarıda Kesildi", "#ef4444"),
    "LIVE": ("Canlı", "#10b981"),
}

def macları_getir():
    try:
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": API_KEY
        }
        bugun = datetime.now().strftime("%Y-%m-%d")
        response = requests.get(f"{API_URL}?date={bugun}", headers=headers, timeout=8)
        data = response.json()
        mac_listesi = data.get("response", [])

        maclar = []
        for m in mac_listesi:
            try:
                durum_kodu = m["fixture"]["status"]["short"]
                durum_dakika = m["fixture"]["status"].get("elapsed")
                durum_label, durum_renk = DURUM_ETIKETLERI.get(durum_kodu, (durum_kodu, "#6b7280"))

                saat_utc = m["fixture"]["date"]  # ISO 8601
                # Saati kısalt: "2024-06-14T18:00:00+00:00" → "18:00"
                try:
                    saat = datetime.fromisoformat(saat_utc).strftime("%H:%M")
                except:
                    saat = "--:--"

                ev = m["teams"]["home"]["name"]
                dep = m["teams"]["away"]["name"]
                ev_logo = m["teams"]["home"].get("logo", "")
                dep_logo = m["teams"]["away"].get("logo", "")

                ev_gol = m["goals"]["home"]
                dep_gol = m["goals"]["away"]

                lig_adi = m["league"]["name"]
                ulke = m["league"]["country"]
                lig_logo = m["league"].get("logo", "")

                maclar.append({
                    "saat": saat,
                    "durum": durum_label,
                    "durum_renk": durum_renk,
                    "durum_dakika": durum_dakika,
                    "ev": ev,
                    "dep": dep,
                    "ev_logo": ev_logo,
                    "dep_logo": dep_logo,
                    "ev_gol": ev_gol,
                    "dep_gol": dep_gol,
                    "lig": f"{ulke} — {lig_adi}",
                    "lig_logo": lig_logo,
                })
            except:
                continue

        # Lige göre grupla
        gruplar = {}
        for mac in maclar:
            gruplar.setdefault(mac["lig"], {"logo": mac["lig_logo"], "maclar": []})
            gruplar[mac["lig"]]["maclar"].append(mac)

        return gruplar, len(maclar), None

    except Exception as e:
        return {}, 0, str(e)


@app.route("/")
def ana_sayfa():
    gruplar, toplam, hata = macları_getir()
    bugun = datetime.now().strftime("%d %B %Y")

    html = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bugünün Maçları</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
      background: #0c0f1a;
      color: #e2e8f0;
      min-height: 100vh;
      padding: 24px 16px 48px;
    }

    .container { max-width: 860px; margin: 0 auto; }

    /* Header */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-bottom: 20px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      margin-bottom: 28px;
    }
    .logo-text {
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #f8fafc;
    }
    .logo-text span { color: #38bdf8; }
    .meta {
      font-size: 13px;
      color: #64748b;
      text-align: right;
    }
    .meta strong { color: #94a3b8; }

    /* Hata */
    .hata-kutu {
      background: rgba(239,68,68,0.1);
      border: 1px solid rgba(239,68,68,0.3);
      border-radius: 12px;
      padding: 20px;
      color: #fca5a5;
      font-size: 14px;
    }

    /* Lig grubu */
    .lig-grup { margin-bottom: 28px; }

    .lig-baslik {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      background: rgba(255,255,255,0.03);
      border-radius: 10px 10px 0 0;
      border: 1px solid rgba(255,255,255,0.06);
      border-bottom: none;
    }
    .lig-baslik img { width: 20px; height: 20px; object-fit: contain; }
    .lig-adi { font-size: 12px; font-weight: 700; color: #94a3b8; letter-spacing: 0.6px; text-transform: uppercase; }

    /* Maç satırı */
    .mac-satir {
      display: grid;
      grid-template-columns: 60px 1fr auto 1fr 70px;
      align-items: center;
      gap: 8px;
      padding: 14px 16px;
      background: rgba(15, 23, 42, 0.5);
      border: 1px solid rgba(255,255,255,0.05);
      border-top: none;
      transition: background 0.15s;
    }
    .mac-satir:last-child { border-radius: 0 0 10px 10px; }
    .mac-satir:hover { background: rgba(30,41,59,0.6); }

    /* Saat / Durum */
    .saat-blok { text-align: center; }
    .saat { font-size: 15px; font-weight: 700; color: #f1f5f9; font-variant-numeric: tabular-nums; }
    .durum-badge {
      display: inline-block;
      margin-top: 4px;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 99px;
      letter-spacing: 0.4px;
    }

    /* Takım */
    .takim {
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 0;
    }
    .takim.dep { flex-direction: row-reverse; }
    .takim img { width: 22px; height: 22px; object-fit: contain; flex-shrink: 0; }
    .takim-adi {
      font-size: 13px;
      font-weight: 600;
      color: #e2e8f0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .takim.dep .takim-adi { text-align: right; }

    /* Skor */
    .skor {
      text-align: center;
      font-size: 18px;
      font-weight: 800;
      color: #f8fafc;
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
      letter-spacing: 2px;
    }
    .skor.yok { font-size: 20px; color: #334155; letter-spacing: 1px; }

    /* Boş durum */
    .bos {
      text-align: center;
      padding: 60px 20px;
      color: #475569;
      font-size: 15px;
    }
    .bos span { font-size: 40px; display: block; margin-bottom: 12px; }

    @media (max-width: 560px) {
      .mac-satir { grid-template-columns: 52px 1fr auto 1fr 52px; gap: 6px; padding: 12px 10px; }
      .takim-adi { font-size: 12px; }
      .skor { font-size: 15px; }
    }
  </style>
</head>
<body>
<div class="container">
  <header>
    <div class="logo-text">⚽ Fikstür<span>.</span></div>
    <div class="meta">
      <strong>{{ bugun }}</strong><br>
      {{ toplam }} maç listeleniyor
    </div>
  </header>

  {% if hata %}
  <div class="hata-kutu">
    ⚠️ API'ye bağlanılamadı: <code>{{ hata }}</code>
  </div>
  {% elif not gruplar %}
  <div class="bos">
    <span>😴</span>
    Bugün için maç bulunamadı.
  </div>
  {% else %}
    {% for lig_adi, lig_data in gruplar.items() %}
    <div class="lig-grup">
      <div class="lig-baslik">
        {% if lig_data.logo %}<img src="{{ lig_data.logo }}" alt="">{% endif %}
        <span class="lig-adi">{{ lig_adi }}</span>
      </div>

      {% for mac in lig_data.maclar %}
      <div class="mac-satir">
        <!-- Saat / Durum -->
        <div class="saat-blok">
          <div class="saat">{{ mac.saat }}</div>
          <span class="durum-badge" style="background: {{ mac.durum_renk }}22; color: {{ mac.durum_renk }}; border: 1px solid {{ mac.durum_renk }}44;">
            {% if mac.durum_dakika %}{{ mac.durum_dakika }}'{% else %}{{ mac.durum }}{% endif %}
          </span>
        </div>

        <!-- Ev Takımı -->
        <div class="takim">
          {% if mac.ev_logo %}<img src="{{ mac.ev_logo }}" alt="">{% endif %}
          <span class="takim-adi">{{ mac.ev }}</span>
        </div>

        <!-- Skor -->
        {% if mac.ev_gol is not none and mac.dep_gol is not none %}
          <div class="skor">{{ mac.ev_gol }} – {{ mac.dep_gol }}</div>
        {% else %}
          <div class="skor yok">vs</div>
        {% endif %}

        <!-- Deplasman Takımı -->
        <div class="takim dep">
          {% if mac.dep_logo %}<img src="{{ mac.dep_logo }}" alt="">{% endif %}
          <span class="takim-adi">{{ mac.dep }}</span>
        </div>

        <!-- Durum (geniş metin) -->
        <div style="text-align:center; font-size: 11px; color: {{ mac.durum_renk }}; font-weight: 600;">{{ mac.durum }}</div>
      </div>
      {% endfor %}
    </div>
    {% endfor %}
  {% endif %}
</div>
</body>
</html>"""

    return render_template_string(html, gruplar=gruplar, toplam=toplam, bugun=bugun, hata=hata)


if __name__ == "__main__":
    app.run(debug=True)
