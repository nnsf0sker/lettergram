FROM alpine:3.7

RUN apk add --update py3-pip
RUN pip3 install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py
COPY rest/ /app/rest/
COPY lettergram /app/lettergram/

EXPOSE 9000

CMD python /app/app.py
