FROM python:3.6.2


WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "app.py" ]
CMD [ "app.py" ]