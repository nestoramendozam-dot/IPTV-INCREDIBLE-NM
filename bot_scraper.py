import requests
from bs4 import BeautifulSoup

def generar_lista_final():
    base_url = "https://daddylive.cv"
    # Usaremos un proxy de referer conocido para engañar al servidor desde la app
    proxy_suffix = "|Referer=https://daddylive.cv/&User-Agent=Mozilla/5.0"
    
    m3u_content = "#EXTM3U\n"
    
    # CANALES FIJOS - Intentando con el formato de stream directo de daddylive
    canales_fijos = [
        {"nombre": "ESPN PREMIUM", "id": "105"},
        {"nombre": "DAZN 1 ESPAÑA", "id": "538"},
        {"nombre": "TYC SPORTS", "id": "112"},
        {"nombre": "FOX SPORTS 1", "id": "16"}
    ]
    
    for canal in canales_fijos:
        m3u_content += f"#EXTINF:-1 group-title='IPTV INCREDIBLE VIP', {canal['nombre']}\n"
        # Probamos con el servidor de stream directo + el bypass de referer
        m3u_content += f"https://daddylive.cv/embed/stream.php?id={canal['id']}{proxy_suffix}\n"

    # AGGENDA AUTOMÁTICA
    try:
        url_agenda = f"{base_url}/schedule/schedule-block.php"
        response = requests.get(url_agenda, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for fila in soup.find_all('tr'):
            cols = fila.find_all('td')
            if len(cols) >= 2:
                evento = cols[0].text.strip()
                link_tag = cols[1].find('a')
                if link_tag:
                    # Extraemos el ID del canal del evento
                    id_evento = link_tag['href'].split('-')[-1].split('.')[0]
                    m3u_content += f"#EXTINF:-1 group-title='PARTIDOS DE HOY', {evento}\n"
                    m3u_content += f"https://daddylive.cv/embed/stream.php?id={id_evento}{proxy_suffix}\n"
    except:
        pass

    with open("lista_sistema_ln.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    generar_lista_final()
