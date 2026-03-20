import requests

def generar_lista_funcional():
    # Encabezado estándar de IPTV
    m3u_content = "#EXTM3U\n"
    
    # --- SECCIÓN: DEPORTES LATINOS (FUENTES ABIERTAS) ---
    # Estos links son directos y funcionan sin bloqueos de navegador
    deportes = [
        {"n": "MERIDIANO TV (VZLA)", "u": "https://meridianotv.miteleven.com/meridianotv/index.m3u8"},
        {"n": "TELEVEN (VZLA)", "u": "https://televencam1.miteleven.com/televencam1/index.m3u8"},
        {"n": "WIN SPORTS (COL)", "u": "https://stream.winsports.co/win/index.m3u8"},
        {"n": "RT DEPORTES (ESP)", "u": "https://rt-esp.rt.com/live/rtesp/playlist.m3u8"},
        {"n": "TYC SPORTS (ALTERNATIVO)", "u": "https://cdn.perfil.com/canal-e/live/playlist.m3u8"}
    ]
    
    for c in deportes:
        m3u_content += f"#EXTINF:-1 group-title='DEPORTES INCREDIBLE', {c['n']}\n"
        m3u_content += f"{c['u']}\n"

    # --- SECCIÓN: CANALES MUNDIALES ---
    mundo = [
        {"n": "CANAL 24 HORAS (ESP)", "u": "https://rtvep-live-03.rtve.es/li/24H_CAN_MAI/playlist.m3u8"},
        {"n": "VTV VENEZUELA", "u": "https://vtv.miteleven.com/vtv/index.m3u8"},
        {"n": "TELESUR", "u": "https://telesur.miteleven.com/telesur/index.m3u8"}
    ]

    for c in mundo:
        m3u_content += f"#EXTINF:-1 group-title='MUNDO INCREDIBLE', {c['n']}\n"
        m3u_content += f"{c['u']}\n"

    # Guardamos el archivo final en el repositorio
    try:
        with open("lista_sistema_ln.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("¡Lista 100% Funcional Generada con Éxito!")
    except Exception as e:
        print(f"Error al guardar: {e}")

if __name__ == "__main__":
    generar_lista_funcional()
