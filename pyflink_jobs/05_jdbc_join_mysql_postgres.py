from pyflink.table import EnvironmentSettings, TableEnvironment

def main():
    t_env = TableEnvironment.create(EnvironmentSettings.in_batch_mode())
    t_env.get_config().set("pipeline.name", "05 - JDBC Join (MySQL + Postgres)")

    # MySQL users
    t_env.execute_sql("""
        CREATE TABLE users_mysql (
            id INT,
            name STRING
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:mysql://mysql:3306/flinkdb',
            'table-name' = 'users',
            'username' = 'flink',
            'password' = 'flink'
        )
    """)

    # Postgres transactions
    t_env.execute_sql("""
        CREATE TABLE transactions_pg (
            txn_id INT,
            user_id INT,
            amount DECIMAL(12,2),
            created_at TIMESTAMP(3)
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/flinkdb',
            'table-name' = 'transactions',
            'username' = 'flink',
            'password' = 'flink'
        )
    """)

    # Filesystem sink for join results
    t_env.execute_sql("""
        CREATE TABLE user_spend_sink (
            user_id INT,
            name STRING,
            total DECIMAL(12,2)
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///data/out/jdbc_join',
            'format' = 'csv'
        )
    """)

    # Join and aggregate
    t_env.execute_sql("""
        INSERT INTO user_spend_sink
        SELECT u.id AS user_id, u.name, SUM(t.amount) AS total
        FROM users_mysql u
        JOIN transactions_pg t
          ON u.id = t.user_id
        GROUP BY u.id, u.name
        ORDER BY total DESC
    """).wait()


if __name__ == "__main__":
    main()