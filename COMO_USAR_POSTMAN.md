# Como Usar Postman para Ver Músicas na API

## Passo 1: Fazer Login

1. **Criar nova requisição:**
   - Método: `POST`
   - URL: `https://mediaplay-api.onrender.com/auth/signin`

2. **Configurar Body:**
   - Aba "Body"
   - Selecionar "raw"
   - Selecionar "JSON" no dropdown
   - Colar:
   ```json
   {
     "email": "seu@email.com",
     "password": "sua_senha"
   }
   ```

3. **Enviar:**
   - Clicar em "Send"
   - Copiar o `access_token` da resposta

## Passo 2: Ver Playlists e Músicas

1. **Na requisição GET /playlists:**
   - Aba "Authorization"
   - Type: `Bearer Token`
   - Token: Colar o `access_token` copiado
   - OU na aba "Headers":
     - Key: `Authorization`
     - Value: `Bearer {seu_token}`

2. **Enviar:**
   - Clicar em "Send"
   - Agora deve funcionar!

## Endpoints Disponíveis

### Autenticação
- `POST /auth/signup` - Criar conta
- `POST /auth/signin` - Fazer login

### Playlists
- `GET /playlists` - Listar todas as playlists (com músicas)
- `POST /playlists` - Criar playlist
- `GET /playlists/{id}` - Ver playlist específica
- `GET /playlists/{id}/items` - Ver músicas de uma playlist
- `POST /playlists/{id}/items` - Adicionar música
- `DELETE /playlists/{id}/items/{item_id}` - Remover música

### Favoritos
- `GET /favorites` - Listar favoritos
- `POST /favorites` - Adicionar favorito
- `DELETE /favorites?media_uri=...&media_type=...` - Remover favorito

## Dica: Usar Environment Variables

1. Criar Environment no Postman:
   - Nome: "Mediaplay API"
   - Variáveis:
     - `base_url`: `https://mediaplay-api.onrender.com`
     - `token`: (deixar vazio, será preenchido após login)

2. Usar nas URLs:
   - `{{base_url}}/auth/signin`
   - `{{base_url}}/playlists`

3. Salvar token automaticamente:
   - Na requisição de login, aba "Tests":
   ```javascript
   if (pm.response.code === 200) {
       var jsonData = pm.response.json();
       pm.environment.set("token", jsonData.access_token);
   }
   ```

4. Usar token nas outras requisições:
   - Authorization → Bearer Token → `{{token}}`

## Exemplo Completo

### 1. Login (POST)
```
POST https://mediaplay-api.onrender.com/auth/signin
Content-Type: application/json

{
  "email": "seu@email.com",
  "password": "sua_senha"
}
```

### 2. Listar Playlists (GET)
```
GET https://mediaplay-api.onrender.com/playlists
Authorization: Bearer {token_aqui}
```

### 3. Ver Músicas de uma Playlist (GET)
```
GET https://mediaplay-api.onrender.com/playlists/1/items
Authorization: Bearer {token_aqui}
```

