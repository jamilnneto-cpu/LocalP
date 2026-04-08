# Configuração do Agente VIAGENS

## Data de criação
2026-04-08

## Repositório GitHub
https://github.com/jamilnneto-cpu/LocalP

## Estrutura do Projeto

```
antibot/
├── .github/workflows/viagens.yml   # Workflow GitHub Actions
├── .gitignore                       # Ignora venv e cache
├── README.md                        # Documentação geral
├── VIAGENS.md                       # Doc do agente
├── GITHUB_ACTIONS.md                # Doc GitHub Actions
├── viagens.py                       # Agente VIAGENS (classe Python)
├── azul_scraper.py                  # Scraper legado para Azul
├── node-proxy.js                    # Proxy HTTP local (porta 8888)
├── tunnel.sh                        # Tunnel SSH (configurado)
├── package.json                     # Dependências Node
└── venv/                            # Python virtualenv (não commitado)
```

## Agente VIAGENS (viagens.py)

### Classe ViagensAgent
- Inicialização com proxy opcional
- Métodos: `buscar_azul()`, `proxima_pagina()`, `screenshot()`
- Stealth aplicado automaticamente

### Uso
```python
from viagens import buscar_passagens

resultado = await buscar_passagens(
    origem="Guarulhos",
    destino="Gramado",
    data_ida="05/05/2026",
    data_volta="08/05/2026",
    use_proxy=False  # ou True com tunnel
)
```

## Configuração do Tunnel

Arquivo: `tunnel.sh`
- VPS_USER="root"
- VPS_IP="191.101.70.190"
- LOCAL_PORT=8888
- REMOTE_PORT=8888

## GitHub Actions

Workflow: `.github/workflows/viagens.yml`
- Disparo manual (workflow_dispatch)
- Inputs: origem, destino, data_ida, data_volta, pagina
- Roda em ubuntu-latest
- Instala Playwright + stealth
- Upload de screenshots e resultado

## Dependências

### Node.js
- http-proxy

### Python
- playwright
- playwright-stealth

## Limitações Conhecidas

1. Site www.azulviagens.com.br bloqueia conexões da VPS (timeout)
2. Solução: usar GitHub Actions (IP diferente) ou tunnel SSH
3. Não resolve CAPTCHA automaticamente

## Tokens GitHub

Tokens utilizados durante a configuração (revogados após uso).

## Próximos Passos

1. Executar workflow no GitHub Actions
2. Verificar se o site ainda bloqueia (IP do GitHub)
3. Ajustar seletores se necessário
4. Adicionar mais sites (Latam, Gol, etc)
