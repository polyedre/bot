FROM python

ADD main.py requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]
