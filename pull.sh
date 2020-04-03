#!/bin/bash
#根据输入参数找到对应项目，执行pull操作
#project1、project2为实际项目目录，p1、p2对应简称
for args in $@
do
  if [ $args == "p1" ]
    then
      cd project1
      git pull
      cd ..
    elif [ $args == "p2" ]
    then
      cd project2
      git pull
      cd ..
    else
    echo "项目不存在"
  fi
done