from flask import Flask, render_template_string
import random

app = Flask(__name__)

API_KEY = "999e0bfd03e0268f0ad00d6619da543f"

def bot_analiz_motoru():
    yedek = sahte_veri_uret()
    try:
        import requests
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(url, headers=headers, timeout=3)
        data = response.json()
        
        if data.get("response") and len(data["response"]) >= 10:
            mac_listesi = data["response"]
            tahmin_havuzu = []
            
            for m in mac_listesi[:25]:
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
                    "oran_3lu_B": round(kupon_3lu_B[0]['oran'] * kupon_3lu_B[1]['oran']
