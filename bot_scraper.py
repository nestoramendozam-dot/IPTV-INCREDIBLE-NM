import requests
from bs4 import BeautifulSoup

def generar_lista_enlaces_web():
    # URL base de DaddyLive
    base_url = "https://daddylive.cv"
    url_agenda = f"{base_url}/schedule/schedule-block.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    m3u_content = "#EXTM3U\n"
    
    # --- CANALES FIJOS (Acceso Directo Web) ---
    canales_fijos = [
        {"nombre": "ESPN PREMIUM", "id": "105"},
        {"nombre": "DAZN 1 ESPAÑA", "id": "538"},
        {"nombre": "TYC SPORTS", "id": "112"},
        {"nombre": "FOX SPORTS 1", "id": "16"},
        {"nombre": "DIRECTV SPORTS", "id": "366"}
    ]
    
    for canal in canales_fijos:
        m3u_content += f"#EXTINF:-1 group-title='INCREDIBLE WEB-TV', {canal['nombre']}\n"
        # Este link abre la página oficial del canal
        m3u_content += f"{base_url}/stream/stream-{canal['id']}.php\n"

    # --- PARTIDOS DEL DÍA (Automático) ---
    try:
        response = requests.get(url_agenda, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for fila in soup.find_all('tr'):
            cols = fila.find_all('td')
            if len(cols) >= 2:
                evento = cols[0].text.strip()
                link_tag = cols[1].find('a')
                if link_tag and 'href' in link_tag.attrs:
                    # Construimos el link completo a la web del evento
                    link_evento = link_tag['href']
                    if not link_evento.startswith('http'):
                        link_evento = f"{base_url}/{link_evento.lstrip('/')}"
                    
                    m3u_content += f"#EXTINF:-1 group-title='PARTIDOS DE HOY (WEB)', {evento}\n"
                    m3u_content += f"{link_evento}\n"
    except Exception as e:
        print(f"Error: {e}")

    with open("lista_sistema_ln.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("¡Lista de accesos directos actualizada!")

if __name__ == "__main__":
    generar_lista_enlaces_web()
