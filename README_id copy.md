# Projek Akhir Data Engineering B

Kelompok 5
Anggota:

- Muhammad Fathur R Khairul
- Zahra Asma Annisa
- Riza Setiawan Soetedjo

---

# Daftar Isi

- [Projek Akhir Data Engineering B](#projek-akhir-data-engineering-b)
- [Daftar Isi](#daftar-isi)
- [Preparasi](#preparasi)
  - [Apa yang Diperlukan?](#apa-yang-diperlukan)
  - [Instalasi Linux di Windows Menggunakan WSL 2](#instalasi-linux-di-windows-menggunakan-wsl-2)
  - [Cara Penggunaan WSL 2](#cara-penggunaan-wsl-2)
  - [Pengunduhan Alat Konfigurasi](#pengunduhan-alat-konfigurasi)
    - [Pemasangan Kafka di WSL 2](#pemasangan-kafka-di-wsl-2)
    - [Pengunduhan Database Browser](#pengunduhan-database-browser)
    - [Pemasangan Python](#pemasangan-python)
    - [Pemasangan Airflow](#pemasangan-airflow)
    - [Pemasangan Great Expectations](#pemasangan-great-expectations)
- [Persiapan Great Expectations](#persiapan-great-expectations)
  - [Hubungkan Great Expectations ke SQLite](#hubungkan-great-expectations-ke-sqlite)
  - [Buat Expectation(s)](#buat-expectations)
  - [Buat Checkpoint dan Jalankan](#buat-checkpoint-dan-jalankan)
- [Proses ETL](#proses-etl)
- [Persiapan Scheduling](#persiapan-scheduling)
  - [Pembuatan Pengguna Airflow](#pembuatan-pengguna-airflow)
  - [Konfigurasi Scheduler](#konfigurasi-scheduler)
    - [Tasks](#tasks)
  - [Konfigurasi Direktori](#konfigurasi-direktori)
  - [Mulai Scheduler dan Airflow Web Server](#mulai-scheduler-dan-airflow-web-server)
  - [Bugs dalam Airflow](#bugs-dalam-airflow)
  - [Jalankan Scheduler di Webserver](#jalankan-scheduler-di-webserver)
- [Menjalankan Model](#menjalankan-model)
  - [Import Library](#import-library)
  - [Pengambilan Data](#pengambilan-data)
  - [Preprocessing](#preprocessing)
    - [Persiapan](#persiapan)
  - [Pengambilan data](#pengambilan-data-1)
  - [TF-IDF Vectorizer](#tf-idf-vectorizer)
  - [Word Cloud](#word-cloud)
  - [Affinity Propagation](#affinity-propagation)
  - [Silhouette Coefficient](#silhouette-coefficient)
- [Script yang Digunakan](#script-yang-digunakan)
  - [etl](#etl)
  - [start_kafka](#start_kafka)
  - [stop_kafka](#stop_kafka)

# Preparasi

## Apa yang Diperlukan?

- Environment Linux
- Apache Kafka
- Apache Airflow
- Database Browser
- Berkas Script
- Berkas Python

## Instalasi Linux di Windows Menggunakan WSL 2

Kami memerlukan environment Linux karena dalam environment tersebut, Airflow lebih mudah dipasang. Dalam kasus pengguna Windows, pengguna dapat menggunakan WSL 2 dengan mengikuti panduan berikut https://docs.microsoft.com/en-us/windows/wsl/install-manual

1. Nyalakan fitur WSL dengan membuka Powershell sebagai admin dan ketik

   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   ```

2. Cek kebutuhanperangkat untuk memasang WSL 2
   Untuk sistem x64, diperlukan Windows 10 dengan versi 1903 atau di atasnya dengan Build 18362 atau lebih. Versi ini dapat dicek dengan memilih **Windows logo key + R**, ketik **winver**, pilih OK.
   Perintah tersebut akan mengeluarkan hal yang serupa dengan di bawah ini
   
   ![Windows Version](img\WindowsVersion.png 'Windows Version')

3. Nyalakan fitur Virtual Machine dengan membuka Powershell sebagai admin and ketik

   ```powershell
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

4. Restart perangkat

5. Unduh paket pembaharuan kernel Linux di https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

6. Unduh Linux di Microsoft Store

   Tidak perlu Ubuntu, sistem Linux lainnya juga tidak apa-apa.
   ![Download Ubuntu Img](img\UbuntuInStore.png 'Download Ubuntu Img')

7. Atur Set WSL 2 sebagai versi default dalam Powershell dengan mengetik

   ```powershell
   wsl --set-default-version 2
   ```

8. Nyalakan aplikasi dan buat akun pengguna dan password untuk Ubuntu

## Cara Penggunaan WSL 2

Untuk menggunakan Ubuntu dari WSL 2, digunakan perintah berikut dari Powershell

```powershell
wsl -e Ubuntu #The command to execute Ubuntu as the WSL Distro
wsl -l -v #To check the version of the Ubuntu and its state
wsl #To open the Ubuntu from WSL. This will open the window as Ubuntu
```

Penghentian Ubuntu dapat dilakukan dengan perintah berikut

```shell
exit #To exit Ubuntu and return to powershell
```

```powershell
wsl -t Ubuntu #To stop Ubuntu state in WSL
wsl -l -v #To check if the Ubuntu has stopped
```

## Pengunduhan Alat Konfigurasi

Beberapa alat harus diunduh terlebih dahulu dan beberapa hanya perlu dipasang.

### Pemasangan Kafka di WSL 2

Pemasangan ini sesuai dengan panduan pada https://www.confluent.io/blog/set-up-and-run-kafka-on-windows-linux-wsl-2/, dimana Powershell sebagai Ubuntu perlu dibuka terlebih dahulu

1. Pasang Java (dalam kasus ini, Java 8)

   Tiap pengguna menggunakan perintah sudo, harus ditulis pula password akunnya.

   ```shell
   sudo apt install openjdk-8-jdk -y
   ```

2. Cek versi Java

   ```shell
   java -version
   ```

3. Unduh Kafka dari https://kafka.apache.org/downloads

   Dalam panduan ini, kami menggunakan kafka_2.13-3.0.0.tgz

4. Ekstrak berkas Kafka ke lokasi projek

### Pengunduhan Database Browser

Kami menggunakan SQLite3 sebagai Database untuk menyimpan data. Karena SQLite3 membuat file berformat DB, kami dapat mengunduh Database Browser dari https://sqlitebrowser.org/dl/ untuk melihat isi database yang dibuat nantinya.

### Pemasangan Python

Kami melakukannya dengan mengikuti panduan berikut https://medium.com/@rhdzmota/python-development-on-the-windows-subsystem-for-linux-wsl-17a0fa1839d.

Pasang Python dengan perintah berikut

```shell
sudo apt update && upgrade
sudo apt install python3 python3-pip ipython3
```

### Pemasangan Airflow

Kami melakukannya dengan mengikuti panduan berikut https://towardsdatascience.com/run-apache-airflow-on-windows-10-without-docker-3c5754bb98b4.

1. Pasang Airflow
   ```shell
   pip3 install apache-airflow
   ```
2. Restart terminal Ubuntu lalu ketik
   ```shell
   airflow info
   ```
   Apabila sukses, maka akan tampil informasi seperti berikut
   ![Airflow Info](img\AirflowInfo.png 'Airflow Info')

### Pemasangan Great Expectations

Pemasangan Great Expectations kami lakukan dengan mengikuti panduan berikut
https://docs.greatexpectations.io/docs/guides/setup/installation/local

1. Pastikan terlebih dahulu bahwa Python telah terpasang dengan mengetik perintah berikut pada terminal
   ```shell
   python --version
   ```
2. Pastikan bahwa pip telah terpasang dengan mengetik perintah berikut pada terminal
   ```shell
   python -m ensurepip --upgrade
   python -m pip install great_expectations
   ```
3. Pastikan Great Expectations telah terpasang dengan mengetik perintah berikut pada terminal
   ```shell
   great_expectations --version
   ```

# Persiapan Great Expectations

## Hubungkan Great Expectations ke SQLite

Langkah ini dilakukan dengan mengikuti panduan berikut https://docs.greatexpectations.io/docs/guides/connecting_to_your_data/database/sqlite/

1. Pilih cara menjalankan kode, dalam kasus ini kami memilih untuk tidak menggunakan CLI dan menggunakan filesystem
2. Pasang dependensi yang diperlukan
   ```shell
   pip install sqlalchemy
   ```
3. Konfigurasikan URL database SQLite
   ```shell
   sqlite:///<PATH_TO_DB_FILE>
   ```
4. Instantiasi DataContext projek akhir dengan pertama mengimport package dan modul yang diperlukan

   ```shell
   from ruamel import yaml

   import great_expectations as ge
   from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
   ```

5. Konfigurasikan Datasource dengan menggunakan template sebagai berikut
   ```shell
   datasource_config = {
      "name": "my_sqlite_datasource",
      "class_name": "Datasource",
      "execution_engine": {
         "class_name": "SqlAlchemyExecutionEngine",
         "connection_string": "sqlite://<PATH_TO_DB_FILE>",
      },
      "data_connectors": {
         "default_runtime_data_connector_name": {
               "class_name": "RuntimeDataConnector",
               "batch_identifiers": ["default_identifier_name"],
         },
         "default_inferred_data_connector_name": {
               "class_name": "InferredAssetSqlDataConnector",
               "name": "whole_table",
         },
      },
   }
   ```
   Jalankan kode berikut untuk menguji konfigurasi
   ```shell
   context.test_yaml_config(yaml.dump(datasource_config))
   ```
6. Simpan konfigurasi datasource ke datacontext dengan menggunakan fungsi add_datasource
   ```shell
   context.add_datasource(**datasource_config)
   ```
7. Uji datasource baru dengan memindahkan data ke Validator menggunakan BatchRequest, dalam kasus ini kami melakukannya dengan menspesifikasi nama tabel. Template yang kami gunakan adalah sebagai berikut
   ```shell
      # Here is a BatchRequest naming a table
   batch_request = BatchRequest(
      datasource_name="my_sqlite_datasource",
      data_connector_name="default_inferred_data_connector_name",
      data_asset_name="yellow_tripdata_sample_2019_01",  # this is the name of the table you want to retrieve
   )
   context.create_expectation_suite(
      expectation_suite_name="test_suite", overwrite_existing=True
   )
   validator = context.get_validator(
      batch_request=batch_request, expectation_suite_name="test_suite"
   ```

## Buat Expectation(s)

Langkah ini dilakukan dengan mengikuti panduan berikut https://greatexpectations.io/expectations, https://docs.greatexpectations.io/docs/guides/expectations/how_to_create_and_edit_expectations_based_on_domain_knowledge_without_inspecting_data_directly

1. Manfaatkan CLI untuk membuat notebook dengan perintah berikut pada terminal
   ```shell
   great_expectations --v3-api suite new
   ```
2. Buat konfigurasi expectation di notebook yang baru dibuatkan. Konfigurasi notebook berbeda-beda sesuai dengan expectation yang diharapkan, dan dapat diliat pada dokumentasi berikut https://greatexpectations.io/expectations
3. Simpan expectation dengan menjalankan cell terakhir pada notebook tersebut. Hal ini akan otomatis menghasilkan file JSON dengan expectation suite yang telah dikonfigurasi dan dapat digunakan untuk melakukan validasi data.

## Buat Checkpoint dan Jalankan

Langkah ini dilakukan dengan mengikuti panduan berikut https://docs.greatexpectations.io/docs/guides/validation/checkpoints/how_to_create_a_new_checkpoint

1. Pastikan terlebih dahulu bahwa Python telah terpasang dengan mengetik perintah berikut pada terminal
   ```shell
   great_expectations --v3-api checkpoint new my_checkpoint
   ```
   Selanjutnya pengguna akan langsung diarahkan ke Jupyter Notebook dimana terdapat panduan untuk pembuatan checkpoint.
2. Buat checkpoint dengan mengikuti panduan yang ada
3. Uji konfigurasi dengan menggunakan context.test_yaml_config
   ```shell
   context.test_yaml_config(yaml_config=config)
   ```
4. Simpan konfigurasi checkpoint dengan menjalankan cell terkait di Jupyter Notebook tersebut

Hasil dari langkah-langkah di atas dapat dilihat pada great_expectations/uncommitted/data_docs/local_site/index.html

# Proses ETL

Proses ETL dimulai dengan proses Extract yaitu pengambilan data, dimana hal tersebut dilakukan dengan mengambilan data Stream dari Twitter API ke producer dalam modul python/Producer.py.

Selanjutnya, data diterima oleh Consumer pada modul python/Consumer1.py, python/Consumer2.py, dan python/Consumer3.py dimana dilakukan langkah Transform untuk mempersiapkan data sebelum dimasukkan ke model yang disiapkan. Transform tersebut meliputi text preprocessing, dimana data cuitan dibersihkan dan waktu dinormalisasikan.

Setelah itu, dilakukan langkah Load dimana data diunggah ke database, dalam kasus ini yaitu file bernama Tweets.db. Proses Validasi nantinya terdapat pada modul python/Validator.py.

# Persiapan Scheduling

Terdapat beberapa langkah untuk mempersiapkan Scheduling dengan menggunakan Airflow

## Pembuatan Pengguna Airflow

Menurut https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#create_repeat1, terdapat sebuah CLI (Command Line Interface) untuk membuat akun di Airflow 2 yang mendukung adanya roles atau peran dan sandi.

```shell
airflow users create [-h] -e EMAIL -f FIRSTNAME -l LASTNAME [-p PASSWORD] -r
ROLE [--use-random-password] -u USERNAME
```

Dalam kasus ini, kami perlu memodifikasi CLI dengan perintah berikut

```shell
airflow users create [-h] [-p admin] -u admin
```

## Konfigurasi Scheduler

Selanjutnya, Scheduler dikonfigurasi dengan langkah sebagai berikut

1. Import modul yang diperlukan

   ```python
   from datetime import datetime, timedelta
   from textwrap import dedent

   # Objek DAG; diperlukan untuk menginstantiasi DAG
   from airflow import DAG

   # Operator
   from airflow.operators.bash import BashOperator
   ```

2. Argumen Default

   Untuk menciptakan DAG dan task, dapat dilakukan 2 hal. Pertama yaitu memberikan sekumpulan argumen ke konstruktor tiap task secara eksplisit (redundan), kedua yaitu mendefinisikan dictionary dari parameter default yang dapat digunakan.

   ```python
   default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'email': ['riz_stwn@student.ub.ac.id'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
   }
   ```

3. Instantiasi sebuah DAG

   Diperlukan deklarasi objek DAG sebagai tempat task.

   ```python
   with DAG(
    'final-project-de',
    default_args=default_args,
    description='Final Project DE-B Klp 5',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2021, 12, 8),
    catchup=False,
    tags=['final-project'],
   ) as dag:
   ```

   ### Tasks

   Tasks dihasilkan ketika dalam proses instantiasi objek operator.

   ```python
   t1 = BashOperator(
      task_id='start_kafka',
      bash_command='/mnt/e/Projects/VisualStudio/PipelineStream/scripts/start_kafka.sh ',
   )

   t2 = BashOperator(
      task_id='etl',
      depends_on_past=False,
      bash_command='/mnt/e/Projects/VisualStudio/PipelineStream/scripts/etl.sh ',
      retries=3,
   )

   t3 = BashOperator(
      task_id='stop_kafka',
      depends_on_past=False,
      bash_command='/mnt/e/Projects/VisualStudio/PipelineStream/scripts/stop_kafka.sh ',
   )
   ```

4. Definisikan urutan task

   Urutan task

   ```python
   t1 >> t2 >> t3
   ```

## Konfigurasi Direktori

Setelah Scheduler selesai dikonfigurasi, maka saatnya untuk mengkonfigurasi direktori Scheduler. Berkas Scheduling harus ada dalam direktori airflow/dags. Apabila direktori tersebut masih belum dibuat, maka direktori tersebut dapt dibuat terlebih dahulu dengan menggunakan perintah berikut

```shell
mkdir dags
```

Lalu salin berkas Scheduling dengan perintah berikut

```shell
cp python/Scheduling.py /home/typozjr/airflow/dags/de_final_project.py
```

## Mulai Scheduler dan Airflow Web Server

Ketika seluruh konfigurasi telahd ilakuakn, maka Scheduler dapat dimulai dengan perintah berikut

```shell
airflow db init
airflow webserver -p 8080
airflow scheduler
```

## Bugs dalam Airflow

Terdapat beberapa bug dalam Airflow yang dapat menyebabkan error ketika menjalankan kode, salah satunya ialah error "Jinja.". Menurut https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=62694614, error ini dapat diatasi dengan menambahkan spasi di akhir perintah bash.

Bug lain yang kami temukan ialah ketika menjalankan suatu task,terkadang Airflow sukses menjalankannya namun task tersebut tidak berjalan. Bug ini dapat diatasi dengan menambahkan interval lebih di antara waktu dimulainya suatu DAG dan waktu pada saat ini.

## Jalankan Scheduler di Webserver
1. Login sesuai akun yang telah dibuat
   ![Login DAG](img\LoginAirflowWebserver.png 'Login DAG')
2. Cari DAG sesuai nama yang dibuat di setup scheduler
   ![Daftar DAG](img\ListDAG.png 'Daftar DAG')
3. Jalankan DAG dengan cara toggle tombol di kiri atas
   ![Jalan DAG](img\RunDAG.png 'Jalan DAG')
4. Jika tidak ingin menunggu waktu yang dijadwalkan, dapat melakukan trigger secara manual menggunakan tombol di kanan atas. Status jalannya DAG terlihat di webserver tersebut
   ![Trigger Manual](img\ManualTriggerDAG.png 'Trigger Manual')
5. Dapat juga melihat Gantt Chart dari satu proses untuk melihat waktu dan urutan jalannya
   ![Gantt Chart](img\GanttChartDAG.png 'Gantt Chart')

# Menjalankan Model

## Import Library

Melakukan import beberapa library yang dibutuhkan seperti numpy, pandas, sqlite3,spacy, dan sklearn

## Pengambilan Data

Data diambil dari database SQLite3 Tweets.db dengan cara membuat koneksi ke database dan setelah itu mengambil kolom tweet untuk diubah menjadi dataframe

## Preprocessing

### Persiapan

Pendefinisian punctuation, bahasa yang digunakan, stop words dan juga parser. Selain itu juga mempersiapkan fungsi spacy_tokenizer yang merupakan pengolahan data dari dokumen berupa cuitan menjadi token. Pengolahan ini berupa case folding, stopword removal, dan tokenisasi. Simplifikasi ini ditujukan untuk mengurangi noise pada data sehingga dapat meningkatkan akurasi dari proses Text Mining.

## Pengambilan data

Data akan diambil dari database dan disimpan dalam bentuk

## TF-IDF Vectorizer

Data cuitan dimasukkan ke TF IDF Vectorizer agar dapat dimasukkan ke model. Vectorizer menggunakan fungsi spacy_tokenizer yang tadi didefinisikan dan ngram_range yang berarti setiap kata dalam cuitan akan divektorisasi satu per satu.

## Word Cloud

Setelah itu dilakukan visualisasi data. Visualisasi ini diawali dari cleaning data menggunakan spacy_tokenizer tadi. Setelah itu dilakukan visualisasi dalam bentuk Word Cloud dengan mengimport library wordcloud dan matplotlib

## Affinity Propagation

Affinity propagation adalah clustering dengan penentuan banyak cluster yaitu sesuai modelnya. Hasil dari affinity propagation akan disimpan dalam bentuk numpy array of integer.

## Silhouette Coefficient

Pada kasus ini, kami mengukur model menggunakan Silhouette Coefficient dengan memanfaatkan matriks cosine. Nilai ini berbanding lurus dengan kualitas modelnya. Pada percobaan kami diperoleh bahwa percobaan dengan waktu Stream yang lebih lama akan menghasilkan Silhouette Coefficient yang lebih tinggi yang berarti kualitas model dalam prediksi cluster.

# Script yang Digunakan

## etl

Script ini digunakan untuk memulai proses ETL dengan memanggil file-file tertentu. Pada bagian yang dibatasi dengan tanda "&" menandakan proses dipanggil secara asinkronus

## start_kafka

Script ini digunakan untuk memulai server zookeeper dan kafka secara daemon (di background)

## stop_kafka

Script ini digunakan untuk mengakhiri server zookeeper dan kafka
