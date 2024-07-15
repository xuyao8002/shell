#!/bin/bash

# Dubbo服务的主机和端口
host="localhost"
port="20880"

max_retries=30
retry_interval=1

retries=0
while [ $retries -lt $max_retries ]; do
    # 使用nc命令进行TCP连接测试
    nc -z -w 2 $host $port

    if [ $? -eq 0 ]; then
        echo "Dubbo service is up and running."
        break
    fi

    echo "Dubbo service is not yet running. Retry in $retry_interval seconds..."
    sleep $retry_interval
    retries=$((retries + 1))
done

if [ $retries -eq $max_retries ]; then
    echo "Maximum retries reached. Dubbo service is still not running."
fi