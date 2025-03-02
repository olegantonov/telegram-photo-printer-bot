# Telegram Photo Printer Bot

Este projeto é um **bot do Telegram** que monitora mensagens contendo números de fotos e envia automaticamente essas imagens para impressão usando a **biblioteca win32print** no Windows.

## 📌 Funcionalidades
- **Monitora mensagens do Telegram** para identificar números de fotos.
- **Verifica a existência do arquivo** antes de iniciar a impressão.
- **Imprime automaticamente** as fotos usando a impressora FUJIFILM ASK-300.
- **Garante intervalo mínimo entre impressões** para evitar sobrecarga.
- **Responde com mensagens de status** sobre o processo de impressão.

## 🛠️ Tecnologias Utilizadas
- **Python 3**
- **python-telegram-bot**
- **PIL (Pillow)**
- **win32print e win32ui** (Windows)

## 🚀 Como Usar
### **1. Configurar o Ambiente**
Antes de rodar o bot, instale as dependências:
```sh
pip install -r requirements.txt

2. Configurar as Variáveis
Configurar o Token do Telegram: Substitua a chave na linha:
python
Copiar
Editar
updater = Updater("SEU_TOKEN_AQUI", use_context=True)
Configurar a impressora: Substitua o nome da impressora no código:
python
Copiar
Editar
printer_name = "FUJIFILM ASK-300 (Copiar 3)"
3. Rodar o Bot
sh
Copiar
Editar
python src/printer_bot.py
4. Enviar Mensagens no Telegram
O bot aceita mensagens no formato:

yaml
Copiar
Editar
1234
1235-2   # (Imprime 2 cópias da foto 1235)
Ele responde com o status da impressão e envia alertas caso a foto ainda não esteja disponível.

📄 Licença
Este projeto é distribuído sob a licença MIT.

✍️ Autor
Daniel Marques

yaml
Copiar
Editar

---

### **Arquivo Principal (`src/printer_bot.py`)**
O código fornecido foi salvo no arquivo `printer_bot.py`, dentro da pasta `src/`.

---

### **Arquivo `.gitignore`**
```txt
# Ignorar arquivos temporários do sistema operacional
.DS_Store
Thumbs.db

# Ignorar cache do Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Logs
logfile.log
