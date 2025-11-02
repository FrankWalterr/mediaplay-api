# 🎵 Mediaplay API

Servidor mestre backend para sincronização de dados do app Mediaplay offline-first.

## 🚀 Características

- **FastAPI** - Framework moderno e rápido
- **PostgreSQL** - Banco de dados robusto em produção
- **SQLite** - Banco local para desenvolvimento
- **JWT Authentication** - Autenticação segura com tokens Bearer
- **Multi-tenant** - Todos os dados isolados por usuário
- **Upsert Operations** - Sincronização inteligente "most recent wins"
- **CORS Configurado** - Acesso controlado por domínio
- **Auto Docs** - Documentação automática em `/docs` (Swagger)

## 📋 Requisitos

- Python 3.11+
- PostgreSQL (para produção) ou SQLite (para desenvolvimento)

## 🔧 Instalação

### 1. Clone o repositório

```bash
cd mediaplay-api
```

### 2. Crie ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale dependências

```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env com suas configurações
```

### 5. Inicialize o banco de dados

```bash
python -c "from app.db import init_db; init_db()"
```

### 6. Execute a API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: **http://localhost:8000**

Documentação interativa: **http://localhost:8000/docs**

## 📁 Estrutura do Projeto

```
mediaplay-api/
├─ app/
│  ├─ __init__.py
│  ├─ config.py          # Configurações da aplicação
│  ├─ main.py            # App FastAPI principal
│  ├─ db.py              # Configuração do banco de dados
│  ├─ security.py        # JWT e hash de senhas
│  ├─ models.py          # Modelos SQLAlchemy
│  ├─ schemas.py         # Schemas Pydantic
│  ├─ crud.py            # Operações CRUD
│  ├─ deps.py            # Dependências (auth, etc)
│  └─ routers/
│     ├─ auth.py         # Autenticação
│     ├─ favorites.py    # Favoritos
│     ├─ history.py      # Histórico
│     ├─ playlists.py    # Playlists
│     ├─ tags.py         # Tags
│     ├─ settings.py     # Configurações
│     └─ statistics.py   # Estatísticas
├─ requirements.txt
├─ render.yaml           # Deploy no Render
├─ .env.example
└─ README.md
```

## 🔐 Autenticação

Todas as rotas (exceto `/health` e `/auth/*`) exigem autenticação:

```bash
Authorization: Bearer <token>
```

### Obter Token

```bash
# Signup
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"User","password":"secret"}'

# Signin
curl -X POST "http://localhost:8000/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret"}'
```

## 📡 Endpoints Principais

### Health Check
- `GET /health` - Verifica se a API está online

### Autenticação
- `POST /auth/signup` - Registra novo usuário
- `POST /auth/signin` - Autentica usuário

### Favoritos
- `GET /favorites` - Lista favoritos
- `POST /favorites` - Upsert favorito
- `DELETE /favorites?media_uri=...&media_type=...` - Deleta favorito

### Histórico
- `GET /history` - Lista histórico
- `POST /history` - Upsert histórico

### Playlists
- `GET /playlists` - Lista playlists
- `POST /playlists` - Cria playlist
- `GET /playlists/{id}` - Obtém playlist
- `PUT /playlists/{id}` - Atualiza playlist
- `DELETE /playlists/{id}` - Deleta playlist

### Itens de Playlist
- `GET /playlists/{id}/items` - Lista itens
- `POST /playlists/{id}/items` - Upsert item
- `DELETE /playlists/{id}/items/{item_id}` - Deleta item

### Tags
- `GET /tags` - Lista tags
- `POST /tags` - Cria tag
- `DELETE /tags/{id}` - Deleta tag

### Vínculos Tag-Mídia
- `POST /tags/media` - Vincula tag a mídia
- `DELETE /tags/media/{id}` - Remove vínculo

### Configurações
- `GET /settings` - Obtém configurações
- `POST /settings` - Upsert configurações

### Estatísticas
- `GET /statistics` - Obtém estatísticas
- `POST /statistics` - Upsert estatísticas

## 🌐 Deploy no Render

### 1. Push para GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <seu-repo>
git push -u origin main
```

### 2. Conecte no Render

1. Acesse https://render.com
2. Clique em "New +"
3. Selecione "Blueprint"
4. Conecte seu repositório GitHub
5. Render detecta o `render.yaml` automaticamente

### 3. Configure Variáveis

No painel do Render, configure:

- `DATABASE_URL` - URL da instância PostgreSQL
- `SECRET_KEY` - Chave secreta (gerada automaticamente)
- `CORS_ORIGINS` - Domínios permitidos (JSON array)

### 4. Deploy

O Render faz deploy automático a cada push!

## 🔄 Sincronização Offline-First

O app mobile envia **upserts** para o servidor:

```json
POST /favorites
{
  "media_uri": "file:///path/to/media",
  "media_type": "audio",
  "title": "Minha Música",
  "duration_ms": 240000
}
```

O servidor:
1. Verifica se existe (por `media_uri + media_type`)
2. Se existe: **atualiza** com novos dados
3. Se não existe: **cria** novo registro

Isso implementa política **"most recent wins"** baseada em `updated_at`.

## 📊 Banco de Dados

### Modelos Principais

- **User** - Usuários do sistema
- **Favorite** - Mídias favoritas
- **HistoryItem** - Histórico de reprodução
- **Playlist** - Playlists do usuário
- **PlaylistItem** - Itens das playlists
- **Tag** - Tags personalizadas
- **MediaTag** - Vínculos tag-mídia
- **Setting** - Configurações do usuário
- **Statistics** - Estatísticas de uso

Todos os modelos têm:
- `created_at` - Timestamp de criação
- `updated_at` - Timestamp de atualização

## 🛡️ Segurança

- **Senhas**: Hash SHA256 com salt
- **JWT**: Tokens Bearer com expiração
- **Multi-tenant**: Isolamento completo por usuário
- **CORS**: Controle de origens permitidas
- **SQL Injection**: Prevenido por SQLAlchemy

## 📚 Documentação

A documentação interativa está disponível em:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio

# Executar testes
pytest
```

## 📄 Licença

MIT

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato

Mediaplay Team

