import requests
from bs4 import BeautifulSoup

def generar_lista():
    url_agenda = "https://daddylive.cv/schedule/schedule-block.php"
    # El Referer es la "llave" para que el video no de error
    referer = "|Referer=https://daddylive.cv/&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Inicio del archivo M3U
    m3u_content = "#EXTM3U\n"
    
    # --- 1. SECCIÓN DE CANALES FIJOS ---
    # IDs verificados de DaddyLive para deportes
    canales_fijos = [
        {"nombre": "ESPN PREMIUM", "id": "105"},
        {"nombre": "DAZN 1 ESPAÑA", "id": "538"},
        {"nombre": "TYC SPORTS", "id": "112"},
        {"nombre": "FOX SPORTS 1", "id": "16"},
        {"nombre": "DIRECTV SPORTS", "id": "366"}
    ]
    
    for canal in canales_fijos:
        m3u_content += f"#EXTINF:-1 group-title='CANALES FIJOS VIP', {canal['nombre']}\n"
        # Concatenamos la URL con el Referer al final
        m3u_content += f"https://daddylive.cv/embed/stream.php?id={canal['id']}{referer}\n"

    # --- 2. SECCIÓN DE EVENTOS AUTOMÁTICOS ---
    try:
        response = requests.get(url_agenda, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos los eventos en la tabla de la agenda
        for fila in soup.find_all('tr'):
            cols = fila.find_all('td')
            if len(cols) >= 2:
                evento = cols[0].text.strip()
                link_tag = cols[1].find('a')
                if link_tag and 'href' in link_tag.attrs:
                    link_raw = link_tag['href']
                    # Extraer el ID del link (ej: stream-50.php -> 50)
                    canal_id = link_raw.split('-')[-1].split('.')[0]
                    
                    m3u_content += f"#EXTINF:-1 group-title='PARTIDOS DE HOY', {evento}\n"
                    m3u_content += f"https://daddylive.cv/embed/stream.php?id={canal_id}{referer}\n"
    except Exception as e:
        print(f"Error capturando agenda: {e}")

    # Guardar el archivo final en el repositorio
    with open("lista_sistema_ln.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("¡Lista corregida y actualizada!")

if __name__ == "__main__":
    generar_lista()
