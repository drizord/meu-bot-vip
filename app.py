import os
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Configuração de logging (MUITO IMPORTANTE!)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ... (suas outras funções, start, echo, etc.)

def webhook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tribopay_secret = os.environ.get("TRIBOPAY_WEBHOOK_SECRET")

        if tribopay_secret is None:
            logger.error("A variável TRIBOPAY_WEBHOOK_SECRET não está definida!")
            return "Erro: Segredo do webhook não configurado", 500  # ERRO 500!

        try:
            tribopay_secret_encoded = tribopay_secret.encode('utf-8')
        except Exception as e:
            logger.error(f"Erro ao codificar o segredo: {e}")
            return "Erro interno", 500

        # ... (SEU CÓDIGO USANDO tribopay_secret_encoded)

        return "Webhook processado com sucesso!", 200  # SUCESSO 200!

    except Exception as e:
        logger.exception("Erro na função webhook:") # Log completo do erro
        return "Erro interno do servidor", 500  # ERRO 500!

if __name__ == '__main__':
   # ... (seu código de inicialização, TOKEN, etc.)

    application.run_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN,
                            webhook_url=WEBHOOK_URL)

    application.idle()
    
