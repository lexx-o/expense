FROM python:3.10-slim
COPY ./frontend/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "src/main.py"]