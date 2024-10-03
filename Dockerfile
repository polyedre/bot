FROM python

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD bot bot

ENTRYPOINT [ "flask", "--app", "bot", "run", "--port", "8080", "--host", "0.0.0.0" ]
