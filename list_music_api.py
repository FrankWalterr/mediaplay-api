"""Script para listar todas as músicas das playlists via API."""
import requests
import json
import sys
import os

# URL da API no Render
BASE_URL = "https://mediaplay-api.onrender.com"

# Arquivo de configuração
CONFIG_FILE = "api_config.json"

def load_config():
    """Carrega configurações salvas."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def list_all_music():
    """Lista todas as músicas de todas as playlists."""
    config = load_config()
    
    token = config.get('token')
    if not token:
        print("ERRO: Execute primeiro 'python add_music_api.py' para fazer login!")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n" + "="*60)
    print("LISTANDO TODAS AS MÚSICAS DA API")
    print("="*60)
    
    try:
        # Buscar todas as playlists
        response = requests.get(f"{BASE_URL}/playlists", headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"ERRO: {response.status_code} - {response.text}")
            return
        
        playlists = response.json()
        print(f"\nTotal de playlists: {len(playlists)}\n")
        
        if not playlists:
            print("Nenhuma playlist encontrada.")
            return
        
        total_music = 0
        
        # Para cada playlist
        for playlist in playlists:
            playlist_id = playlist.get('id')
            playlist_name = playlist.get('name')
            items = playlist.get('items', [])
            
            print("-" * 60)
            print(f"PLAYLIST: {playlist_name} (ID: {playlist_id})")
            print(f"Músicas: {len(items)}")
            print("-" * 60)
            
            if items:
                for i, item in enumerate(items, 1):
                    print(f"\n  {i}. {item.get('title')}")
                    print(f"     Tipo: {item.get('media_type')}")
                    print(f"     URI: {item.get('media_uri')}")
                    print(f"     Posição: {item.get('position')}")
                    if item.get('duration_ms'):
                        duration_sec = item.get('duration_ms') // 1000
                        duration_min = duration_sec // 60
                        duration_sec = duration_sec % 60
                        print(f"     Duração: {duration_min}:{duration_sec:02d}")
                    if item.get('mime_type'):
                        print(f"     MIME: {item.get('mime_type')}")
                    total_music += 1
            else:
                print("  (Nenhuma música nesta playlist)")
            print()
        
        print("="*60)
        print(f"TOTAL DE MÚSICAS: {total_music}")
        print("="*60)
        
    except requests.exceptions.RequestException as e:
        print(f"ERRO de conexão: {e}")
        print("Verifique se a API está online no Render")
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_all_music()

