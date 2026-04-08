# VIAGENS - Agente de Busca de Passagens

Agente especializado em buscar passagens aéreas e pacotes de viagem.

## Uso

```python
from viagens import buscar_passagens

resultado = await buscar_passagens(
    origem="Guarulhos",
    destino="Gramado", 
    data_ida="05/05/2026",
    data_volta="08/05/2026"
)
```

## Configuração

Requer:
- Playwright com stealth
- Proxy local (opcional, para bypass de WAF)
- Tunnel SSH (quando usando proxy)

## Arquivos

- `viagens.py` - Agente principal
- `azul_scraper.py` - Scraper específico para Azul Viagens
- `node-proxy.js` - Proxy local
- `tunnel.sh` - Tunnel SSH
