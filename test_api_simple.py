"""Teste simples da API."""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=== Testando Mediaplay API ===\n")

# Health check
print("1. Health check...")
response = requests.get(f"{BASE_URL}/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}\n")

# Signup
print("2. Criando usuario...")
signup_data = {
    "email": "teste@mediaplay.com",
    "name": "Usuario Teste",
    "password": "senha123"
}
response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
print(f"   Status: {response.status_code}")
result = response.json()
print(f"   Token recebido: {result.get('access_token', 'N/A')[:50]}...\n")
token = result.get("access_token")

# Listar favoritos
print("3. Listando favoritos...")
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/favorites", headers=headers)
print(f"   Status: {response.status_code}")
print(f"   Favoritos: {len(response.json())} itens\n")

# Adicionar favorito
print("4. Adicionando favorito...")
favorite_data = {
    "media_uri": "file:///music/test.mp3",
    "media_type": "audio",
    "title": "Teste de Musica",
    "duration_ms": 180000
}
response = requests.post(f"{BASE_URL}/favorites", headers=headers, json=favorite_data)
print(f"   Status: {response.status_code}")
if response.status_code == 201:
    print(f"   Favorito criado com sucesso!\n")

# Listar favoritos novamente
print("5. Listando favoritos novamente...")
response = requests.get(f"{BASE_URL}/favorites", headers=headers)
print(f"   Status: {response.status_code}")
favorites = response.json()
print(f"   Total de favoritos: {len(favorites)}\n")
if favorites:
    print(f"   Primeiro favorito: {favorites[0]['title']}\n")

print("=== Testes concluidos! ===")


