import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

class ViagensAgent:
    """Agente para busca de passagens e pacotes de viagem."""
    
    def __init__(self, use_proxy=False, proxy_url='http://127.0.0.1:8888'):
        self.use_proxy = use_proxy
        self.proxy_url = proxy_url
        self.browser = None
        self.context = None
        self.page = None
    
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        
        launch_options = {
            'headless': True,
            'args': ['--disable-http2']
        }
        
        if self.use_proxy:
            launch_options['proxy'] = {'server': self.proxy_url}
        
        self.browser = await self.playwright.chromium.launch(**launch_options)
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        self.page = await self.context.new_page()
        
        # Apply stealth
        stealth = Stealth()
        await stealth.apply_stealth_async(self.page)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        await self.playwright.stop()
    
    async def buscar_azul(self, origem, destino, data_ida, data_volta):
        """Busca passagens na Azul Viagens."""
        print(f"Buscando: {origem} -> {destino}")
        print(f"Datas: {data_ida} - {data_volta}")
        
        await self.page.goto('https://www.azulviagens.com.br', 
                            wait_until='domcontentloaded', 
                            timeout=60000)
        await self.page.wait_for_timeout(5000)
        
        # Preencher origem
        origem_selectors = [
            'input[placeholder*="origem" i]',
            'input[placeholder*="Origem" i]',
            'input[name*="origem" i]',
            'input[name*="Origem" i]',
        ]
        
        for selector in origem_selectors:
            try:
                field = await self.page.wait_for_selector(selector, timeout=3000)
                if field:
                    await field.click()
                    await self.page.wait_for_timeout(500)
                    await field.fill(origem)
                    await self.page.wait_for_timeout(1000)
                    await self.page.keyboard.press('Enter')
                    await self.page.wait_for_timeout(1000)
                    break
            except:
                continue
        
        # Preencher destino
        destino_selectors = [
            'input[placeholder*="destino" i]',
            'input[placeholder*="Destino" i]',
            'input[name*="destino" i]',
            'input[name*="Destino" i]'
        ]
        
        for selector in destino_selectors:
            try:
                field = await self.page.wait_for_selector(selector, timeout=3000)
                if field:
                    await field.click()
                    await self.page.wait_for_timeout(500)
                    await field.fill(destino)
                    await self.page.wait_for_timeout(1000)
                    await self.page.keyboard.press('Enter')
                    await self.page.wait_for_timeout(1000)
                    break
            except:
                continue
        
        # Clicar em buscar
        buscar_selectors = [
            'button:has-text("Buscar")',
            'button[type="submit"]'
        ]
        
        for selector in buscar_selectors:
            try:
                btn = await self.page.wait_for_selector(selector, timeout=3000)
                if btn:
                    await btn.click()
                    await self.page.wait_for_timeout(5000)
                    await self.page.wait_for_load_state('networkidle')
                    break
            except:
                continue
        
        # Retornar conteúdo da página
        return await self.page.inner_text('body')
    
    async def proxima_pagina(self):
        """Navega para a próxima página de resultados."""
        next_selectors = [
            'button:has-text("Próxima")',
            'a:has-text("2")',
            '[data-testid*="next"]'
        ]
        
        for selector in next_selectors:
            try:
                btn = await self.page.wait_for_selector(selector, timeout=3000)
                if btn:
                    await btn.click()
                    await self.page.wait_for_timeout(3000)
                    await self.page.wait_for_load_state('networkidle')
                    return await self.page.inner_text('body')
            except:
                continue
        
        return None
    
    async def screenshot(self, path):
        """Tira screenshot da página atual."""
        await self.page.screenshot(path=path)


async def buscar_passagens(origem, destino, data_ida, data_volta, use_proxy=False):
    """Função helper para buscar passagens."""
    async with ViagensAgent(use_proxy=use_proxy) as agent:
        resultado = await agent.buscar_azul(origem, destino, data_ida, data_volta)
        return resultado


if __name__ == '__main__':
    # Exemplo de uso
    resultado = asyncio.run(buscar_passagens(
        origem="Guarulhos",
        destino="Gramado",
        data_ida="05/05/2026",
        data_volta="08/05/2026",
        use_proxy=False
    ))
    print(resultado[:2000])
