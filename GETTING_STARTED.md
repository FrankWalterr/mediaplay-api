# 🚀 Guia de Início Rápido - Mediaplay API

## ⚡ Execução Rápida

### 1. Instalar Dependências

```bash
cd mediaplay-api
pip install -r requirements.txt
```

### 2. Executar a API

```bash
python run.py
```

A API estará disponível em: **http://localhost:8000**

### 3. Acessar Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testar a API

### Health Check

```bash
curl http://localhost:8000/health
```

Resposta esperada:
```json
{"status":"ok","version":"1.0.0"}
```

### Criar Usuário (Signup)

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User","password":"secret123"}'
```

Resposta:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Login (Signin)

```bash
curl -X POST "http://localhost:8000/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"secret123"}'
```

### Listar Favoritos

```bash
curl -X GET "http://localhost:8000/favorites" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Adicionar Favorito

```bash
curl -X POST "http://localhost:8000/favorites" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "media_uri": "file:///music/song.mp3",
    "media_type": "audio",
    "title": "Minha Música",
    "duration_ms": 240000
  }'
```

## 📋 Estrutura Completa

```
mediaplay-api/
├─ app/
│  ├─ __init__.py              # Módulo principal
│  ├─ __main__.py              # Entry point
│  ├─ config.py                # Configurações
│  ├─ main.py                  # App FastAPI
│  ├─ db.py                    # Database setup
│  ├─ security.py              # JWT e bcrypt
│  ├─ models.py                # Modelos SQLAlchemy
│  ├─ schemas.py               # Schemas Pydantic
│  ├─ crud.py                  # Operações CRUD
│  ├─ deps.py                  # Dependências (auth)
│  └─ routers/
│     ├─ __init__.py
│     ├─ auth.py               # POST /auth/signup, /auth/signin
│     ├─ favorites.py          # GET/POST/DELETE /favorites
│     ├─ history.py            # GET/POST /history
│     ├─ playlists.py          # CRUD /playlists + items
│     ├─ tags.py               # CRUD /tags + media links
│     ├─ settings.py           # GET/POST /settings
│     └─ statistics.py         # GET/POST /statistics
├─ requirements.txt            # Dependências Python
├─ render.yaml                 # Config deploy Render
├─ run.py                      # Script de execução
├─ .env.example                # Exemplo de configuração
└─ README.md                   # Documentação completa
```

## 🗄️ Banco de Dados

### SQLite (Desenvolvimento)

Banco criado automaticamente: `mediaplay.db`

### PostgreSQL (Produção)

Configure a variável de ambiente:

```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

## 🔐 Segurança

- **Senhas**: Hash com bcrypt
- **JWT**: Tokens Bearer com expiração (30 min default)
- **Multi-tenant**: Dados isolados por usuário
- **CORS**: Configurável por domínio

## 🌐 Deploy no Render

1. Push para GitHub
2. Conecte no Render.com
3. Render detecta `render.yaml` automaticamente
4. Configure `DATABASE_URL` no painel
5. Deploy automático! 🎉

## 📝 Próximos Passos

1. ✅ Testar todos os endpoints em `/docs`
2. ✅ Integrar com app mobile
3. ✅ Configurar CORS para domínios reais
4. ✅ Deploy em produção

## 🆘 Suporte

Em caso de problemas:
- Verifique logs do servidor
- Confira variáveis de ambiente
- Consulte `/docs` para detalhes dos endpoints


