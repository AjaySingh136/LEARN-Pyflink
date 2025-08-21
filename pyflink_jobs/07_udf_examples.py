from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.udf import udf
from pyflink.table import DataTypes

def main():
    t_env = TableEnvironment.create(EnvironmentSettings.in_batch_mode())
    t_env.get_config().set("pipeline.name", "07 - UDF Examples")

    # Simple scalar UDF: normalize a word (lowercase, strip punctuation)
    @udf(result_type=DataTypes.STRING())
    def normalize(s: str):
        if s is None:
            return None
        return ''.join(ch for ch in s.lower().strip() if ch.isalnum())

    t_env.create_temporary_system_function("normalize", normalize)

    # Source: filesystem lines
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

    # Sink
    t_env.execute_sql("""
        CREATE TABLE normalized_counts (
            word STRING,
            cnt BIGINT
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///data/out/udf_counts',
            'format' = 'csv'
        )
    """)

    # Use the UDF in SQL
    t_env.execute_sql("""
        INSERT INTO normalized_counts
        SELECT w AS word, COUNT(*) AS cnt
        FROM (
            SELECT normalize(tw) AS w
            FROM words_src,
            UNNEST(SPLIT(line, ' ')) AS t(tw)
        )
        WHERE w IS NOT NULL AND w <> ''
        GROUP BY w
        ORDER BY cnt DESC
    """).wait()


if __name__ == "__main__":
    main()