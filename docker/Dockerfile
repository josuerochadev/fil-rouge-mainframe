FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gnucobol \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask flask-cors

WORKDIR /app

COPY . /app/

RUN mkdir -p /app/bin

COPY compile.sh /app/compile.sh
RUN chmod +x /app/compile.sh

EXPOSE 8080

CMD ["python3", "server.py"]
