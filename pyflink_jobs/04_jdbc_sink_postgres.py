from pyflink.table import EnvironmentSettings, TableEnvironment

def main():
    t_env = TableEnvironment.create(EnvironmentSettings.in_batch_mode())
    t_env.get_config().set("pipeline.name", "04 - JDBC Sink (Postgres)")

    # Source: filesystem words (same as 01)
    t_env.execute_sql("""
        CREATE TABLE words_src (
            line STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///data/words.txt',
            'format' = 'csv',
            'csv.ignore-parse-errors' = 'true'
        )
    """)

    # Transform to word,count
    t_env.execute_sql("""
        CREATE TEMPORARY VIEW word_counts AS
        SELECT word, COUNT(*) AS cnt
        FROM (
            SELECT TRIM(w) as word
            FROM words_src, UNNEST(SPLIT(line, ' ')) AS t(w)
        )
        WHERE word IS NOT NULL AND word <> ''
        GROUP BY word
    """)

    # JDBC sink: Postgres table word_counts_jdbc(word TEXT PRIMARY KEY, cnt BIGINT)
    t_env.execute_sql("""
        CREATE TABLE word_counts_jdbc (
            word STRING,
            cnt BIGINT,
            PRIMARY KEY (word) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/flinkdb',
            'table-name' = 'word_counts_jdbc',
            'username' = 'flink',
            'password' = 'flink'
        )
    """)

    t_env.execute_sql("""
        INSERT INTO word_counts_jdbc
        SELECT word, cnt FROM word_counts
    """).wait()


if __name__ == "__main__":
    main()