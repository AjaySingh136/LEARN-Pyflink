#!/usr/bin/env bash
set -euo pipefail

# Uses .env defaults if present
FLINK_VERSION="${FLINK_VERSION:-1.19.1}"
CONNECTOR_VERSION="${FLINK_CONNECTOR_VERSION:-3.2.0}"
POSTGRES_DRIVER_VERSION="${POSTGRES_DRIVER_VERSION:-42.7.3}"
MYSQL_DRIVER_VERSION="${MYSQL_DRIVER_VERSION:-8.3.0}"

LIB_DIR="/opt/flink/lib"
mkdir -p "${LIB_DIR}"

echo "Downloading connectors into ${LIB_DIR} ..."

# Kafka SQL connector (matches Flink 1.19.x)
KAFKA_JAR="flink-sql-connector-kafka-${CONNECTOR_VERSION}-1.19.jar"
KAFKA_URL="https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/${CONNECTOR_VERSION}-1.19/${KAFKA_JAR}"

# JDBC connector (matches Flink 1.19.x)
JDBC_JAR="flink-connector-jdbc-${CONNECTOR_VERSION}-1.19.jar"
JDBC_URL="https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/${CONNECTOR_VERSION}-1.19/${JDBC_JAR}"

# Postgres JDBC driver
PG_JAR="postgresql-${POSTGRES_DRIVER_VERSION}.jar"
PG_URL="https://repo1.maven.org/maven2/org/postgresql/postgresql/${POSTGRES_DRIVER_VERSION}/${PG_JAR}"

# MySQL JDBC driver
MYSQL_JAR="mysql-connector-j-${MYSQL_DRIVER_VERSION}.jar"
MYSQL_URL="https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/${MYSQL_DRIVER_VERSION}/${MYSQL_JAR}"

download() {
  local url="$1"
  local out="$2"
  if [ ! -f "${out}" ]; then
    echo "-> ${url}"
    curl -fsSL "${url}" -o "${out}"
  else
    echo "Already exists: ${out}"
  fi
}

download "${KAFKA_URL}" "${LIB_DIR}/${KAFKA_JAR}"
download "${JDBC_URL}" "${LIB_DIR}/${JDBC_JAR}"
download "${PG_URL}" "${LIB_DIR}/${PG_JAR}"
download "${MYSQL_URL}" "${LIB_DIR}/${MYSQL_JAR}"

echo "Connector jars present in ${LIB_DIR}:"
ls -1 "${LIB_DIR}"