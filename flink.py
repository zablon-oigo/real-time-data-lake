from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
env.enable_checkpointing(60000) 

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

t_env.get_config().set("pipeline.jars", "file:///opt/flink/lib/iceberg-flink-runtime-2.0-1.10.0.jar;file:///opt/flink/lib/iceberg-aws-bundle-1.10.0.jar")

t_env.execute_sql("""
CREATE CATALOG lakehouse WITH (
    'type'='iceberg',
    'catalog-type'='hadoop',
    'warehouse'='',
    'property-version'='1'
)
""")

t_env.execute_sql("USE CATALOG lakehouse")

t_env.execute_sql("CREATE DATABASE IF NOT EXISTS `raw`")

t_env.execute_sql("""
CREATE TABLE IF NOT EXISTS `raw`.posts (
    post_id STRING,
    user_id STRING,
    title STRING,
    content STRING,
    ts TIMESTAMP(3),
    PRIMARY KEY (post_id) NOT ENFORCED
) WITH (
    'format-version'='2',
    'write.upsert.enabled'='true'
)
""")


