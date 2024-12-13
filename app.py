import os
import logging
import hmac
import hashlib
import requests


from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("7586099231:AAG-OKSBGYzr2WAqTXy1aRuM8oCeutmARPw")
TRIBOPAY_WEBHOOK_SECRET = os.getenv("njiy12589%jgnbep3@5g")
GRUPO_VIP_ID = os.getenv("-4659850721") #adicione essa linha

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bem-vindo ao meu grupo VIP!")

async def add_user_to_group(user_id): #função para adicionar user ao grupo.
    try:
        await application.bot.add_chat_member(chat_id=int(-4659850721), user_id=user_id)
        logging.info(f"Usuário {user_id} adicionado ao grupo {-4659850721}")
    except Exception as e:
        logging.error(f"Erro ao adicionar usuário ao grupo: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)        

async def handle_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await echo(update, context) # Chama a função echo para mensagens
    # Adicione aqui outros tipos de tratamento, se necessário (edições, etc.)

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
    application = ApplicationBuilder().token(os.environ.get("7586099231:AAG-OKSBGYzr2WAqTXy1aRuM8oCeutmARPw")).build()

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) # Filtra mensagens de texto que não são comandos
    application.add_handler(start_handler)
    application.add_handler(message_handler)

    # Configuração do webhook:
    PORT = int(os.environ.get("PORT", 5000))
    application.run_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=os.environ.get("7586099231:AAG-OKSBGYzr2WAqTXy1aRuM8oCeutmARPw"),
                            webhook_url="https://meu-bot-vip.onrender.com/" + os.environ.get("7586099231:AAG-OKSBGYzr2WAqTXy1aRuM8oCeutmARPw"))

    application.idle()






#if __name__ == '__main__':
    application = ApplicationBuilder().token(B7586099231:AAG-OKSBGYzr2WAqTXy1aRuM8oCeutmARPw).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Inicia o bot em background
    application.run_polling(allowed_updates=Update.ALL_TYPES)
