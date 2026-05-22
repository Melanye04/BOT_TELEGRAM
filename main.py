import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise RuntimeError("TOKEN não encontrado. Verifique o arquivo .env")


# Função para enviar todas imagens da pasta
async def enviar_pasta(caminho, message):
    try:
        arquivos = sorted(os.listdir(caminho))

        for arquivo in arquivos:
            caminho_arquivo = os.path.join(caminho, arquivo)

            if os.path.isfile(caminho_arquivo):
                with open(caminho_arquivo, 'rb') as img:
                    await message.reply_photo(photo=img)

    except Exception as e:
        await message.reply_text(f"Erro ao carregar imagens: {e}")


# Menu inicial
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Como se registrar", callback_data="registro")],
        [InlineKeyboardButton("Definir senha", callback_data="senha")],
        [InlineKeyboardButton("Cadastrar PIX", callback_data="pix")],
        [InlineKeyboardButton("Como negociar", callback_data="negociacao")],
        [InlineKeyboardButton("Sacar dinheiro", callback_data="saque")],
        [InlineKeyboardButton("OKX passo a passo", callback_data="okx")],
        [InlineKeyboardButton("Doação instituição", callback_data="doacao")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "Escolha uma opção abaixo",
            reply_markup=reply_markup
        )
        
def menu_principal():
    keyboard = [
        [InlineKeyboardButton("Como se registrar", callback_data="registro")],
        [InlineKeyboardButton("Definir senha", callback_data="senha")],
        [InlineKeyboardButton("Cadastrar PIX", callback_data="pix")],
        [InlineKeyboardButton("Como negociar", callback_data="negociacao")],
        [InlineKeyboardButton("Sacar dinheiro", callback_data="saque")],
        [InlineKeyboardButton("OKX passo a passo", callback_data="okx")],
        [InlineKeyboardButton("Doação instituição", callback_data="doacao")],
    ]
    return InlineKeyboardMarkup(keyboard)       


# Botões
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query is None:
        return

    await query.answer()
    message = query.message

    if message is None or not isinstance(message, Message):
        return

    # Mapeamento das pastas
    pastas = {
        "registro": "images/registro",
        "senha": "images/senha",
        "pix": "images/pix",
        "negociacao": "images/negociacao",
        "saque": "images/saque",
        "okx": "images/okx",
        "doacao": "images/doacao"
    }

    if query.data == "okx":
        keyboard = [
            [InlineKeyboardButton("Criar conta", callback_data="okx_conta")],
            [InlineKeyboardButton("Comprar USDT", callback_data="okx_compra")],
            [InlineKeyboardButton("Voltar", callback_data="menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("Escolha uma opção OKX:", reply_markup=reply_markup)
    elif query.data in pastas:
        await message.reply_text("Enviando passo a passo...")
        await enviar_pasta(pastas[query.data], message)
# Inicialização
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

if __name__ == "__main__":
    print("Bot rodando...")
    app.run_polling()
    