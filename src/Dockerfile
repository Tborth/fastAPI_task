
FROM python:3.9-slim

WORKDIR /app
COPY ./src .
COPY ./src/requirements.txt /app

RUN pip3 install -r requirements.txt


CMD python3 /app/main.py

# CMD ["uvicorn","src.route:app","--host=0.0.0.0","--reload"]