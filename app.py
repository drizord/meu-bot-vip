import requests
import os
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TRIBOPAY_API_KEY = os.environ.get("TRIBOPAY_API_KEY")  # Obtém o token das variáveis de ambiente (Render)
TRIBOPAY_API_URL = "https://api.tribopay.com.br" # URL base da API

def consultar_transacoes():
    try:
      if TRIBOPAY_API_KEY is None:
          raise ValueError("A variável TRIBOPAY_API_KEY não está configurada.")

      headers = {"Authorization": f"Bearer {TRIBOPAY_API_KEY}"} # Cabeçalho de autorização
      params = {"status": "pago"} # Parâmetros de consulta (opcional)
      response = requests.get(TRIBOPAY_API_URL + "/transacoes", headers=headers, params=params) # Endpoint da API

      response.raise_for_status() # Verifica se a requisição foi bem-sucedida (status 2xx)
      transacoes = response.json()
      logger.info(f"Resposta da API: {transacoes}") # Registra a resposta da API

      # Processa as transações aqui
      for transacao in transacoes:
          logger.info(f"Processando transação: {transacao.get('id')}") # Acessa o 'id' com segurança
          # Sua lógica de processamento aqui
          valor = transacao.get('valor') # Acessa o valor da transação
          if valor is not None:
              logger.info(f"Valor da transação: {valor}")
          else:
              logger.info("Campo 'valor' ausente na transação.")

    except requests.exceptions.RequestException as e:
      logger.error(f"Erro na requisição à API: {e}")
      if response is not None:
          logger.error(f"Resposta da API (erro): {response.text}") # Imprime a resposta de erro da API
    except ValueError as e:
      logger.error(f"Erro de configuração: {e}") # Registra erros de configuração
    except Exception as e:
      logger.exception("Erro na função consultar_transacoes:")

# Exemplo de chamada da função
consultar_transacoes()
