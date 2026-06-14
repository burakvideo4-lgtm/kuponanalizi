from flask import Flask, render_template_string
import random
import requests

app = Flask(__name__)

API_KEY = "999e0bfd03e0268f0ad00d6619da543f"

def bot_analiz_motoru():
    # Sunucu anlık çökerse veya API yavaşlarsa site hiç beklemeden bu yedek veriyi basacak
    yedek_veri = sahte_veri_uret()
    
    try:
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': API_KEY
        }
        # Zaman aşımını 3 saniye yaparak sunucunun kilitlenmesini önlüyoruz
        response = requests.get(url, headers=headers, timeout=3)
        data = response.json()
        
        if not data.get("response") or len(data["response"]) < 10:
            return yedek_veri
            
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
                
        if len(tahmin_havuzu) < 10:
            return yedek_veri
            
        tahmin_havuzu = sorted(tahmin_havuzu, key=lambda x: x['yuzde'], reverse=True)
        
        return {
            "tekli_maclar": tahmin_havuzu[:10],
            "kupon_2li_A": tahmin_havuzu[0:2],
            "kupon_2li_B": tahmin_havuzu[2:4],
            "kupon_3lu_A": tahmin_havuzu[4:7],
            "kupon_3lu_B": tahmin_havuzu[7:10],
            "oran_2li_A": round(tahmin_havuzu[0]['oran'] * tahmin_havuzu[1]['oran'], 2),
            "oran_2li_B": round(tahmin_havuzu[2]['oran'] * tahmin_havuzu[3]['oran'], 2),
            "oran_3lu_A": round(tahmin_havuzu[4]['oran'] * tahmin_havuzu[5]['oran'] * tahmin_havuzu[6]['oran'], 2),
            "oran_3lu_B": round(tahmin_havuzu[7]['oran'] * tahmin_havuzu[8]['oran'] * tahmin_havuzu[9]['oran'], 2),
            "guven_2li_A": round((tahmin_havuzu[0]['yuzde'] + tahmin_havuzu[1]['yuzde']) / 2),
            "guven_2li_B": round((tahmin_havuzu[2]['yuzde'] + tahmin_havuzu[3]['yuzde']) / 2),
            "guven_3lu_A": round((tahmin_havuzu[4]['yuzde'] + tahmin_havuzu[5]['yuzde'] + tahmin_havuzu[6]['yuzde']) / 3),
            "guven_3lu_B": round((tahmin_havuzu[7]['yuzde'] + tahmin_havuzu[8]['yuzde'] + tahmin_havuzu[9]['yuzde']) / 3)
        }
    except:
        return yedek_veri

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
        "oran_2li
