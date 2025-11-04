"""Teste simples da API."""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def wait_for_api(max_attempts=10):
    """Aguarda a API estar disponível."""
    print("Aguardando API iniciar...")
    for i in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print("API esta respondendo!\n")
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    print("ERRO: API nao esta respondendo. Certifique-se de que esta rodando.")
    return False

print("=== Testando Mediaplay API ===\n")

# Aguardar API iniciar
if not wait_for_api():
    sys.exit(1)

# Health check
print("1. Health check...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
except Exception as e:
    print(f"   ERRO: {e}\n")
    sys.exit(1)

# Signup
print("2. Criando usuario...")
signup_data = {
    "email": f"teste{int(time.time())}@mediaplay.com",  # Email único
    "name": "Usuario Teste",
    "password": "senha123"
}
token = None
try:
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data, timeout=5)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        token = result.get("access_token")
        print(f"   Token recebido: {token[:50] if token else 'N/A'}...\n")
    elif response.status_code == 400:
        print(f"   Usuario ja existe, tentando login...")
        # Tentar fazer login
        signin_data = {
            "email": signup_data["email"],
            "password": signup_data["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/signin", json=signin_data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print(f"   Login OK! Token recebido: {token[:50] if token else 'N/A'}...\n")
        else:
            print(f"   ERRO no login: {response.status_code}\n")
            sys.exit(1)
    else:
        print(f"   ERRO: {response.status_code} - {response.text}\n")
        sys.exit(1)
except Exception as e:
    print(f"   ERRO: {e}\n")
    sys.exit(1)

if not token:
    print("ERRO: Nao foi possivel obter token de autenticacao")
    sys.exit(1)

# Listar favoritos
print("3. Listando favoritos...")
headers = {"Authorization": f"Bearer {token}"}
try:
    response = requests.get(f"{BASE_URL}/favorites", headers=headers, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        favorites = response.json()
        print(f"   Favoritos: {len(favorites)} itens\n")
    else:
        print(f"   ERRO: {response.status_code} - {response.text}\n")
except Exception as e:
    print(f"   ERRO: {e}\n")

# Adicionar favorito
print("4. Adicionando favorito...")
favorite_data = {
    "media_uri": "file:///music/test.mp3",
    "media_type": "audio",
    "title": "Teste de Musica",
    "duration_ms": 180000
}
try:
    response = requests.post(f"{BASE_URL}/favorites", headers=headers, json=favorite_data, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"   Favorito criado/atualizado com sucesso!\n")
    else:
        print(f"   ERRO: {response.status_code} - {response.text}\n")
except Exception as e:
    print(f"   ERRO: {e}\n")

# Listar favoritos novamente
print("5. Listando favoritos novamente...")
try:
    response = requests.get(f"{BASE_URL}/favorites", headers=headers, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        favorites = response.json()
        print(f"   Total de favoritos: {len(favorites)}\n")
        if favorites:
            print(f"   Primeiro favorito: {favorites[0].get('title', 'N/A')}\n")
    else:
        print(f"   ERRO: {response.status_code} - {response.text}\n")
except Exception as e:
    print(f"   ERRO: {e}\n")

print("=== Testes concluidos! ===")


