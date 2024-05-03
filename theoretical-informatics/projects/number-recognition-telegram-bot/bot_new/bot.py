from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from config import TOKEN
from detector import detect_image

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Отправь мне изображение для детекции.")

def handle_message(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('current_image.jpg')
    result_path = detect_image('current_image.jpg')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(result_path, 'rb'))

start_handler = CommandHandler('start', start)
image_handler = MessageHandler(Filters.photo, handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(image_handler)

updater.start_polling()
