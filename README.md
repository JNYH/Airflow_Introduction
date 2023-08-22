# Airflow_Introduction

This is a memo to share what I have learnt in Apache Airflow.

The presentation file `Airflow_Introduction.pdf` provides a brief overview: 
* Airflow introduction
* Airflow key components
* Python code
* How to install Airflow

The DAG file `testJamesDAG.py` illustrates the DAG structure, and contains some common useful functions.

---
For a deeper learning about Airflow, please refer to another repository, where I have captured notes from a course in DataCamp: https://github.com/JNYH/DataCamp_Introduction_to_Airflow

---
## Install Airflow with Docker
Reference from [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)


**Step 0**. Install Docker Community Edition (CE) on your workstation from this link: <br>
https://docs.docker.com/engine/install/


**Step 1**. Download `docker-compose.yaml` by using the latest curl statement from this [link](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml). <br>
In the Bash terminal, navigate to an empty directory where the Airflow and Docker files can be stored, and run this:

    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml'

For SSL issue run this instead:

    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml' --ssl-no-revoke

To remove example DAGs, edit `docker-compose.yaml`

    environment:
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'


**Step 2**. Initialize Environment <br>
Create the necessary files, directories and initialize the database. Set AIRFLOW_UID. Add libraries to `requirements.txt`.

    mkdir -p ./dags ./logs ./plugins ./config ./utils
    echo "AIRFLOW_UID=50000" > .env
    echo "openpyxl" > requirements.txt

To add access folders, edit `docker-compose.yaml`

    volumes:
      - ${AIRFLOW_PROJ_DIR:-.}/utils:/opt/airflow/utils

To add additional Python libraries (separated by space " "), edit `docker-compose.yaml`

    environment:
      _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- openpyxl}
      

**Step 3**. Initialize the database (takes a few minutes)

    docker compose up airflow-init

When successfully done, you'd see: User "airflow" created with role "Admin". <br>
To check Docker image files created, run this:

    docker ps


**Step 4**. Running Airflow - start all services (takes a few minutes) <br>
To create/start scheduler and webserver etc, add `-d` to run in the background

    docker compose up -d


**Step 5**. Access Airflow via browser <br>
The webserver is available at: http://localhost:8080 <br>
(Note: this might take a minute to be ready) <br>
The default account has the login `airflow` and the password `airflow`


**Step 6**. Stop and remove container (Ctrl+C) <br>
Option (i) To keep volumes (folders) for the next run

    docker compose down

Option (ii) To remove volumes associated with containers use `-v`

    docker compose down -v

Option (iii) To delete all files, use `--volumes --rmi all`. Will have to re-download the files in the next run.

    docker compose down --volumes --rmi all

To restart container, do **Step 3** and **Step 4**.
