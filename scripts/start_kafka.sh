# Ke folder dimana kafka tersimpan
cd /mnt/e/projects/visualstudio/pipelinestream

# Menjaankan zookeeper secara daemon (Running in Background)
./kafka_2.13-3.0.0/bin/zookeeper-server-start.sh -daemon ./kafka_2.13-3.0.0/config/zookeeper.properties

# Tunggu 10 detik
sleep 10

# Menjalankan kafka server secara daemon (Running in Background)
./kafka_2.13-3.0.0/bin/kafka-server-start.sh -daemon ./kafka_2.13-3.0.0/config/server.properties

# Tunggu 20 detik
sleep 20

# Membuat topik pada kafka
./kafka_2.13-3.0.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic tugas-11-2

# Tunggu 5 detik
sleep 5
