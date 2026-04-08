import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-http2']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        # Apply stealth
        stealth = Stealth()
        await stealth.apply_stealth_async(page)

        # Acessar Azul Viagens
        print("Acessando www.azulviagens.com.br...")
        await page.goto('https://www.azulviagens.com.br', wait_until='domcontentloaded', timeout=60000)
        await page.wait_for_timeout(5000)

        # Tirar screenshot da página inicial
        await page.screenshot(path='/root/.openclaw/workspace/antibot/azul_inicial.png')
        print("Screenshot da página inicial salvo")

        # Buscar campos de busca
        try:
            # Procurar campo de origem
            print("Procurando campos de busca...")
            
            # Tentar encontrar campo de origem (Guarulhos)
            origem_selectors = [
                'input[placeholder*="origem" i]',
                'input[placeholder*="Origem" i]',
                'input[name*="origem" i]',
                'input[name*="Origem" i]',
                '[data-testid*="origem"]',
                '[data-testid*="Origem"]'
            ]
            
            origem_field = None
            for selector in origem_selectors:
                try:
                    origem_field = await page.wait_for_selector(selector, timeout=3000)
                    if origem_field:
                        print(f"Campo origem encontrado: {selector}")
                        break
                except:
                    continue
            
            if origem_field:
                await origem_field.click()
                await page.wait_for_timeout(500)
                await origem_field.fill('Guarulhos')
                await page.wait_for_timeout(1000)
                # Tentar selecionar da lista
                await page.keyboard.press('Enter')
                await page.wait_for_timeout(1000)
            
            # Destino (Gramado)
            destino_selectors = [
                'input[placeholder*="destino" i]',
                'input[placeholder*="Destino" i]',
                'input[name*="destino" i]',
                'input[name*="Destino" i]'
            ]
            
            destino_field = None
            for selector in destino_selectors:
                try:
                    destino_field = await page.wait_for_selector(selector, timeout=3000)
                    if destino_field:
                        print(f"Campo destino encontrado: {selector}")
                        break
                except:
                    continue
            
            if destino_field:
                await destino_field.click()
                await page.wait_for_timeout(500)
                await destino_field.fill('Gramado')
                await page.wait_for_timeout(1000)
                await page.keyboard.press('Enter')
                await page.wait_for_timeout(1000)
            
            # Data de ida (05/05/2026)
            # Data de volta (08/05/2026)
            
            # Botão buscar
            buscar_selectors = [
                'button:has-text("Buscar")',
                'button:has-text("buscar")',
                '[type="submit"]',
                'button[type="submit"]'
            ]
            
            buscar_btn = None
            for selector in buscar_selectors:
                try:
                    buscar_btn = await page.wait_for_selector(selector, timeout=3000)
                    if buscar_btn:
                        print(f"Botão buscar encontrado: {selector}")
                        break
                except:
                    continue
            
            if buscar_btn:
                await buscar_btn.click()
                await page.wait_for_timeout(5000)
                
                # Aguardar resultados
                await page.wait_for_load_state('networkidle')
                await page.wait_for_timeout(3000)
                
                # Screenshot dos resultados
                await page.screenshot(path='/root/.openclaw/workspace/antibot/azul_resultados.png')
                print("Screenshot dos resultados salvo")
                
                # Tentar ir para segunda página
                next_selectors = [
                    'button:has-text("Próxima")',
                    'button:has-text("próxima")',
                    'a:has-text("2")',
                    '[data-testid*="next"]',
                    '.pagination button:nth-child(2)'
                ]
                
                next_btn = None
                for selector in next_selectors:
                    try:
                        next_btn = await page.wait_for_selector(selector, timeout=3000)
                        if next_btn:
                            print(f"Botão próxima página encontrado: {selector}")
                            break
                    except:
                        continue
                
                if next_btn:
                    await next_btn.click()
                    await page.wait_for_timeout(3000)
                    await page.wait_for_load_state('networkidle')
                    
                    # Screenshot da segunda página
                    await page.screenshot(path='/root/.openclaw/workspace/antibot/azul_pagina2.png')
                    print("Screenshot da página 2 salvo")
                    
                    # Extrair conteúdo da página
                    content = await page.content()
                    text = await page.inner_text('body')
                    
                    # Salvar conteúdo
                    with open('/root/.openclaw/workspace/antibot/pagina2_conteudo.txt', 'w', encoding='utf-8') as f:
                        f.write(text)
                    
                    print("\n=== CONTEÚDO DA SEGUNDA PÁGINA ===")
                    print(text[:3000])  # Primeiros 3000 caracteres
                    print("\n... (conteúdo completo salvo em pagina2_conteudo.txt)")
                else:
                    print("Botão de próxima página não encontrado")
                    # Salvar conteúdo da primeira página
                    text = await page.inner_text('body')
                    with open('/root/.openclaw/workspace/antibot/pagina1_conteudo.txt', 'w', encoding='utf-8') as f:
                        f.write(text)
                    print("\n=== CONTEÚDO DA PRIMEIRA PÁGINA ===")
                    print(text[:3000])
            else:
                print("Botão buscar não encontrado")
                
        except Exception as e:
            print(f"Erro durante a busca: {e}")
            await page.screenshot(path='/root/.openclaw/workspace/antibot/azul_erro.png')
            print("Screenshot do erro salvo")

        await browser.close()

asyncio.run(main())
