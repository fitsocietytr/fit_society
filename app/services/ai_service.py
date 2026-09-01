import requests

from config import Config


class AIServiceError(Exception):
    """Yapay zekâ servisinde oluşan hatalar için özel hata sınıfı."""
    pass


class AIService:
    """Fit Society için yapay zekâ servis katmanı."""

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.business_context = Config.BUSINESS_CONTEXT
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"

    def _sistem_talimati(self):
        """Yapay zekânın sistem talimatını döndürür."""
        return self.business_context

    def yanit_uret(self, mesaj, gecmis):
        """Kullanıcı mesajına yapay zekâ yanıtı üretir."""

        # API anahtarı yoksa demo modu çalışır.
        if not self.api_key:
            return (
                "Şu anda demo modundayım. "
                "Fit Society hakkında bilgi almak için "
                "iletişim bilgilerinizi bırakabilirsiniz."
            )

        messages = [
            {
                "role": "system",
                "content": self._sistem_talimati()
            }
        ]

        # Önceki konuşmaları mesaja ekler.
        if gecmis:
            messages.extend(gecmis)

        # Yeni kullanıcı mesajını en sona ekler.
        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        payload = {
            "model": self.model,
            "messages": messages
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.RequestException as error:
            raise AIServiceError(
                "Yapay zekâ servisine şu anda ulaşılamıyor."
            ) from error

        except (KeyError, IndexError, TypeError) as error:
            raise AIServiceError(
                "Yapay zekâdan geçerli bir yanıt alınamadı."
            ) from error


ai_service = AIService()