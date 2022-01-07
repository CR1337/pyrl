FROM python:3.9

COPY . /device

RUN apt update
RUN apt install -y python-smbus
RUN pip3 install -r requirements.txt

CMD python3 start.py