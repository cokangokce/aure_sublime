import os
from groq import Groq
from dotenv import load_dotenv
from config import Config

load_dotenv()

class AIService:
    def __init__(self):
        # .env veya config.py üzerindeki anahtarı alır
        api_key = os.getenv('GROQ_API_KEY') or Config.GROQ_API_KEY
        self.client = Groq(api_key=api_key.strip() if api_key else "")

    def yanit_uret(self, kullanici_mesaji, gecmis_mesajlar=None):
        try:
            messages = [{"role": "system", "content": Config.BUSINESS_CONTEXT}]
            
            if gecmis_mesajlar and isinstance(gecmis_mesajlar, list):
                messages.extend(gecmis_mesajlar)
                
            messages.append({"role": "user", "content": kullanici_mesaji})

            # Aktif Groq Modeli: openai/gpt-oss-120b
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                temperature=0.5
            )

            return completion.choices[0].message.content

        except Exception as e:
            print(f"Groq API Hatasi: {str(e)}")
            return f"Sistem hatasi olustu: {str(e)}"

ai_service = AIService()