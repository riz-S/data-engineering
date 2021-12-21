# Ke folder dimana script ini disimpan
cd /mnt/e/projects/visualstudio/pipelinestream

# Menunggu setelah proses sebelumnya selesai
wait

# Menjalankan ETL secara paralel
python3 python/Producer.py &
python3 python/Consumer1.py &
python3 python/Consumer2.py &
python3 python/Consumer3.py &

# Menunggu semua proses ETL selesai
wait

# Melakukan validasi ke data yang telah masuk
python3 python/Validator.py

# Keluar
exit 0