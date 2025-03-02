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
