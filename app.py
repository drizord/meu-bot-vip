import os
import logging
import hmac
import hashlib
import requests

from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TRIBOPAY_WEBHOOK_SECRET = os.getenv("TRIBOPAY_WEBHOOK_SECRET")
GRUPO_VIP_ID = os.getenv("GRUPO_VIP_ID") #adicione essa linha

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bem-vindo ao bot VIP!")

async def add_user_to_group(user_id): #função para adicionar user ao grupo.
    try:
        await application.bot.add_chat_member(chat_id=int(GRUPO_VIP_ID), user_id=user_id)
        logging.info(f"Usuário {user_id} adicionado ao grupo {GRUPO_VIP_ID}")
    except Exception as e:
        logging.error(f"Erro ao adicionar usuário ao grupo: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Tribopay-Signature')
    data = request.get_data()

    expected_signature = hmac.new(
        TRIBOPAY_WEBHOOK_SECRET.encode(),
        msg=data,
        digestmod=hashlib.sha256
    ).hexdigest()

    if hmac.compare_digest(signature.encode(), expected_signature.encode()):
        data_json = request.get_json()
        logging.info(f"Webhook recebido: {data_json}")

        # Exemplo de processamento do webhook (ADAPTE PARA SUA LÓGICA):
        if data_json.get("event") == "payment.paid": #verifica o tipo de evento.
          payment_id = data_json.get("data").get("id") #pega o id do pagamento
          customer_email = data_json.get("data").get("customer").get("email") #pega o email do cliente
          logging.info(f"Pagamento Aprovado ID: {payment_id}, Cliente Email: {customer_email}")
          # Aqui você adiciona a lógica para consultar seu banco de dados ou o TriboPay API para confirmar o pagamento
          # Se o pagamento estiver confirmado, adicione o usuário ao grupo

          # Exemplo (você precisa adaptar para o seu fluxo)
          user_id_to_add = 1234567890  # Substitua pelo ID do usuário que pagou, esse ID voce tem que buscar no banco de dados a partir do email do cliente
          add_user_to_group(user_id_to_add)
          logging.info(f"User ID {user_id_to_add} processado para adicionar no grupo")


        return jsonify({'status': 'success'}), 200
    else:
        logging.error("Assinatura inválida")
        return jsonify({'status': 'error'}), 400

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Inicia o bot em background
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    