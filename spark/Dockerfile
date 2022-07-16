FROM openjdk:8-jre-slim

ARG spark_uid=185

ENV SPARK_HOME /opt/spark

RUN set -ex && \
    sed -i 's/http:\/\/deb.\(.*\)/https:\/\/deb.\1/g' /etc/apt/sources.list && \
    apt-get -y update && \
    ln -s /lib /lib64 && \
    apt install -y bash tini libc6 libpam-modules krb5-user libnss3 && \
    mkdir -p $SPARK_HOME && \
    mkdir -p $SPARK_HOME/python && \
    mkdir -p $SPARK_HOME/work-dir && \
    rm /bin/sh && \
    ln -sv /bin/bash /bin/sh && \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
    chgrp root /etc/passwd && chmod ug+rw /etc/passwd && \
    rm -rf /var/cache/apt/*

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl && \
    apt install -y python3 python3-pip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    rm -rf /var/cache/apt/*

ENV SPARK_VERSION=3.0.1
ENV HADOOP_VERSION=3.2

RUN curl -LOv https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars ${SPARK_HOME} && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin ${SPARK_HOME} && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/sbin ${SPARK_HOME} && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/kubernetes/dockerfiles/spark/entrypoint.sh /opt/ && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/python/pyspark ${SPARK_HOME}/python && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/python/lib ${SPARK_HOME}/python && \
    rm -rf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

WORKDIR $SPARK_HOME/jars
ENV MVN_URL=https://search.maven.org/remotecontent?filepath=

RUN \
    # Add Postgres jar to Spark
    curl -SLO https://jdbc.postgresql.org/download/postgresql-42.2.6.jar && \
    # Add Kafka jars to Spark
    curl -SLO ${MVN_URL}org/apache/commons/commons-pool2/2.9.0/commons-pool2-2.9.0.jar && \
    curl -SLO ${MVN_URL}org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.0.1/spark-token-provider-kafka-0-10_2.12-3.0.1.jar && \
    curl -SLO ${MVN_URL}org/apache/spark/spark-streaming-kafka-0-10_2.12/3.0.1/spark-streaming-kafka-0-10_2.12-3.0.1.jar && \
    curl -SLO ${MVN_URL}org/apache/kafka/kafka-clients/2.6.0/kafka-clients-2.6.0.jar && \
    curl -SLO ${MVN_URL}org/apache/spark/spark-sql-kafka-0-10_2.12/3.0.1/spark-sql-kafka-0-10_2.12-3.0.1.jar
    #Add AWS/S3 jars to Spark (Not needed yet)
    #curl -SLO ${MVN_URL}org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar && \
    #curl -SLO ${MVN_URL}com/amazonaws/aws-java-sdk/1.11.892/aws-java-sdk-1.11.892.jar && \
    #curl -SLO ${MVN_URL}com/amazonaws/aws-java-sdk-core/1.11.892/aws-java-sdk-core-1.11.892.jar && \
    #curl -SLO ${MVN_URL}com/amazonaws/aws-java-sdk-s3/1.11.892/aws-java-sdk-s3-1.11.892.jar && \
    #curl -SLO ${MVN_URL}com/amazonaws/aws-java-sdk-dynamodb/1.11.892/aws-java-sdk-dynamodb-1.11.892.jar

# Add extra Python lib
COPY ./requirements.txt /tmp/requirements.txt
ENV PYTHONPATH=/opt/spark/python/extra
RUN pip3 install --target ${SPARK_HOME}/python/extra --no-cache-dir -r /tmp/requirements.txt

# Copy PySpark job
COPY work-dir ${SPARK_HOME}
COPY data ${SPARK_HOME}/../data

WORKDIR /opt/spark

ENTRYPOINT [ "/opt/entrypoint.sh" ]

# Specify the User that the actual main process will run as
USER ${spark_uid}