import logging
import threading
import time
import re
import os
from PIL import Image
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import Update
import win32print
import win32ui
from PIL import ImageWin  # Se você planeja usar ImageWin.Dib(img)

# Configuração do log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logfile.log"),
        logging.StreamHandler()
    ]
)

# Variáveis globais
status = {'impressas': 0, 'pendentes': 0}
chat_ids = set()
last_print_time = 0  # Adicionado para controle do tempo de impressão



    
# Função de impressão usando a biblioteca win32
def print_with_win32(photo_path, printer_name):
    global status

    # Intervalo mínimo entre duas impressões em segundos
    min_interval = 3.0  # Ajuste este valor de acordo com o limite de taxa

    current_time = time.time()
    elapsed_time = current_time - last_print_time

    if elapsed_time < min_interval:
        time_to_wait = min_interval - elapsed_time
        time.sleep(time_to_wait)
    try:
        img = Image.open(photo_path)
        width, height = img.size

        # Se a imagem for horizontal, rotacione-a
        if width > height:
            img = img.rotate(90, expand=True)
            img.save('rotated_temp_image.png')  # Salve a imagem rotacionada temporariamente
            photo_path = 'rotated_temp_image.png'
        
        # Redimensionar a imagem para corresponder ao tamanho do papel
        paper_width, paper_height = 1235, 1860
        img = img.resize((paper_width, paper_height), Image.LANCZOS)

        hprinter = win32print.OpenPrinter(printer_name)
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(printer_name)
        pdc.StartDoc(photo_path)
        pdc.StartPage()

        # Renderize a imagem para o contexto do dispositivo
        ImageWin.Dib(img).draw(pdc.GetHandleOutput(), (0, 0, img.width, img.height))
        
        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()
        win32print.ClosePrinter(hprinter)

        logging.info("Foto impressa com sucesso.")
        
    except Exception as e:
        logging.error(f"Erro de impressão: {e}")
        status['impressas'] += 1

        time.sleep(5)

# Função para impressão de fotos
def print_photo(photo_number: str, copies: int, printer_name: str, context: CallbackContext, chat_id: int) -> None:
    global status
    
    logging.info(f"Tentando imprimir a foto {photo_number}")
    folder_path = "G:\\.shortcut-targets-by-id\\1rekGfQbooqqm_VwooIePdyhXjnI9Fyom\\__PHOTOS_DONE"
    photo_path = os.path.join(folder_path, f"{photo_number}.png")
    
    already_notified = False

    while not os.path.exists(photo_path):
        if not already_notified:
            logging.info(f"Foto {photo_number} ainda não disponível, aguardando...")
            context.bot.send_message(chat_id=chat_id, text=f"Aguardando foto {photo_number} ser carregada.")
            already_notified = True
        time.sleep(5)

    try:
        context.bot.send_message(chat_id=chat_id, text=f"Foto {photo_number} na fila de impressão.")
        
        for _ in range(copies):
            print_with_win32(photo_path, printer_name)
        
        logging.info(f"Foto {photo_number} impressa com sucesso")
        context.bot.send_message(chat_id=chat_id, text=f"Foto {photo_number} impressa com sucesso.")
    except Exception as e:
        logging.error(f"Erro de impressão da foto {photo_number}: {e}")
        context.bot.send_message(chat_id=chat_id, text=f"Erro de impressão da foto {photo_number}.")

    status['impressas'] += 1


# Função para impressão em thread separada
def threaded_print(photo_number, copies, printer_name, context, chat_id):
    threading.Thread(target=print_photo, args=(photo_number, copies, printer_name, context, chat_id)).start()

# Função para manipular mensagens recebidas
def handle_messages(update: Update, context: CallbackContext) -> None:
    global status
    global chat_ids
    
    chat_id = update.message.chat_id
    chat_ids.add(chat_id)

    msg = update.message.text
    match = re.search(r'Foto nr\.:\s*(\d+(-\d+)?)', msg)
    if match:
        msg = match.group(1)
    
    photo_data = [data.strip() for data in msg.split(',') if re.match(r'\d+(-\d+)?', data.strip())]
    if photo_data:
        printer_name = "FUJIFILM ASK-300 (Copiar 3)"
        for data in photo_data:
            copies = 1
            if '-' in data:
                photo_number, copies = data.split('-')
                copies = int(copies)
            else:
                photo_number = data

            threaded_print(photo_number, copies, printer_name, context, chat_id)
            status['pendentes'] += 1

# Função principal para iniciar o bot
def main() -> None:
    logging.info("Iniciando o bot.")
    updater = Updater("6648969640:AAEqoUJpT3VYMc7xaYsum1XXzPiQUu5tSXQ", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    updater.start_polling(poll_interval=5.0)
    logging.info("Bot iniciado.")
    updater.idle()

# Ponto de entrada do script
if __name__ == '__main__':
    main()
