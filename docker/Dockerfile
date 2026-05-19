FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gnucobol \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask flask-cors

WORKDIR /app

COPY 01-batch/ /app/01-batch/
COPY docker/compile.sh /app/compile.sh
COPY docker/server.py /app/server.py
COPY docker/static/ /app/static/

RUN mkdir -p /app/bin && chmod +x /app/compile.sh

EXPOSE 8080

CMD ["python3", "server.py"]
