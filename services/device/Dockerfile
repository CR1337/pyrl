FROM python:3.9

COPY . /device

RUN apt update
RUN apt install -y python3-smbus=4.2-2
RUN apt install -y i2c-tools=4.2-2
RUN pip3 install -r requirements.txt

CMD python3 start.py