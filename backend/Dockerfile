FROM python:3.8-slim

WORKDIR /src

COPY requirements.txt .

# Instalar dependencias del sistema y ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "4000"]
