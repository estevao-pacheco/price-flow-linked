import os
import smtplib
from config import LISTING_MAPPING
from datetime import datetime, timedelta
from email.message import EmailMessage
from config import GMAIL_KEY
from services.cstech_client import get_prices
from services.xtay_client import send_prices
from services.transformer import (
    transform_and_save,
    build_xtay_payload
)

# CONFIGURAÇÕES DE E-MAIL (GMAIL)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_REMETENTE = "desenvolvimento@xtay.com.br"
EMAIL_SENHA = GMAIL_KEY
EMAIL_DESTINO = ["desenvolvimento@xtay.com.br"]

# DIRETÓRIO
pasta = r"C:\Users\XTAY\OneDrive - Atrio Hotéis S A\Documentos\Projetos\coisasdastays\price_sync\Data"

# LIMPAR DIRETÓRIO
def limpar_diretorio(pasta):
    
    arquivos_removidos = 0

    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            os.remove(caminho)
            arquivos_removidos += 1

# ENVIO DE E-MAIL
def enviar_email(status, mensagem):

        msg = EmailMessage()
        msg["Subject"] = f"[AUTOMAÇÃO ATUALIZAR PRICES LINKED BATEL] {status}"
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = ", ".join(EMAIL_DESTINO)

        corpo = f"""
Status: {status}
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Detalhes:
{mensagem}
        """
        msg.set_content(corpo)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_REMETENTE, EMAIL_SENHA)
            server.send_message(msg)

def main():
    inicio = datetime.now()
   
    from_date = datetime.today().strftime('%Y-%m-%d')
    to_date = (datetime.today() + timedelta(days=365)).strftime('%Y-%m-%d')
    try:

        limpar_diretorio(pasta)

        for m in LISTING_MAPPING:
            try:
                print(f"\n{m['name']} | {m['cstech']} → {m['xtay']}")

                raw_data = get_prices(m["cstech"], from_date, to_date)

                if not raw_data:
                    print("API retornou vazio, pulando...")
                    continue

                transformed = transform_and_save(raw_data, m["cstech"])

                if not transformed:
                    print("Transformação vazia, pulando...")
                    continue

                payload = build_xtay_payload(transformed)

                print(f"{len(payload)} dias processados | CSTECH: {m['cstech']}")

                if not payload:
                    print("Nenhum dado para envio, pulando...")
                    continue

                # DEBUG opcional
                # import json
                # print(json.dumps(payload, indent=2))

                send_prices(m["xtay"], payload)

            except Exception as e:
                print(f"Erro no mapping {m['cstech']} -> {m['xtay']}: {str(e)}")
            
            fim = datetime.now()
            duracao = fim - inicio

            mensagem = f"""
Processo executado com sucesso.
Preços Linked Batel atualizados no sistema Xtay.
Início: {inicio}
Fim: {fim}
Duração: {duracao}
        """
        enviar_email("SUCESSO", mensagem)

    except Exception as e:
        fim = datetime.now()
        duracao = fim - inicio
        erro = str(e)
        mensagem = f"""
Erro durante execução.
Início: {inicio}
Fim: {fim}
Duração: {duracao}
Erro:
{erro}
        """
        enviar_email("ERRO", mensagem)

if __name__ == "__main__":
    main()