# Antibot Proxy + VIAGENS

Sistema de proxy local com agente de busca de passagens.

## Estrutura

```
antibot/
├── README.md           # Este arquivo
├── VIAGENS.md          # Documentação do agente
├── viagens.py          # Agente VIAGENS
├── azul_scraper.py     # Scraper legado (Azul)
├── node-proxy.js       # Proxy HTTP local
├── tunnel.sh           # Tunnel SSH
├── venv/               # Python virtual environment
└── package.json        # Node dependencies
```

## Componentes

### 1. Proxy Local (node-proxy.js)
Proxy HTTP na porta 8888 que remove headers de proxy e força HTTP/1.1.

### 2. Tunnel SSH (tunnel.sh)
Conecta cliente local à VPS para rotear tráfego.

### 3. Agente VIAGENS (viagens.py)
Agente Playwright com stealth para busca de passagens.

## Uso Básico

```python
from viagens import buscar_passagens

# Sem proxy
resultado = await buscar_passagens(
    origem="Guarulhos",
    destino="Gramado",
    data_ida="05/05/2026",
    data_volta="08/05/2026"
)

# Com proxy (requer tunnel)
resultado = await buscar_passagens(
    origem="Guarulhos",
    destino="Gramado", 
    data_ida="05/05/2026",
    data_volta="08/05/2026",
    use_proxy=True
)
```

## Fluxo Completo com Proxy

1. **Cliente**: `./tunnel.sh start`
2. **VPS Terminal 1**: `node node-proxy.js`
3. **VPS Terminal 2**: `python viagens.py`

## Instalação

```bash
# Node.js dependencies
npm install

# Python dependencies
source venv/bin/activate
pip install playwright playwright-stealth
playwright install chromium
```
