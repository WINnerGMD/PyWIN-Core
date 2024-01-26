FROM python:3.11


RUN mkdir /pywin_core

WORKDIR /pywin_core

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


RUN chmod a+x docker/*.sh

ENTRYPOINT ["/pywin_core/docker/start.sh"]