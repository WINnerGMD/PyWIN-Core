FROM python:3.11


RUN mkdir /pywin_core

WORKDIR /pywin_core

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


RUN chmod a+x start.sh
EXPOSE 80


ENTRYPOINT ["/start.sh"]
#CMD gunicorn core:fastapi --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:6000