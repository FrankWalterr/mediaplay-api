# 🚀 Guia de Deploy - Mediaplay API

## 📋 Deploy no Render.com

### Passo 1: Preparar o Repositório

```bash
# Certifique-se de que todos os arquivos estão commitados
git add mediaplay-api/
git commit -m "Add Mediaplay API backend"
git push
```

### Passo 2: Criar Blueprint no Render

1. Acesse https://render.com
2. Clique em **"New +"** → **"Blueprint"**
3. Conecte seu repositório GitHub/GitLab
4. Render detectará o arquivo `render.yaml`

### Passo 3: Configurar Variáveis de Ambiente

No painel do Render, configure:

#### Para a Web Service:
- `DATABASE_URL`: Será preenchido automaticamente (referência ao PostgreSQL)
- `SECRET_KEY`: Clique em "Generate" para gerar uma chave segura
- `CORS_ORIGINS`: Lista de domínios permitidos
  ```json
  ["https://yourapp.com", "https://app.yourapp.com"]
  ```

#### Para o PostgreSQL:
- Nenhuma configuração adicional necessária
- Render cria automaticamente

### Passo 4: Deploy

O Render faz deploy automático!
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Passo 5: Verificar

Após o deploy, teste:
```bash
curl https://seu-app.onrender.com/health
```

---

## 🔧 Configuração Manual (Alternativa)

Se preferir criar os serviços manualmente:

### 1. Criar PostgreSQL

1. New + → PostgreSQL
2. Nome: `mediaplay-db`
3. Database: `mediaplay`
4. Copiar **Internal Database URL**

### 2. Criar Web Service

1. New + → Web Service
2. Repository: Seu repositório GitHub
3. Build Command: `pip install -r mediaplay-api/requirements.txt`
4. Start Command: `cd mediaplay-api && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Configurar Variáveis

- `DATABASE_URL`: Internal URL do PostgreSQL
- `SECRET_KEY`: Gerar com `openssl rand -hex 32`
- `CORS_ORIGINS`: JSON array de domínios

---

## 🧪 Testar API em Produção

```bash
# Health check
curl https://seu-app.onrender.com/health

# Signup
curl -X POST https://seu-app.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test","password":"secret123"}'

# Acessar documentação
# https://seu-app.onrender.com/docs
```

---

## 📝 Checklist de Deploy

- [ ] Código commitado e pushed
- [ ] Blueprint criado no Render
- [ ] PostgreSQL provisionado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy bem-sucedido
- [ ] Health check funcionando
- [ ] Documentação acessível em `/docs`
- [ ] Testes de autenticação passando
- [ ] CORS configurado corretamente

---

## 🔍 Troubleshooting

### Erro de banco de dados

**Problema**: `relation "users" does not exist`

**Solução**: O banco é criado automaticamente no startup. Verifique logs para erros.

### CORS bloqueando requisições

**Problema**: Requisições do app são bloqueadas

**Solução**: Configure `CORS_ORIGINS` com domínios exatos em produção.

### Token inválido

**Problema**: `Token inválido ou expirado`

**Solução**: Verifique `SECRET_KEY` e tempo de expiração do token.

---

## 📊 Monitoramento

O Render fornece:
- **Logs em tempo real**
- **Métricas de uso**
- **Alertas de erro**
- **Status de saúde**

Acesse o painel para monitorar sua API!

---

## 🔄 Deploy Contínuo

Cada push para a branch `main` aciona:
1. Build automático
2. Testes (se configurados)
3. Deploy para produção
4. Restart do serviço

---

## 💰 Custos

- **PostgreSQL Free**: 1 GB, 90 dias
- **Web Service Free**: 512 MB RAM, adormece após inatividade
- **Para produção**: Upgrade para planos pagos

---

## 🔐 Segurança em Produção

1. ✅ **SECRET_KEY**: Use chave forte aleatória
2. ✅ **CORS**: Liste domínios específicos
3. ✅ **HTTPS**: Automático no Render
4. ✅ **Backup**: Configure backups do PostgreSQL
5. ✅ **Monitoramento**: Configure alertas

---

## 📞 Suporte

- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Issues: Abra issue no GitHub do projeto


