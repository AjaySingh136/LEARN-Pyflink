# Flink + Python + PyFlink + Connectors
FROM flink:1.19.1-scala_2.12-java17

# Install Python and utilities
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install PyFlink (client libs for Python API)
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir apache-flink==1.19.1

# Copy connector installer and run it
COPY scripts/install_connectors.sh /opt/install_connectors.sh
RUN chmod +x /opt/install_connectors.sh && /opt/install_connectors.sh

# Folders for jobs and data (mounted by docker-compose)
RUN mkdir -p /opt/pyflink_jobs /data

USER flink