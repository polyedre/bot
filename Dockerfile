FROM python

ADD requirements.txt bot .

RUN pip install -r requirements.txt

ENTRYPOINT [ "flask", "--app", "bot", "run" ]
