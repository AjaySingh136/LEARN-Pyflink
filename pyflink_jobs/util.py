from pyflink.table import EnvironmentSettings, TableEnvironment


def create_table_env(streaming: bool = True) -> TableEnvironment:
    settings = EnvironmentSettings.in_streaming_mode() if streaming else EnvironmentSettings.in_batch_mode()
    t_env = TableEnvironment.create(settings)

    # Optional: pipeline name for UI
    t_env.get_config().set("pipeline.name", "PyFlink Learning Job")

    # Example: Set default parallelism
    t_env.get_config().set("parallelism.default", "1")

    # Note: connector jars are already in /opt/flink/lib via Docker build
    return t_env