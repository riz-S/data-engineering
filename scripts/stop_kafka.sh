# Ke folder dimana kafka tersimpan
cd /mnt/e/projects/visualstudio/pipelinestream

# Stop zookeeper server yang lagi jalan
./kafka_2.13-3.0.0/bin/kafka-server-stop.sh ./kafka_2.13-3.0.0/config/server.properties

# Stop kafka server yang lagi jalan
./kafka_2.13-3.0.0/bin/zookeeper-server-stop.sh ./kafka_2.13-3.0.0/config/zookeeper.properties
