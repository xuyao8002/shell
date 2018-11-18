kill -9 `ps ax | grep "fileServer-0.0.1-SNAPSHOT.jar" | grep -v 'grep' | awk '{ print $1; }'`
#ps -ef | grep "fileServer-0.0.1-SNAPSHOT.jar" | grep -v grep | awk '{print $2}' | xargs kill -9
sleep 5
export JAVA_HOME=/usr/local/xuyao/jdk1.8
export PATH=$JAVA_HOME/bin:$PATH
cd /usr/local/project/upload
rm -rf fileServer-0.0.1-SNAPSHOT.jar
cp /var/lib/jenkins/workspace/upload/target/fileServer-0.0.1-SNAPSHOT.jar /usr/local/project/upload
nohup java -jar fileServer-0.0.1-SNAPSHOT.jar >nohup.out 2>&1 --server.port=8888 &

