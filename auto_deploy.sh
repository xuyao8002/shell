#!/bin/bash

# 项目信息
repo_url="url"
local_path="/path"
service_name="service.jar"

# 拉取最新代码
pull_latest_code() {
    if [ -d "$local_path" ]; then
        cd "$local_path"
        git pull origin master
    else
        git clone "$repo_url" "$local_path"
    fi
}

# 编译和打包应用
build_and_package() {
    cd "$local_path"
    mvn -DskipTests clean package
}

# 终止现有服务
stop_service() {
    is_running
    if [ $? -eq "1" ]; then
        kill -9 $pid
    else
        echo "$service_name is not running"
    fi
}

# 启动新的服务
start_service() {
    jar_file="$local_path/target/$service_name"
    nohup java -jar "$jar_file" --spring.config.location=$local_path/application.properties > "$local_path/target/$service_name.log" 2>&1 &
}

# 是否运行中
is_running(){
    pid=`ps -ef | grep $service_name | grep -v grep | awk '{print $2}' `
    if [ -n "${pid}" ]; then
	return 1
    else
	return 0
    fi
}

# 当前状态
status(){
    is_running
    if [ $? -eq "1" ]; then
        echo "$service_name is running, pid: $pid"
    else
        echo "$service_name is not running"
    fi	
}

# 重启服务
restart_service(){
    stop_service
    start_service
}

# 主函数
main() {
    pull_latest_code
    echo "代码已更新"
    build_and_package
    echo "代码已构建"
    stop_service
    echo "服务已停止"
    start_service
    echo "应用已发布！"
}

#main

case "$1" in
    "start")
        start_service
    ;;
    "stop")
        stop_service
    ;;
    "status")
        status
    ;;
    "restart")
        restart_service
    ;;
    *)
        main
    ;;
esac

