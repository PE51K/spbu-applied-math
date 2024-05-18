import logging
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from io import BytesIO

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./weights/best.pt')
model.conf = 0.03
model.iou = 0.03

# Load TrOCR model and processor
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-small-printed')
ocr_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-small-printed').to(device)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! Send me a picture, and I will perform OCR on detected objects.')

async def process_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.photo[-1].get_file()
    file_path = BytesIO()
    await file.download_to_memory(out=file_path)
    file_path.seek(0)
    img = Image.open(file_path)

    # Perform object detection
    results = model(img)

    # Crop the first detected object
    boxes = results.xyxy[0]
    if len(boxes) > 0:
        box = boxes[0]
        roi = img.crop(box[:4].cpu().int().tolist())

        # Perform OCR
        text = ocr(roi, processor, ocr_model)
        await update.message.reply_text(f'Detected text: {text}')
    else:
        await update.message.reply_text('No objects detected.')

def ocr(image, processor, model):
    pixel_values = processor(image, return_tensors='pt').pixel_values.to(device)
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

def main() -> None:
    application = Application.builder().token("7172458964:AAHUzjUaetrJX6BYJcnUdgdtbysssmr86Bk").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, process_image))

    application.run_polling()

if __name__ == '__main__':
    main()
