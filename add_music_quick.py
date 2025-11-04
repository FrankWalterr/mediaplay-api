import requests
import json
import sys
import os

BASE_URL = "https://mediaplay-api.onrender.com"
CONFIG_FILE = "api_config.json"

def load_config():
    """Carrega configurações."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def add_music_quick(media_uri, title, media_type="audio", mime_type=None, duration_ms=None):
    """Adiciona música rapidamente usando configurações salvas."""
    config = load_config()
    
    token = config.get('token')
    playlist_id = config.get('playlist_id')
    
    if not token or not playlist_id:
        print("ERRO: Execute primeiro 'python add_music_api.py' para configurar!")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buscar posição atual
    try:
        response = requests.get(
            f"{BASE_URL}/playlists/{playlist_id}/items",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            items = response.json()
            position = len(items)
        else:
            position = 0
    except:
        position = 0
    
    item_data = {
        "media_uri": media_uri,
        "media_type": media_type,
        "title": title,
        "position": position
    }
    
    if mime_type:
        item_data["mime_type"] = mime_type
    if duration_ms:
        item_data["duration_ms"] = duration_ms
    
    try:
        response = requests.post(
            f"{BASE_URL}/playlists/{playlist_id}/items",
            headers=headers,
            json=item_data,
            timeout=10
        )
        
        if response.status_code == 201:
            print(f"✓ Música '{title}' adicionada com sucesso!")
            return True
        else:
            print(f"ERRO: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python add_music_quick.py <URI> <Título> [tipo] [mime_type] [duration_ms]")
        print("Exemplo: python add_music_quick.py 'file:///musicas/musica.mp3' 'Minha Música'")
        sys.exit(1)
    
    media_uri = sys.argv[1]
    title = sys.argv[2]
    media_type = sys.argv[3] if len(sys.argv) > 3 else "audio"
    mime_type = sys.argv[4] if len(sys.argv) > 4 else None
    duration_ms = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] else None
    
    add_music_quick(media_uri, title, media_type, mime_type, duration_ms)

