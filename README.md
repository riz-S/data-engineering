# Final Project Data Engineering B

Kelompok 5
Anggota:

- Muhammad Fathur R Khairul
- Zahra Asma Annisa
- Riza Setiawan Soetedjo

---

## Table of Contents

- [Final Project Data Engineering B](#final-project-data-engineering-b)
  - [Table of Contents](#table-of-contents)
  - [Preparation](#preparation)
    - [What is needed?](#what-is-needed)
    - [Installing Linux on Windows (WSL 2)](#installing-linux-on-windows-wsl-2)
    - [How to use WSL 2](#how-to-use-wsl-2)
    - [Download The Tools](#download-the-tools)
      - [Install Kafka in WSL 2](#install-kafka-in-wsl-2)
      - [Download Database Browser](#download-database-browser)
      - [Install Python](#install-python)
      - [Install Airflow](#install-airflow)
      - [Install Great Expectations](#install-great-expectations)
  - [Setup Great Expectations](#setup-great-expectations)
    - [Connect Great Expectations to SQLite](#connect-great-expectations-to-sqlite)
    - [Make the Expectation(s)](#make-the-expectations)
    - [Create Checkpoint and Run](#create-checkpoint-and-run)
  - [ETL Process](#etl-process)
  - [Setup Scheduling](#setup-scheduling)
    - [Airflow User Creation](#airflow-user-creation)
    - [Configure the Scheduler](#configure-the-scheduler)
      - [Tasks](#tasks)
    - [Setting up the directories](#setting-up-the-directories)
    - [Start the Scheduler and Airflow Web Server](#start-the-scheduler-and-airflow-web-server)
    - [Airflow Bugs](#airflow-bugs)
    - [Run Scheduler on Webserver](#run-scheduler-on-webserver)
  - [Run the Model](#run-the-model)
    - [Import Library](#import-library)
    - [Data retrieval](#data-retrieval)
    - [Preprocessing](#preprocessing)
      - [Preparation](#preparation-1)
    - [Data retrieval](#data-retrieval-1)
    - [TF-IDF Vectorizer](#tf-idf-vectorizer)
    - [Word Cloud](#word-cloud)
    - [Affinity Propagation](#affinity-propagation)
    - [Silhouette Coefficient](#silhouette-coefficient)
  - [Scripts Used](#scripts-used)
    - [etl](#etl)
    - [start_kafka](#start_kafka)
    - [stop_kafka](#stop_kafka)

## Preparation

### What is needed?

- Linux Environment
- Apache Kafka
- Apache Airflow
- Database Browser
- Script Files
- Python Files
- Great Expectation

### Installing Linux on Windows (WSL 2)

You need a linux environment because Airflow is easier to setup in Linux. In the case of Windows users, they can use WSL 2 to install the tools needed for this. Guide on this is based on https://docs.microsoft.com/en-us/windows/wsl/install-manual

1. Enable WSL feature by opening powershell as admin and type

   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   ```

2. Check requirements for WSL 2
   For x64 systems, windows 10 version 1903 or higher with Build 18362 or higher is needed. You can check the version and build number by selecting **Windows logo key + R**, type **winver**, select OK.
   The output will be this window
   ![Windows Version](img\WindowsVersion.png 'Windows Version')

3. Enable Virtual Machine feature by opening powershell as admin and type

   ```powershell
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

4. Restart your PC

5. Download the Linux kernel update package in https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

6. Download Linux in Microsoft Store

   It doesn't have to be Ubuntu, so any other Linux System is okay.
   ![Download Ubuntu Img](img\UbuntuInStore.png 'Download Ubuntu Img')

7. Set WSL 2 as default version in powershell by typing

   ```powershell
   wsl --set-default-version 2
   ```

8. Launch the app and create a user account and password for the Ubuntu

### How to use WSL 2

To use Ubuntu from WSL 2, you can do these commands from powershell

```powershell
wsl -e Ubuntu #The command to execute Ubuntu as the WSL Distro
wsl -l -v #To check the version of the Ubuntu and its state
wsl #To open the Ubuntu from WSL. This will open the window as Ubuntu
```

To stop Ubuntu from command, you can do these commands

```shell
exit #To exit Ubuntu and return to powershell
```

```powershell
wsl -t Ubuntu #To stop Ubuntu state in WSL
wsl -l -v #To check if the Ubuntu has stopped
```

### Download The Tools

Some tools need to be downloaded while others can just be installed.

#### Install Kafka in WSL 2

This guide is based on https://www.confluent.io/blog/set-up-and-run-kafka-on-windows-linux-wsl-2/. You need to open the powershell as Ubuntu first.

1. Install Java (in this case, Java 8)

   Everytime you use the sudo command, you need to write the password for your account.

   ```shell
   sudo apt install openjdk-8-jdk -y
   ```

2. Check the Java version

   ```shell
   java -version
   ```

3. Download Kafka from https://kafka.apache.org/downloads

   In this guide, We use kafka_2.13-3.0.0.tgz as the downloaded file

4. Extract the kafka file to project location

#### Download Database Browser

In this guide, we use SQLite3 as the Database to store the data. Since SQLite3 created a DB file, we can download database browser from https://sqlitebrowser.org/dl/ to see the data later on.

#### Install Python

This guide is based on https://medium.com/@rhdzmota/python-development-on-the-windows-subsystem-for-linux-wsl-17a0fa1839d.

Install Python using these commands

```shell
sudo apt update && upgrade
sudo apt install python3 python3-pip ipython3
```

#### Install Airflow

This guide is based on https://towardsdatascience.com/run-apache-airflow-on-windows-10-without-docker-3c5754bb98b4.

1. Install Airflow
   ```shell
   pip3 install apache-airflow
   ```
2. Restart Ubuntu terminal then type
   ```shell
   airflow info
   ```
   It should be fine if you see this
   ![Airflow Info](img\AirflowInfo.png 'Airflow Info')

#### Install Great Expectations

Installing Great Expectations by following this guide
https://docs.greatexpectations.io/docs/guides/setup/installation/local

1. Ensure that Python is installed by using this command in the terminal
   ```shell
   python --version
   ```
2. Ensure that Pip is installed by using this command in the terminal
   ```shell
   python -m ensurepip --upgrade
   python -m pip install great_expectations
   ```
3. Ensure that Great Expectations is installed by using this command in the terminal
   ```shell
   great_expectations --version
   ```

## Setup Great Expectations

### Connect Great Expectations to SQLite

The steps below is based on this guide https://docs.greatexpectations.io/docs/guides/connecting_to_your_data/database/sqlite/

1. Choose how to connect. In this case, we choose Not CLI + Filesystem
2. Install necessary dependency
   ```shell
   pip install sqlalchemy
   ```
3. Configure SQLite database URL
   ```shell
   sqlite:///<PATH_TO_DB_FILE>
   ```
4. Instantiate DataContext of final project by first importing the necessary package and module

   ```shell
   from ruamel import yaml

   import great_expectations as ge
   from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
   ```

5. Configure Datasource by using this template
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
   Run this code to test the configuration
   ```shell
   context.test_yaml_config(yaml.dump(datasource_config))
   ```
6. Save the configuration to DataContext using the add_datasource function
   ```shell
   context.add_datasource(**datasource_config)
   ```
7. Test the new datasource by moving the data to Validator using BatchRequest. In this case, we specify the table name using this template.
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

### Make the Expectation(s)

These steps follow these guides https://greatexpectations.io/expectations, https://docs.greatexpectations.io/docs/guides/expectations/how_to_create_and_edit_expectations_based_on_domain_knowledge_without_inspecting_data_directly

1. Use the terminal to make notebook for the guide
   ```shell
   great_expectations --v3-api suite new
   ```
2. Create an expectation configuration in the newly created notebook. Notebook configurations vary according to the expected expectations, and can be seen in the following documentation https://greatexpectations.io/expectations
3. Save the expectation by running the last cell on the notebook. This will automatically generate a JSON file with a configured expectation suite that can be used to validate data.

### Create Checkpoint and Run

This step is done by following the following guide https://docs.greatexpectations.io/docs/guides/validation/checkpoints/how_to_create_a_new_checkpoint

1. Make sure first that Python is installed by typing the following command in the terminal
    ```shell
    great_expectations --v3-api checkpoint new my_checkpoint
    ```
    Next, users will be directed to Jupyter Notebook where there is a guide for creating checkpoints.
2. Create a checkpoint by following the guidelines
3. Test the configuration using context.test_yaml_config
    ```shell
    context.test_yaml_config(yaml_config=config)
    ```
4. Save the checkpoint configuration by running the corresponding cell in the Jupyter Notebook

The results of the above steps can be seen in great_expectations/uncommitted/data_docs/local_site/index.html

## ETL Process

The ETL process begins with the Extract process, namely data retrieval, where this is done by retrieving Stream data from the Twitter API to the producer in the python/Producer.py module.

Next, the data is received by the Consumer in the python/Consumer1.py, python/Consumer2.py, and python/Consumer3.py modules where the Transform step is carried out to prepare the data before being entered into the prepared model. The transform includes text preprocessing, where tweet data is cleaned and time is normalized.

After that, the Load step is carried out where the data is uploaded to the database, in this case a file called Tweets.db. The Validation process will be found in the python/Validator.py module.

## Setup Scheduling

There are few steps to setup Scheduling with Airflow

### Airflow User Creation

According to https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#create_repeat1, there are a Command Line Interface to create user in Airflow 2 which can support roles and passwords.

```shell
airflow users create [-h] -e EMAIL -f FIRSTNAME -l LASTNAME [-p PASSWORD] -r
ROLE [--use-random-password] -u USERNAME
```

In this case, we need to modify the CLI just like below

```shell
airflow users create [-h] [-p admin] -u admin
```

### Configure the Scheduler

Next step, we need to configure the Scheduler. There are some steps to do a good configuration

1. Importing Modules

   Let's start the configuration with importing all the modules we needed.

   ```python
   from datetime import datetime, timedelta
   from textwrap import dedent

   # The DAG object; we'll need this to instantiate a DAG
   from airflow import DAG

   # Operators; we need this to operate!
   from airflow.operators.bash import BashOperator
   IMPORT SOURCE CODE DISINI
   ```

2. Default Arguments

   To create a DAG and some tasks, we have two choices. First one, explicitly pass a set of arguments to each task's constructor which would become redundant. The other choice is define a dictionary of default parameters that can we use (this way better).

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

3. Instantiate a DAG

   We need to declare a DAG object to nest our task into.

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

   #### Tasks

   Tasks are generated when instantiating operator objects.

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

4. Define the task sequences

   Task sequences

   ```shell
   t1 >> t2 >> t3
   ```

### Setting up the directories

After we configure the Scheduler. We need to setting up the Scheduler's directories. The Scheduling file must be located in airflow/dags folder. If the folder is not created yet, create it using the command line below

```shell
mkdir dags
```

Then copy the Scheduling file using the command line below

```shell
cp python/Scheduling.py /home/typozjr/airflow/dags/de_final_project.py
```

### Start the Scheduler and Airflow Web Server

If all the configuration were done. We can start the Scheduler with the command line below

```shell
airflow db init
airflow webserver -p 8080
airflow scheduler
```

### Airflow Bugs

There are a bug in Airflow that may cause an error while running a code. The "Jinja" bug error is one of them. According to https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=62694614, we can overcome this bug by adding a space at the end of the bash-command.

The other bug is while runnning a task. Sometimes we faced the Airflow successfully executed but the task didn't run. We can overcome this bug by leaving extra interval between the DAG's start time and the current time.

### Run Scheduler on Webserver
1. Login according to the account that was created
    ![Login DAG](img\LoginAirflowWebserver.png 'Login DAG')
2. Search for DAG according to the name created in the setup scheduler
    ![DAG List](img\ListDAG.png 'DAG List')
3. Run DAG by toggle button on top left
    ![DAG Path](img\RunDAG.png 'DAG Path')
4. If you don't want to wait for the scheduled time, you can trigger it manually using the button on the top right. The running status of the DAG is visible on the webserver
    ![Manual Trigger](img\ManualTriggerDAG.png 'Manual Trigger')
5. Can also view the Gantt Chart of a process to see the time and order of the run
    ![Gantt Chart](img\GanttChartDAG.png 'Gantt Chart')

## Run the Model

### Import Library

Import some required libraries such as numpy, pandas, sqlite3, spacy, and sklearn

### Data retrieval

The data is retrieved from the SQLite3 Tweets.db database by making a connection to the database and after that taking the tweet column to be converted into a dataframe

### Preprocessing

#### Preparation

Define punctuation, language used, stop words and parser. In addition, it also prepares the spacecy_tokenizer function which is processing data from documents in the form of tweets into tokens. This processing is in the form of case folding, stopword removal, and tokenization. This simplification is intended to reduce noise in the data so as to increase the accuracy of the Text Mining process.

### Data retrieval

The data will be retrieved from the database and stored in the form of

### TF-IDF Vectorizer

Tweet data is entered into the TF IDF Vectorizer so that it can be entered into the model. The vectorizer uses the previously defined spacy_tokenizer function and ngram_range which means that each word in the tweet will be vectorized individually.

### Word Cloud

After that, the data visualization was carried out. This visualization begins with cleaning the data using the space_tokenizer earlier. After that, visualization is done in the form of Word Cloud by importing the wordcloud and matplotlib libraries

### Affinity Propagation

Affinity propagation is clustering by determining the number of clusters according to the model. The results of affinity propagation will be stored in the form of a numpy array of integers.

### Silhouette Coefficient

In this case, we measure the model using the Silhouette Coefficient using the cosine matrix. This value is directly proportional to the quality of the model. In our experiment, it was found that experiments with a longer Stream time will produce a higher Silhouette Coefficient which means the quality of the model in cluster prediction.

## Scripts Used

### etl

This script is used to start the ETL process by calling certain files. In the section delimited by "&" signifies the process is called asynchronously

### start_kafka

This script is used to start the zookeeper and kafka servers daemonically (in the background)

### stop_kafka

This script is used to terminate zookeeper and kafka servers
