# Flink with Python (PyFlink) – A Complete Hands-On Guide and Project

This repository is a complete, practical “book” and lab to learn Apache Flink with Python end-to-end, powered by Docker. You will:

- Understand core Flink concepts in plain language
- Run a local Flink cluster with Kafka, Postgres, and MySQL
- Learn PyFlink (Table API and SQL) by running real jobs
- Work with multiple connectors (filesystem, Kafka, JDBC)
- Practice windows, joins, UDFs, watermarking, event time, and more
- Submit jobs and observe them in the Flink Web UI

Everything runs locally on macOS using Docker.

--------------------------------------------------------------------------------

Table of Contents
1) What You Will Build
2) Prerequisites (macOS)
3) Quick Start (TL;DR)
4) Flink Concepts in Plain English
5) Project Structure
6) How the Docker Stack Works
7) Learning Path (Step-by-Step)
8) Examples Index
9) Working with Connectors
10) UDFs (User-Defined Functions)
11) Time, Watermarks, and Windows
12) Stateful Processing (Intro)
13) Troubleshooting
14) Appendix: Install PyFlink Natively on macOS (Optional)

--------------------------------------------------------------------------------

1) What You Will Build
- A local learning playground for PyFlink:
  - Flink JobManager + TaskManager containers
  - Kafka in KRaft mode (no ZooKeeper)
  - Postgres and MySQL databases (with seeded demo data)
- A set of runnable PyFlink jobs that you can submit directly:
  - Filesystem wordcount (batch)
  - Streaming wordcount with Kafka
  - Windowed aggregations and watermarks (event time)
  - JDBC sinks (Postgres), JDBC joins (MySQL + Postgres)
  - UDFs (text normalization)
- A repeatable way to download and mount connector jars
- Samples and scripts that are easy to adapt for your own projects

--------------------------------------------------------------------------------

2) Prerequisites (macOS)
- Docker Desktop for Mac installed and running
- Enough disk and memory (at least 4GB for the stack)
- Terminal and basic shell familiarity

Optional (only if you want to run PyFlink without Docker): see Appendix.

--------------------------------------------------------------------------------

3) Quick Start (TL;DR)
- Build and start the stack:
  - docker compose up -d --build
- Verify Flink UI: http://localhost:8081
- Create Kafka topics:
  - ./scripts/create_kafka_topics.sh
- Submit a simple batch job (filesystem wordcount):
  - ./scripts/submit.sh pyflink_jobs/01_batch_word_count.py
- Produce streaming messages to Kafka:
  - docker compose exec kafka kafka-console-producer.sh --bootstrap-server kafka:9092 --topic input-words
  - Type lines like: {"word": "hello", "ts": "2025-01-01T00:00:00Z"}
- Submit streaming job:
  - ./scripts/submit.sh pyflink_jobs/03_kafka_windowed_wordcount.py

Outputs appear in ./data/out or in Kafka topic output-counts or inside databases.

--------------------------------------------------------------------------------

4) Flink Concepts in Plain English

- What is Flink?
  Apache Flink is a distributed engine for processing data streams and batch datasets at scale. It excels at low-latency, stateful stream processing with exactly-once guarantees.

- Key ideas:
  - Stream vs. Batch: In Flink, batch is often treated as bounded streams. PyFlink supports both Table API and SQL (primary) and DataStream (Python available but Table API is the most mature).
  - Time and Watermarks: For event-time processing, Flink uses watermarks to handle out-of-order data. Windows (tumbling, sliding) group stream data by time.
  - State and Checkpointing: Flink can remember information across events (state) and take periodic snapshots (checkpoints) so jobs can recover.
  - Connectors: Sources and sinks (Kafka, files, JDBC databases, etc.) are defined via DDL in the Table API/SQL with connector properties.

- Why PyFlink?
  PyFlink lets you write jobs in Python while leveraging Flink’s Java runtime. You typically use the Table API or SQL, define connectors in DDL, and submit through the Flink CLI.

--------------------------------------------------------------------------------

5) Project Structure

.
├── Dockerfile                      # Custom Flink image with Python + PyFlink + connectors
├── docker-compose.yml              # Flink + Kafka + Postgres + MySQL stack
├── .env                            # Version pins (Flink, connector, driver)
├── scripts/
│   ├── install_connectors.sh       # Downloads connector jars into the Flink lib
│   ├── submit.sh                   # Helper to submit a PyFlink job
│   └── create_kafka_topics.sh      # Creates input/output Kafka topics
├── db/
│   ├── postgres/init.sql           # Initializes Postgres with demo schema/data
│   └── mysql/init.sql              # Initializes MySQL with demo schema/data
├── pyflink_jobs/
│   ├── 01_batch_word_count.py      # Filesystem batch wordcount
│   ├── 03_kafka_windowed_wordcount.py # Streaming Kafka wordcount with watermarks + tumbling windows
│   ├── 04_jdbc_sink_postgres.py    # Write to Postgres via JDBC
│   ├── 05_jdbc_join_mysql_postgres.py # Join JDBC tables and sink to filesystem
│   ├── 07_udf_examples.py          # Scalar UDF demo
│   └── util.py                     # Shared helpers and config
└── data/
    ├── words.txt                   # Sample input for batch job
    └── out/                        # Outputs land here

Note: “even-numbered” slots are not used for all numbers to keep room for you to add exercises. Add your own jobs as pyflink_jobs/NN_description.py and submit them through scripts/submit.sh.

--------------------------------------------------------------------------------

6) How the Docker Stack Works

- Flink JobManager/TaskManager:
  - Our image includes Python 3 and pyflink, plus connectors jars placed in /opt/flink/lib
  - We mount ./pyflink_jobs into /opt/pyflink_jobs and ./data into /data
  - Submit jobs into the JobManager which coordinates execution; TaskManagers do the work

- Kafka (KRaft mode):
  - Single-broker setup suitable for local dev
  - Topics: input-words, output-counts
  - Use kafka-console-producer/consumer for testing

- Postgres/MySQL:
  - Auto-initialized with /docker-entrypoint-initdb.d .sql files
  - JDBC drivers pre-loaded; Flink can read/write via DDL

--------------------------------------------------------------------------------

7) Learning Path (Step-by-Step)

A) Setup and Explore
1. Start the stack: docker compose up -d --build
2. Open Flink UI: http://localhost:8081
3. Explore jars: docker compose exec jobmanager ls /opt/flink/lib
4. Verify DBs are live:
   - Postgres: psql -h localhost -U flink -d flinkdb (password: flink)
   - MySQL: mysql -h 127.0.0.1 -u flink -pflink flinkdb

B) Batch Fundamentals (Filesystem)
5. Run 01_batch_word_count.py to learn TableEnvironment, DDL, SELECT/UNNEST/GROUP BY:
   ./scripts/submit.sh pyflink_jobs/01_batch_word_count.py
   See output in ./data/out/wordcount

C) Streaming + Windows + Watermarks (Kafka)
6. Create Kafka topics: ./scripts/create_kafka_topics.sh
7. Start a Kafka console producer:
   docker compose exec kafka kafka-console-producer.sh --bootstrap-server kafka:9092 --topic input-words
   Paste JSON lines like: {"word":"hello","ts":"2025-01-01T00:00:10Z"}
8. Run 03_kafka_windowed_wordcount.py:
   ./scripts/submit.sh pyflink_jobs/03_kafka_windowed_wordcount.py
   Consume results:
   docker compose exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic output-counts --from-beginning

D) JDBC Sinks and Joins
9. Run 04_jdbc_sink_postgres.py to upsert word counts into Postgres:
   ./scripts/submit.sh pyflink_jobs/04_jdbc_sink_postgres.py
   Check results in Postgres table word_counts_jdbc
10. Run 05_jdbc_join_mysql_postgres.py to join across two JDBC sources:
   ./scripts/submit.sh pyflink_jobs/05_jdbc_join_mysql_postgres.py
   View filesystem output ./data/out/jdbc_join

E) UDFs
11. Run 07_udf_examples.py to see Python UDFs:
   ./scripts/submit.sh pyflink_jobs/07_udf_examples.py

F) Extend
12. Add your own connectors (e.g., different file formats), windows, or UDFs
13. Turn on checkpointing and state backends for production-like semantics
14. Scale TaskManagers and parallelism in docker-compose.yml

--------------------------------------------------------------------------------

8) Examples Index

- 01_batch_word_count.py
  Batch wordcount from a filesystem source to filesystem sink using SQL with UNNEST(SPLIT(...))

- 03_kafka_windowed_wordcount.py
  Streaming job:
  - Kafka source (JSON) with event-time timestamps and watermarks
  - Tumbling window aggregation
  - Kafka sink (JSON)

- 04_jdbc_sink_postgres.py
  Inserts/Upserts into Postgres using JDBC connector

- 05_jdbc_join_mysql_postgres.py
  Reads from MySQL and Postgres via JDBC, performs join, writes to filesystem

- 07_udf_examples.py
  Registers and uses a Python scalar UDF to normalize text

--------------------------------------------------------------------------------

9) Working with Connectors

We preload these jars at build time (see scripts/install_connectors.sh):
- flink-sql-connector-kafka-<ver>-1.19.jar
- flink-connector-jdbc-<ver>-1.19.jar
- postgresql-42.x.jar
- mysql-connector-j-8.x.x.jar

Using a connector in PyFlink is typically:
- create TableEnvironment
- execute_sql with CREATE TABLE ... WITH ('connector'='kafka'| 'filesystem' | 'jdbc', ...)

Important tips:
- For Kafka, set bootstrap.servers, topics, format (json/csv), and startup mode
- For JDBC, ensure the driver jar is in /opt/flink/lib and provide url, table-name, username, password
- For Filesystem, use file:/// absolute paths; in this project we mount ./data to /data

--------------------------------------------------------------------------------

10) UDFs (User-Defined Functions)

- Use Python UDFs for custom transforms:
  - Scalar UDFs (@udf(result_type=...)) for per-row functions
  - Register with table_env.create_temporary_function("name", udf_fn)
  - Use in SQL or Table API expressions

Caveats:
- UDFs run in separate Python worker processes; consider performance and serialization
- Prefer built-in SQL functions for simple transforms where possible

--------------------------------------------------------------------------------

11) Time, Watermarks, and Windows

- Event Time vs Processing Time:
  - Event time is the timestamp embedded in your events
  - Processing time is when the system processes events
- Watermarks provide bounds on out-of-orderness: e.g., ts - INTERVAL '5' SECOND
- Windows:
  - Tumbling: non-overlapping fixed-size windows (e.g., 10 seconds)
  - Sliding: overlapping windows that advance by slide (e.g., size 10s, slide 5s)
  - Session: gaps-based windows (more advanced in SQL)

We demo tumbling windows in 03_kafka_windowed_wordcount.py

--------------------------------------------------------------------------------

12) Stateful Processing (Intro)

- Flink keeps state per key for aggregations, joins, patterns
- Exactly-once semantics require checkpointing and a durable state backend
- For local learning, you can start with in-memory (RocksDB or HashMap in Java, but for Table API the runtime manages it)
- To enable checkpoints, set config keys (e.g., execution.checkpointing.interval)

In this project, we keep configs simple; you can enable checkpoints via TableEnvironment config before productionizing.

--------------------------------------------------------------------------------

13) Troubleshooting

- Job can’t find a connector:
  - Ensure the connector jar exists in /opt/flink/lib inside JobManager/TaskManager
  - Rebuild image if you changed versions: docker compose build --no-cache

- Kafka errors:
  - Confirm topics exist: ./scripts/create_kafka_topics.sh
  - Use kafka-console-consumer to inspect messages

- DB connectivity:
  - Confirm DB container is healthy
  - Check JDBC URL, user, and password

- File path errors:
  - Use file:/// absolute paths
  - Remember containers see /data, not your local filesystem paths

--------------------------------------------------------------------------------

14) Appendix: Install PyFlink Natively on macOS (Optional)

If you want to run PyFlink locally (without Docker):
1) Install Java 17:
   - brew install openjdk@17
   - export PATH="/usr/local/opt/openjdk@17/bin:$PATH"
   - export JAVA_HOME=$(/usr/libexec/java_home -v 17)
2) Python and PyFlink:
   - python3 -m venv .venv && source .venv/bin/activate
   - pip install --upgrade pip
   - pip install apache-flink==1.19.1
3) Run local jobs via flink run -py or pyflink shell, but you still need connector jars on the classpath to use Kafka/JDBC.
We recommend Docker for a complete, reproducible environment.

Happy streaming!