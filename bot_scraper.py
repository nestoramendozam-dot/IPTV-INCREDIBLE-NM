import requests
from bs4 import BeautifulSoup

def generar_lista():
    url_agenda = "https://daddylive.cv/schedule/schedule-block.php"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    m3u_content = "#EXTM3U\n"
    
    # CANALES FIJOS (Los que siempre salen en la app)
    canales_fijos = [
        {"nombre": "ESPN PREMIUM", "id": "105"},
        {"nombre": "DAZN 1 ESPAÑA", "id": "538"},
        {"nombre": "TYC SPORTS", "id": "112"},
        {"nombre": "FOX SPORTS 1", "id": "16"}
    ]
    
    for canal in canales_fijos:
        m3u_content += f"#EXTINF:-1 group-title='CANALES FIJOS VIP', {canal['nombre']}\n"
        m3u_content += f"https://daddylive.cv/embed/stream.php?id={canal['id']}\n"

    # EVENTOS AUTOMÁTICOS DEL DÍA
    try:
        response = requests.get(url_agenda, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for fila in soup.find_all('tr'):
            cols = fila.find_all('td')
            if len(cols) >= 2:
                evento = cols[0].text.strip()
                link_raw = cols[1].find('a')['href']
                canal_id = link_raw.split('-')[-1].split('.')[0]
                m3u_content += f"#EXTINF:-1 group-title='PARTIDOS DE HOY', {evento}\n"
                m3u_content += f"https://daddylive.cv/embed/stream.php?id={canal_id}\n"
    except:
        pass

    with open("lista_sistema_ln.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    generar_lista()
