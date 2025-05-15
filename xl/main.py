import os
import asyncio
from pathlib import Path
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from browser_use import Agent, Browser, BrowserConfig

load_dotenv()

def get_chrome_path() -> str:
    return "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

def read_pdf_content(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f'PDF file not found at {pdf_path}')
    
    pdf = PdfReader(pdf_path)
    text = ''
    for page in pdf.pages:
        text += page.extract_text() or ''
    return text

async def main():
    pdf_path = 'file.pdf'  # Cambia a la ruta real del PDF
    pdf_content = read_pdf_content(pdf_path)
    
    browser = Browser(
        config=BrowserConfig(
            chrome_instance_path=get_chrome_path(),
            headless=False
        )
    )

    agent = Agent(
        task=f"""Abre Google Chrome y ve a https://docs.google.com/document. Crea un nuevo documento y escribe el siguiente texto: Hola mundo""",
        llm = ChatDeepSeek(model="deepseek-chat"),
        browser=browser,
    )

    await agent.run()
    await browser.close()
    input('Presiona Enter para salir...')

if __name__ == '__main__':
    asyncio.run(main())
