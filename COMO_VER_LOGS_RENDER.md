# 📋 Como Ver Logs no Render

## 🔍 Onde os Logs Aparecem

Os logs da API aparecem **apenas quando a API está rodando no Render** (produção), não localmente.

### Passos para Ver Logs no Render:

1. **Acesse o Painel do Render**
   - Vá para https://render.com
   - Faça login na sua conta

2. **Navegue até seu Serviço**
   - Clique no serviço `mediaplay-api` na lista de serviços

3. **Acesse a Aba "Logs"**
   - No menu lateral, clique em **"Logs"**
   - Ou use o atalho: `https://dashboard.render.com/web/[seu-servico-id]/logs`

4. **Visualize os Logs em Tempo Real**
   - Os logs aparecem automaticamente
   - Você verá:
     - ✅ Logs de startup da API
     - ✅ Todas as requisições HTTP (método, path, status)
     - ✅ Erros e exceções
     - ✅ Logs do banco de dados (se SQL_ECHO=true)

## 📝 O Que Aparece nos Logs

Com a configuração atual, você verá:

### Durante o Startup:
```
INFO - Mediaplay API iniciando...
INFO - Banco de dados inicializado com sucesso!
INFO - API pronta para receber requisicoes!
```

### Para Cada Requisição:
```
INFO - REQUEST: GET /health
INFO - Health check realizado
INFO - RESPONSE: GET /health - Status: 200
```

### Em Caso de Erro:
```
ERROR - Erro ao inicializar banco de dados: [detalhes]
```

## 🔧 Configuração Atual

A API está configurada para:

1. **Logging configurado** em `app/main.py`:
   - Nível: `INFO`
   - Formato: timestamp, nome, nível, mensagem
   - Logs de todas as requisições via middleware

2. **Uvicorn configurado** em `render.yaml`:
   - `--log-level info` para mostrar logs detalhados
   - Porta dinâmica via `$PORT`

## 🚀 Para Fazer Deploy e Ver Logs

### 1. Commit e Push das Alterações

```bash
cd mediaplay-api
git add .
git commit -m "Adiciona logging para Render"
git push
```

### 2. Render Faz Deploy Automático

- O Render detecta o push
- Faz build automático
- Inicia a API com logging ativado

### 3. Acesse os Logs

- Vá para o painel do Render
- Clique em "Logs" no seu serviço
- Veja os logs em tempo real!

## 🧪 Testar e Gerar Logs

Após o deploy, faça requisições para gerar logs:

```bash
# Health check
curl https://seu-app.onrender.com/health

# Documentação
curl https://seu-app.onrender.com/docs

# Criar usuário
curl -X POST https://seu-app.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test","password":"secret123"}'
```

Cada requisição aparecerá nos logs do Render!

## 📊 Logs Locais vs Render

| Local (Desenvolvimento) | Render (Produção) |
|------------------------|-------------------|
| Logs no terminal | Logs no painel Render |
| `python run_with_logs.py` | Deploy automático |
| Porta 8000 | Porta dinâmica ($PORT) |
| SQLite local | PostgreSQL do Render |

## ⚠️ Importante

- **Logs locais** aparecem no terminal onde você executa a API
- **Logs no Render** aparecem apenas quando a API está em produção no Render
- Após fazer deploy, aguarde alguns minutos para o serviço iniciar
- Os logs podem ter um pequeno delay (alguns segundos)

## 🔍 Troubleshooting

### Não vejo logs no Render

1. Verifique se o serviço está rodando (status "Live")
2. Verifique se o deploy foi bem-sucedido
3. Aguarde alguns minutos após o deploy
4. Faça uma requisição para gerar logs

### Logs não mostram detalhes

1. Verifique se `--log-level info` está no `render.yaml`
2. Confirme que o logging está configurado em `app/main.py`
3. Verifique se há erros no build do Render

### Logs muito verbosos

Se quiser reduzir os logs, altere o nível para `WARNING`:
```yaml
startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level warning"
```

---

**Última atualização**: Configurado para logging completo no Render! 🎉


