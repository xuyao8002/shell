#!/bin/bash

#根据名称判断进程是否存在，重试一定次数
#重试次数
retries=5
#进程名称
process_name="x"
count=0
while [ $count -lt $retries ]; do
    if pgrep -x "$process_name" > /dev/null; then
        break;
    else
        count=$((count+1))
    fi
    sleep 1
done