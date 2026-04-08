# VIAGENS no GitHub Actions

Roda o agente VIAGENS no GitHub Actions (IP diferente a cada execução).

## Como usar

### 1. Criar repositório no GitHub

```bash
cd /root/.openclaw/workspace/antibot
git init
git add .
git commit -m "Agente VIAGENS v1.0"
```

### 2. Push para GitHub

Crie um repositório privado no GitHub e:

```bash
git remote add origin https://github.com/SEU_USER/viagens-agent.git
git push -u origin main
```

### 3. Executar workflow

1. Vá em **Actions** no GitHub
2. Selecione **VIAGENS - Busca de Passagens**
3. Clique em **Run workflow**
4. Preencha os campos:
   - Origem: Guarulhos
   - Destino: Gramado
   - Data ida: 05/05/2026
   - Data volta: 08/05/2026
   - Página: 2

### 4. Resultados

- Screenshots das páginas (artifacts)
- Texto extraído da página solicitada
- Logs da execução

## Vantagens

- IP diferente a cada run (GitHub Actions)
- Não depende do seu dispositivo
- Gratuito (limitado a 2000 minutos/mês)
- Screenshots salvos automaticamente
