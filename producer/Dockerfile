FROM redpandadata/redpanda:latest

USER root

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -o Acquire::ForceIPv4=true update --fix-missing && \
    apt-get -o Acquire::ForceIPv4=true install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --chmod=755 requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chmod=755 entrypoint.sh /app/bin/entrypoint.sh
COPY --chmod=755 python_producer.py /app/bin/python_producer.py
WORKDIR /app/bin

ENTRYPOINT ["/bin/bash", "/app/bin/entrypoint.sh"]
