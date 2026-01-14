## Real-time Data Lake 

This project demonstrates a practical end-to-end solution for building a real-time data lake. It showcases how to integrate Apache Kafka, Flink, Hadoop, and Apache Iceberg to stream data from a FastAPI application into a scalable, reliable data lake architecture.


#### Architecture Diagram
<img width="1078" height="357" alt="s3 drawio(1)" src="https://github.com/user-attachments/assets/46b8a888-84e0-40b3-9a90-5c0143d49be4" />

#### Prequisites
Before running the project , ensure you have the following installed:
|  Tool | Version  | Purpose  |
|---|---|---|
|  Java |  11+ |  Runtime for Hadoop/Kafka/Flink |
|  Python | 3.9+  | Running FastAPI Backend   |
|  Kafka | 4.0.0+  | Distributed Event Streaming   |
|  Hadoop | 3.x  | Catalog management & S3 Connectivity  | 
|  Iceberg | Latest  | Table Format  |
|  Flink | 2.1+ | Stream Processing Engine  |
|  S3 | -  | Cloud Object Storage  |
|  Uv | Latest  | Python Package Management   |
|  httpie | Latest  | API Testing   |

#### Key Benefits
- Near real-time data availability
- Reliable and scalable streaming architecture
- ACID-compliant lake storage
- Simplified analytics with Iceberg’s table layer
- Suitable for modern data engineering workloads


#### Setup Guide & Installation
Dependency Management

Download the required JARs to enable Flink's connectivity with S3 and Iceberg


```bash
# AWS SDK & S3 Connectivity
wget https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/2.20.16/bundle-2.20.16.jar

# Iceberg Flink Runtime
wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-flink-runtime-1.18/1.4.3/iceberg-flink-runtime-1.18-1.4.3.jar

# Hadoop AWS (required for S3A filesystem)
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar

```

Hadoop Configuration

Configure Hadoop to communicate with your S3 bucket. Replace placeholders with your actual credentials.

```bash
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
  <property>
    <name>fs.s3a.impl</name>
    <value>org.apache.hadoop.fs.s3a.S3AFileSystem</value>
  </property>
  <property>
    <name>fs.s3a.access.key</name>
    <value>${YOUR_ACCESS_KEY}</value>
  </property>
  <property>
    <name>fs.s3a.secret.key</name>
    <value>${YOUR_SECRET_KEY}</value>
  </property>
  <property>
    <name>fs.s3a.endpoint</name>
    <value>s3.amazonaws.com</value>
  </property>
  <property>
    <name>fs.s3a.path.style.access</name>
    <value>true</value>
  </property>
</configuration>
```

#### Execution Steps

**Step 1:** Start the Hadoop and Flink clusters:

```bash
# Start Hadoop (HDFS/YARN)
$HADOOP_HOME/sbin/start-all.sh

# Start Flink Cluster
$FLINK_HOME/bin/start-cluster.sh
```

**Step 2:** Launch FastAPI 
```bash
fastapi dev 
```
 **Step 3:** Run the Flink Stream Processor

In a new terminal, execute the PyFlink script to begin consuming Kafka events and writing to Iceberg:
```bash
py flink.py
```
**Step 4:** Test the Pipeline

Send a sample payload to the API:

```bash
curl -X POST http://localhost:8000/posts \
     -H "Content-Type: application/json" \
     -d '{"title": "Hello Iceberg", "body": "Testing real-time ingestion"}'
```
**Step 5:** Verification

Verify that data has been successfully written to your S3-backed Iceberg table using the Hadoop CLI:
```bash
hadoop fs -ls -R s3://your-bucket-name/data/
```
