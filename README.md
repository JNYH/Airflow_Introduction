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
      

**Step 3**. Initialize the database (takes a few minutes) <br>
In the terminal where the file `docker-compose.yaml` is located, run this command:

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

When the Airflow container is running on Docker, you are free to edit the DAG files and test running them on Airflow (via browser). This includes files in the mounted volumes such as `utils` folder.


**Step 6**. Stop and remove container (Ctrl+C) <br>
Option (i) To keep volumes (folders) for the next run. DAG run histories will remain intact.

    docker compose down

Option (ii) To remove volumes associated with containers use `-v`

    docker compose down -v

Option (iii) To delete all files, use `--volumes --rmi all`. Will have to re-download the files in the next run.

    docker compose down --volumes --rmi all

To restart container, do **Step 3** and **Step 4**.

---
## Set up Airflow to send email from Gmail

First, create a Google "App Password" for your Gmail account. This is done so that you don't use your original password or 2 Factor authentication.

Visit your [App passwords](https://security.google.com/settings/security/apppasswords) page. You may be asked to sign in to your Google Account. <br>
* Under "Your app passwords", click **Select app** and choose "Mail". <br>
* Click **Select device** and choose "Other (Custom name)" so that you can input "Airflow". <br>
* Select **Generate**. <br>
* Copy the generated App password (the 16 character code in the yellow bar), for example xxxxyyyyxxxxyyyy. <br>
* Select **Done**. <br>
* Once you are finished, you won’t see that App password code again. <br>However, you will see a list of apps and devices (which you've created App passwords for) in your Google Account.

Next is to set up the Airflow SMTP server, edit `docker-compose.yaml`

    environment:
      AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
      AIRFLOW__SMTP__STARTTLS: 'true'
      AIRFLOW__SMTP__SSL: 'false'
      AIRFLOW__SMTP__SMTP_PORT: 587
      AIRFLOW__SMTP__SMTP_USER: mypersonalemail@gmail.com
      AIRFLOW__SMTP__SMTP_PASSWORD: xxxxyyyyxxxxyyyy
      AIRFLOW__SMTP__SMTP_MAIL_FROM: mypersonalemail@gmail.com



