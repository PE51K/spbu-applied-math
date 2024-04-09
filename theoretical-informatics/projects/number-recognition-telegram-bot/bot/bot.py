from io import BytesIO
from typing import Union

import keras_ocr
from pydantic_settings import BaseSettings
from telegram import (
    Update,
    Message,
    File
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)


class BotSettings(BaseSettings):
    telegram_bot_token: str

    class Config:
        env_file = './env/.env'


bot_settings: Union[BotSettings, None] = None
ocr_pipeline: Union[keras_ocr.pipeline.Pipeline, None] = None


# noinspection PyUnusedLocal
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Send me a photo and I\'ll try to recognize text in it.')


# noinspection PyUnusedLocal
async def recognize_text(update: Update, context: CallbackContext) -> None:
    global ocr_pipeline

    sticker_message: Message = await update.message.reply_sticker(
        sticker='CAACAgIAAxkBAAJMS2YHPrVKVmiyNhVR3J5vQE2Qpu-kAAIjAAMoD2oUJ1El54wgpAY0BA'
    )

    file_id: str = update.message.photo[-1].file_id
    photo_file: File = await context.bot.get_file(file_id)

    photo_buffer: BytesIO = BytesIO()
    await photo_file.download_to_memory(photo_buffer)
    photo_buffer.seek(0)

    images: list = [keras_ocr.tools.read(photo_buffer)]
    prediction_groups: list = ocr_pipeline.recognize(images)

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=sticker_message.message_id)

    # detected_text = "\n".join([word for word, box in prediction_groups[0]])
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Detected text: {detected_text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Detected text: {prediction_groups}")


def filter_prediction(prediction):
    """Filter prediction to find the required pattern in recognized text."""
    for pair in prediction:
        word = pair[0].replace('o', '0')
        if len(word) == 6 and word.isdigit():
            return word
    return 'I could not find the number :('


def setup_and_start_bot():
    global bot_settings, ocr_pipeline

    bot_settings = BotSettings()
    ocr_pipeline = keras_ocr.pipeline.Pipeline()

    application: Application = Application.builder().token(bot_settings.telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, recognize_text))

    application.run_polling()


if __name__ == '__main__':
    setup_and_start_bot()
