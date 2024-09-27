FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app app
COPY migrations migrations
COPY backend/zazen.py backend/boot.sh ./

ENV FLASK_APP=zazen.py
ENV FLASK_ENV=development 

RUN chmod a+x boot.sh

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
