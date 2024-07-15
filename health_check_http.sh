#!/bin/bash

# Spring Boot应用的健康检查URL
health_check_url="http://localhost:8080/actuator/health"

max_retries=30
retry_interval=1

retries=0
while [ $retries -lt $max_retries ]; do
    # 发送HTTP请求进行健康检查
    response=$(curl -s -o /dev/null -w "%{http_code}" "$health_check_url")

    if [ "$response" = "200" ]; then
        echo "Spring Boot application is up and running."
        break
    fi

    echo "Spring Boot application is not yet running. Retry in $retry_interval seconds..."
    sleep $retry_interval
    retries=$((retries + 1))
done

if [ $retries -eq $max_retries ]; then
    echo "Maximum retries reached. Spring Boot application is still not running."
fi