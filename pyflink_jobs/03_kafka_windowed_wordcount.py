from pyflink.table import EnvironmentSettings, TableEnvironment

def main():
    t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
    t_env.get_config().set("pipeline.name", "03 - Kafka Windowed WordCount")
    # Enable periodic checkpoints (optional for dev)
    t_env.get_config().set("execution.checkpointing.interval", "10 s")

    # Kafka source with event time
    t_env.execute_sql("""
        CREATE TABLE input_words (
            word STRING,
            ts TIMESTAMP(3),
            WATERMARK FOR ts AS ts - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'input-words',
            'properties.bootstrap.servers' = 'kafka:9092',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json',
            'json.ignore-parse-errors' = 'true'
        )
    """)

    # Kafka sink for counts
    t_env.execute_sql("""
        CREATE TABLE output_counts (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            word STRING,
            cnt BIGINT
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'output-counts',
            'properties.bootstrap.servers' = 'kafka:9092',
            'format' = 'json'
        )
    """)

    # Tumbling window of 10 seconds on event time
    t_env.execute_sql("""
        INSERT INTO output_counts
        SELECT
            WINDOW_START,
            WINDOW_END,
            word,
            COUNT(*) AS cnt
        FROM TABLE(
            TUMBLE(TABLE input_words, DESCRIPTOR(ts), INTERVAL '10' SECOND)
        )
        GROUP BY WINDOW_START, WINDOW_END, word
    """).wait()


if __name__ == "__main__":
    main()