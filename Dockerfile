FROM rasa/rasa:3.6.20-full

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt || true

EXPOSE 5005

CMD ["rasa", "run", "--enable-api", "--cors", "*"]