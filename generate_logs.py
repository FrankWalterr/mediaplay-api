"""Script para gerar requisições de teste e criar logs na API."""
import requests
import time
import json
import sys

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Gerando requisicoes de teste para criar logs na API")
print("=" * 60)
print()

# Aguardar API iniciar
print("Aguardando API iniciar...")
for i in range(10):
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("API esta respondendo!\n")
            break
    except requests.exceptions.RequestException:
        time.sleep(1)
        if i == 9:
            print("ERRO: API nao esta respondendo. Certifique-se de que esta rodando.")
            sys.exit(1)

# Lista de testes
tests = [
    ("GET", "/health", None, "Health check"),
    ("GET", "/", None, "Root endpoint"),
    ("GET", "/docs", None, "Documentação Swagger"),
    ("POST", "/auth/signup", {
        "email": f"teste{int(time.time())}@mediaplay.com",
        "name": "Usuario Teste Logs",
        "password": "senha123"
    }, "Criar usuário"),
]

token = None

for method, endpoint, data, description in tests:
    print(f">> {description} ({method} {endpoint})...")
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        elif method == "POST":
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
        
        print(f"   Status: {response.status_code}")
        
        if endpoint == "/auth/signup" and response.status_code in [200, 201]:
            result = response.json()
            token = result.get("access_token")
            if token:
                print(f"   OK: Token recebido (primeiros 30 chars): {token[:30]}...")
        
        if endpoint == "/docs":
            print(f"   OK: Documentacao carregada ({len(response.text)} bytes)")
        else:
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
            except:
                print(f"   Response: {response.text[:100]}...")
        
    except Exception as e:
        print(f"   ERRO: {e}")
    
    print()
    time.sleep(0.5)

# Se tiver token, fazer mais testes autenticados
if token:
    print("Testando endpoints autenticados...")
    headers = {"Authorization": f"Bearer {token}"}
    
    auth_tests = [
        ("GET", "/favorites", "Listar favoritos"),
        ("GET", "/history", "Listar histórico"),
        ("GET", "/playlists", "Listar playlists"),
    ]
    
    for method, endpoint, description in auth_tests:
        print(f">> {description} ({method} {endpoint})...")
        try:
            response = requests.get(
                f"{BASE_URL}{endpoint}",
                headers=headers,
                timeout=5
            )
            print(f"   Status: {response.status_code}")
            result = response.json()
            print(f"   OK: {len(result) if isinstance(result, list) else 1} item(s) retornado(s)")
        except Exception as e:
            print(f"   ERRO: {e}")
        print()
        time.sleep(0.5)

print("=" * 60)
print("OK: Requisicoes concluidas! Verifique os logs do servidor.")
print("=" * 60)

