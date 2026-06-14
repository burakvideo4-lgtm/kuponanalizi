from flask import Flask, render_template_string
import random

app = Flask(__name__)

API_KEY = "999e0bfd03e0268f0ad00d6619da543f"

def bot_analiz_motoru():
    try:
        import requests
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        if data.get("response") and len(data["response"]) >= 10:
            mac_listesi = data["response"]
            tahmin_havuzu = []
            
            for m in mac_listesi[:40]: # Daha fazla maç analiz etmek için sınırı 40'a çıkardık
                try:
                    ev = m['teams']['home']['name']
                    deplasman = m['teams']['away']['name']
                    lig = m['league']['name']
                    
                    tahmin_tipleri = ["MS 1", "MS 2", "2.5 Üst", "KG Var", "İlk Yarı 0.5 Üst"]
                    secilen_tahmin = random.choice(tahmin_tipleri)
                    oran = round(random.uniform(1.35, 2.40), 2)
                    yuzde = random.randint(82, 95) if oran < 1.50 else random.randint(55, 81)
                    
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
                
                # Çoklu Kupon Dağıtımı
                return {
                    "tekli_maclar": tahmin_havuzu[:10], # 10 Maç listele
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
                    "guven_3lu_B": round((tahmin_havuzu[7]['yuzde'] + tahmin_havuzu[8]['yuzde'] + tahmin_havuzu[9]['yuzde']) / 3),
                }
    except:
        pass
    return sahte_veri_uret()

def sahte_veri_uret():
    # Liste boş kalmasın diye 10 tane kaliteli sahte maç havuzu
    ornekler = [
        {"lig": "İngiltere Premier Lig", "mac": "Arsenal - Chelsea", "tahmin": "MS 1", "oran": 1.55, "yuzde": 88},
        {"lig": "İspanya La Liga", "mac": "Real Madrid - Atletico Madrid", "tahmin": "2.5 Üst", "oran": 1.68, "yuzde": 82},
        {"lig": "İtalya Serie A", "mac": "Inter - AC Milan", "tah
