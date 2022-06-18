FROM python:3.10.2

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY 🏡_Home.py .

RUN mkdir -p pages
COPY pages/👤_Sign_Up.py pages

EXPOSE 8501

CMD ["streamlit", "run", "🏡_Home.py", "--server.port", "8501", "--logger.level=debug"]
