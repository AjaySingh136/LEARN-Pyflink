from pyflink.table import TableEnvironment, EnvironmentSettings

# Batch wordcount using filesystem source/sink
def main():
    t_env = TableEnvironment.create(EnvironmentSettings.in_batch_mode())
    t_env.get_config().set("pipeline.name", "01 - Batch WordCount (Filesystem)")

    # Filesystem source: one column 'line' read from CSV (each line is a row)
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

    # Filesystem sink: word, cnt
    t_env.execute_sql("""
        CREATE TABLE word_counts_sink (
            word STRING,
            cnt BIGINT
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///data/out/wordcount',
            'format' = 'csv'
        )
    """)

    # Use SQL with UNNEST(SPLIT(...)) to tokenize and count
    # Note: TRIM to drop empty tokens
    t_env.execute_sql("""
        INSERT INTO word_counts_sink
        SELECT word, COUNT(*) AS cnt
        FROM (
            SELECT TRIM(w) AS word
            FROM words_src,
            UNNEST(SPLIT(line, ' ')) AS t(w)
        )
        WHERE word IS NOT NULL AND word <> ''
        GROUP BY word
        ORDER BY cnt DESC, word
    """).wait()


if __name__ == "__main__":
    main()