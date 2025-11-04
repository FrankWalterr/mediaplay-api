"""Script para adicionar música à playlist via API - Tudo configurado automaticamente."""
import requests
import json
import sys
import os
from datetime import datetime

# URL da API no Render
BASE_URL = "https://mediaplay-api.onrender.com"

# Arquivo para salvar credenciais e configurações
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

def save_config(config):
    """Salva configurações."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def ensure_login():
    """Garante que temos um usuário logado."""
    config = load_config()
    
    # Se já temos token válido, testar
    if config.get('token'):
        headers = {"Authorization": f"Bearer {config['token']}"}
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            # Testar token fazendo uma requisição autenticada
            response = requests.get(f"{BASE_URL}/playlists", headers=headers, timeout=5)
            if response.status_code == 200:
                print("✓ Token válido encontrado!")
                return config['token'], config.get('email'), config.get('playlist_id')
        except:
            pass
    
    # Precisa fazer login ou criar conta
    print("\n" + "="*60)
    print("CONFIGURAÇÃO INICIAL - LOGIN/CADASTRO")
    print("="*60)
    
    email = input("\nDigite seu email: ").strip()
    password = input("Digite sua senha: ").strip()
    
    token = None
    
    # Tentar login primeiro
    print(f"\nTentando fazer login...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signin",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print(f"✓ Login realizado com sucesso!")
        else:
            print(f"Login falhou. Criando nova conta...")
            # Criar conta
            name = input("Digite seu nome: ").strip()
            response = requests.post(
                f"{BASE_URL}/auth/signup",
                json={"email": email, "name": name, "password": password},
                timeout=10
            )
            if response.status_code == 201:
                result = response.json()
                token = result.get("access_token")
                print(f"✓ Conta criada e login realizado!")
            else:
                print(f"ERRO: {response.status_code} - {response.text}")
                sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"ERRO de conexão: {e}")
        print("Verifique se a API está online no Render")
        sys.exit(1)
    
    if not token:
        print("ERRO: Não foi possível obter token")
        sys.exit(1)
    
    # Salvar token
    config['token'] = token
    config['email'] = email
    save_config(config)
    
    # Verificar/criar playlist
    playlist_id = ensure_playlist(token)
    
    # Salvar playlist_id
    config['playlist_id'] = playlist_id
    save_config(config)
    
    return token, email, playlist_id

def ensure_playlist(token):
    """Garante que temos uma playlist disponível."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Listar playlists
    try:
        response = requests.get(f"{BASE_URL}/playlists", headers=headers, timeout=10)
        if response.status_code == 200:
            playlists = response.json()
            
            if playlists:
                # Usar primeira playlist
                playlist_id = playlists[0].get('id')
                playlist_name = playlists[0].get('name')
                print(f"\n✓ Usando playlist existente: '{playlist_name}' (ID: {playlist_id})")
                return playlist_id
            
            # Criar nova playlist
            print("\nNenhuma playlist encontrada. Criando nova...")
            playlist_name = f"Playlist {datetime.now().strftime('%Y-%m-%d')}"
            response = requests.post(
                f"{BASE_URL}/playlists",
                headers=headers,
                json={"name": playlist_name, "description": "Playlist criada automaticamente"},
                timeout=10
            )
            if response.status_code == 201:
                playlist = response.json()
                playlist_id = playlist.get('id')
                print(f"✓ Playlist criada: '{playlist_name}' (ID: {playlist_id})")
                return playlist_id
    except requests.exceptions.RequestException as e:
        print(f"ERRO: {e}")
    
    return None

def add_music(token, playlist_id, media_uri, title, media_type="audio", mime_type=None, duration_ms=None, position=None):
    """Adiciona música à playlist."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Se position não especificado, buscar último
    if position is None:
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
            result = response.json()
            print(f"✓ Música adicionada com sucesso!")
            print(f"  Título: {result.get('title')}")
            print(f"  Tipo: {result.get('media_type')}")
            print(f"  Posição: {result.get('position')}")
            return result
        else:
            print(f"ERRO: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"ERRO de conexão: {e}")
        return None

def list_playlist_items(token, playlist_id):
    """Lista itens da playlist."""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/playlists/{playlist_id}/items",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            items = response.json()
            return items
    except:
        pass
    return []

def main():
    print("\n" + "="*60)
    print("ADICIONAR MÚSICA À PLAYLIST VIA API")
    print("="*60)
    
    # Garantir login e playlist
    token, email, playlist_id = ensure_login()
    
    print("\n" + "="*60)
    print("TUDO PRONTO!")
    print("="*60)
    print(f"Email: {email}")
    print(f"Playlist ID: {playlist_id}")
    print(f"API: {BASE_URL}")
    print("\nAgora você pode adicionar músicas facilmente!")
    
    while True:
        print("\n" + "-"*60)
        print("OPÇÕES:")
        print("1. Adicionar música")
        print("2. Ver músicas da playlist")
        print("3. Sair")
        print("-"*60)
        
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            print("\n--- ADICIONAR MÚSICA ---")
            media_uri = input("URI da música (ex: file:///musicas/musica.mp3): ").strip()
            if not media_uri:
                print("URI é obrigatória!")
                continue
            
            title = input("Título da música: ").strip()
            if not title:
                title = "Música sem título"
            
            media_type = input("Tipo (audio/video) [audio]: ").strip().lower() or "audio"
            mime_type = input("MIME type (ex: audio/mpeg) [opcional]: ").strip() or None
            duration_input = input("Duração em milissegundos [opcional]: ").strip()
            duration_ms = int(duration_input) if duration_input else None
            
            add_music(token, playlist_id, media_uri, title, media_type, mime_type, duration_ms)
            
        elif opcao == "2":
            print("\n--- MÚSICAS DA PLAYLIST ---")
            items = list_playlist_items(token, playlist_id)
            if items:
                print(f"\nTotal de músicas: {len(items)}\n")
                for i, item in enumerate(items, 1):
                    print(f"{i}. {item.get('title')}")
                    print(f"   Tipo: {item.get('media_type')}")
                    print(f"   URI: {item.get('media_uri')}")
                    print(f"   Posição: {item.get('position')}")
                    if item.get('duration_ms'):
                        duration_sec = item.get('duration_ms') // 1000
                        print(f"   Duração: {duration_sec}s")
                    print()
            else:
                print("Nenhuma música na playlist ainda.")
                
        elif opcao == "3":
            print("\nAté logo!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
        import traceback
        traceback.print_exc()

