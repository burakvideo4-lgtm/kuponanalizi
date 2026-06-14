from flask import Flask, render_template_string
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}


def api_get(endpoint, params=None):
    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            headers=HEADERS,
            params=params,
            timeout=15
        )

        return response.json().get("response", [])

    except Exception as e:
        print("API ERROR:", e)
        return []


def get_team_form(team_id):

    fixtures = api_get(
        "fixtures",
        {
            "team": team_id,
            "last": 5
        }
    )

    points = 0

    for match in fixtures:

        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        hg = match["goals"]["home"]
        ag = match["goals"]["away"]

        if hg is None or ag is None:
            continue

        if team_id == home_id:

            if hg > ag:
                points += 3
            elif hg == ag:
                points += 1

        else:

            if ag > hg:
                points += 3
            elif ag == hg:
                points += 1

    return points


def get_goal_average(team_id):

    fixtures = api_get(
        "fixtures",
        {
            "team": team_id,
            "last": 10
        }
    )

    total = 0
    count = 0

    for match in fixtures:

        hg = match["goals"]["home"]
        ag = match["goals"]["away"]

        if hg is not None and ag is not None:
            total += hg + ag
            count += 1

    if count == 0:
        return 0

    return round(total / count, 2)


def get_home_away_strength(team_id):

    fixtures = api_get(
        "fixtures",
        {
            "team": team_id,
            "last": 10
        }
    )

    points = 0

    for match in fixtures:

        hg = match["goals"]["home"]
        ag = match["goals"]["away"]

        if hg is None or ag is None:
            continue

        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        if team_id == home_id:

            if hg > ag:
                points += 3
            elif hg == ag:
                points += 1

        elif team_id == away_id:

            if ag > hg:
                points += 3
            elif ag == hg:
                points += 1

    return points


def get_h2h_score(home_id, away_id):

    matches = api_get(
        "fixtures/headtohead",
        {
            "h2h": f"{home_id}-{away_id}",
            "last": 5
        }
    )

    home_wins = 0
    away_wins = 0

    for m in matches:

        hg = m["goals"]["home"]
        ag = m["goals"]["away"]

        if hg is None or ag is None:
            continue

        if hg > ag:
            home_wins += 1

        elif ag > hg:
            away_wins += 1

    return home_wins - away_wins


def calculate_team_power(team_id):

    form = get_team_form(team_id)
    goals = get_goal_average(team_id)
    strength = get_home_away_strength(team_id)

    score = (
        form * 4 +
        goals * 12 +
        strength * 2
    )

    return round(score, 2)


def analyze_match(home_id, away_id):

    home_power = calculate_team_power(home_id)
    away_power = calculate_team_power(away_id)

    h2h = get_h2h_score(home_id, away_id)

    diff = (home_power - away_power) + (h2h * 4)

    if diff > 15:
        prediction = "MS 1"

    elif diff < -15:
        prediction = "MS 2"

    else:
        prediction = "KG VAR"

    confidence = min(
        95,
        max(
            60,
            int(60 + abs(diff))
        )
    )

    odds = round(
        1.20 + ((100 - confidence) / 50),
        2
    )

    return prediction, confidence, odds


def get_today_predictions():

    today = datetime.now().strftime("%Y-%m-%d")

    fixtures = api_get(
        "fixtures",
        {
            "date": today
        }
    )

    results = []

    for match in fixtures:

        try:

            status = match["fixture"]["status"]["short"]

            if status in ["FT", "AET", "PEN"]:
                continue

            home_id = match["teams"]["home"]["id"]
            away_id = match["teams"]["away"]["id"]

            prediction, confidence, odds = analyze_match(
                home_id,
                away_id
            )

            results.append({
                "league": match["league"]["name"],
                "country": match["league"]["country"],
                "home": match["teams"]["home"]["name"],
                "away": match["teams"]["away"]["name"],
                "prediction": prediction,
                "confidence": confidence,
                "odds": odds
            })

        except Exception as e:
            print(e)

    results.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return results[:20]


HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>BETAI Analytics</title>

<style>

body{
background:#0f172a;
font-family:Arial;
padding:20px;
color:white;
}

h1{
text-align:center;
}

.card{
background:#1e293b;
padding:15px;
border-radius:12px;
margin-bottom:12px;
}

.badge{
background:#2563eb;
padding:5px 10px;
border-radius:8px;
}

.green{
color:#22c55e;
font-weight:bold;
}

</style>

</head>

<body>

<h1>⚽ BETAI ANALYTICS</h1>

{% for m in matches %}

<div class="card">

<div>{{m.country}} - {{m.league}}</div>

<h3>{{m.home}} vs {{m.away}}</h3>

<p>
<span class="badge">{{m.prediction}}</span>
</p>

<p class="green">
Güven: %{{m.confidence}}
</p>

<p>
Oran: {{m.odds}}
</p>

</div>

{% endfor %}

</body>
</html>
"""


@app.route("/")

def home():

    matches = get_today_predictions()

    return render_template_string(
        HTML,
        matches=matches
    )


if __name__ == "__main__":
    app.run(debug=True)
