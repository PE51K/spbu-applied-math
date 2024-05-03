# Используем образ с поддержкой CUDA
FROM nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y python3-pip

# Устанавливаем рабочий каталог в контейнере
WORKDIR /app

# Копируем файлы проекта в рабочий каталог
COPY . /app

# Устанавливаем необходимые зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Запускаем бота при старте контейнера
CMD ["python3", "bot.py"]

