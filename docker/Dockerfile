FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gnucobol \
    python3 \
    python3-pip \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask flask-cors gunicorn

WORKDIR /app

COPY 01-batch/ /app/01-batch/
COPY 02-db2/sql/ /app/02-db2/sql/
COPY docker/compile.sh /app/compile.sh
COPY docker/server.py /app/server.py
COPY docker/db2_sim.py /app/db2_sim.py
COPY docker/cics_screens.py /app/cics_screens.py
COPY docker/static/ /app/static/

RUN mkdir -p /app/bin && chmod +x /app/compile.sh

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/programs')" || exit 1

EXPOSE 8080

CMD ["sh", "-c", "bash /app/compile.sh && python3 -c 'from db2_sim import init_db; init_db()' && gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 30 server:app"]
