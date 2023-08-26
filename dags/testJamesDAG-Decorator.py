'''
This DAG provides sample codes for various purposes:
* get multiple payload values
* get task instance from previous task using xcom
* get some key word arguments
* create 1 Excel file (with multiple tabs) <--- required to install Excel support library `openpyxl`
  and create 1 CSV file 
* send an email with 2 attachment files <--- required to set up email SMTP in Airflow
@author: James

Version: 
2023-08-26 Created DAG in the decorator-based format introduced in Apache Airflow 2.0+
'''

import os
import pandas as pd
from datetime import datetime, timedelta
import pytz
from airflow import DAG
from airflow.models import Variable    #need this for Airflow.Admin.Variables
from airflow.decorators import dag, task
from airflow.operators.email_operator import EmailOperator
from pathlib import Path

import sys
sys.path.append('/opt/airflow/utils')    #to add custom functions
# from utils import custom_tools as ct

temp_storage_path = os.path.join(os.getcwd(), 'temp')                     #/opt/airflow/temp
excel_file_path2 = os.path.join(temp_storage_path, 'testJamesDAG.csv')    #/opt/airflow/temp/testJamesDAG.csv
excel_file_path = os.path.join(temp_storage_path, 'testJamesDAG.xlsx')    #/opt/airflow/temp/testJamesDAG.xlsx
localtz = pytz.timezone('Asia/Singapore')

try:
    support_email = Variable.get('testJamesDAG_support_emails', deserialize_json=True)['emails']    #from Airflow.Admin.Variables    #note: use "double" quotes json body
                                                                                                    #testJamesDAG_support_emails = {"emails": [ "jnyh@yahoo.com", "jnyh@yahoo.com" ]}
except:
    support_email = ['jnyh@yahoo.com']

DAG_ID = 'testJamesDAG-Decorator'    #same as filename testJamesDAG-Decorator.py
default_args = {
    'owner': 'JamesNg',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 25),
    'retries': 0,
    'retry_delay': timedelta(minutes=3),
    'email_on_retry': False,
    'email_on_failure': True,
    'email': support_email
}

@dag(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval=None,
    # schedule_interval = '01 00 28 * *',    #trigger monthly on 28th day at UTC 00:01:00 (HH:MM:SS) / SGT 08:01
    tags=['Test 2.0'],
    description='''This is a test DAG in the decorator-based format introduced in Apache Airflow 2.0+'''
)

def my_dag():
    
    @task
    def print_hello():
        return '#### Hello world from first Airflow DAG!'
    
    @task
    def get_payload(**context):
        #### get multiple payload values
        #### POST API with endpoint = '{base_url}/dags/{dag_name}/dag_runs'
        #### conf payload = {"key1": "value1", "key2": "value2"}    #note: use "double" quotes json body
        execution_date = context.get('logical_date')    #<datetime> object, this is the DAG run execution date in UTC timezone
        print('#### data_interval_start:', execution_date)                       #2023-01-12T10:31:14+00:00    #use this for UTC
        print('#### data_interval_end:', str(execution_date.add(minutes=30)))    #2023-01-12T11:01:14+00:00
        
        try:
            payload = context['dag_run'].conf
            print('#### payload:', payload)    #{'key1': 'value1', 'key2': 'value2'}
            v1 = payload.get('key1', 'nothing')
            v2 = payload.get('key2', 'nothing')
            return {'key1': v1, 'key2': v2}
        except:
            return {'key1': 'value1', 'key2': 'value2'}
        
    @task
    def get_task_instance(**kwargs):
        #### get task instance from previous task using xcom
        ti = kwargs['ti']    #ti = task instance
        payload = ti.xcom_pull(key=None, task_ids='get_payload')
        print('#### payload_dict:', payload)    #payload_dict: {'key1': 'value1', 'key2': 'value2'}
    
    @task
    def get_some_kwargs(**kwargs):
        #### get some key word arguments
        execution_date = kwargs['logical_date']    #<datetime> object, this is the DAG run execution date in UTC timezone
        print('#### execution_date:', execution_date)                        #2023-01-12T10:31:14+00:00    #use this for UTC
        print('#### execution_date:', execution_date.astimezone(localtz))    #2023-01-12T18:31:14+08:00    #use this for GMT+8

        some_kwargs = kwargs['my_param']
        print('#### my_param:', some_kwargs)    #my_param: Additional info from kwargs
    
    @task
    def create_excel(**kwargs):
        #### create an Excel file (with multiple tabs)
        df1 = pd.DataFrame({'col1': [0,1,2,3], 'col2': [0,1,2,3]})
        df2 = pd.DataFrame({'col1': [1,2,3,4], 'col2': [5,6,7,8]})

        print('#### os.getcwd():', os.getcwd())                        #current working directory is /opt/airflow
        print('#### os.listdir(os.curdir):', os.listdir(os.curdir))    #['logs', 'dags', 'airflow-worker.pid', 'airflow.cfg', 'webserver_config.py', 'temp', 'config']
        if not os.path.exists(temp_storage_path):
            os.makedirs(temp_storage_path)    #create `temp` folder if not exists
        
        #convert to CSV file
        df1.to_csv(excel_file_path2, index=False)
        file_size = Path(excel_file_path2).stat().st_size * 0.000001
        print('#### CSV file path:', excel_file_path2)
        print('#### CSV file consumed {:.3f} MB'.format(file_size))
        
        #convert to Excel file
        with pd.ExcelWriter(excel_file_path) as writer:
            df1.to_excel(writer, sheet_name='sheet1', index=False)
            df2.to_excel(writer, sheet_name='sheet2', index=False)
        file_size = Path(excel_file_path).stat().st_size * 0.000001
        print('#### Excel file path:', excel_file_path)
        print('#### Excel file consumed {:.3f} MB'.format(file_size))
    
    @task
    def build_email_with_attachment(subject, **context):
        #### send an email with the Excel attachment
        try:
            recipient_email = Variable.get('testJamesDAG_recipient_emails', deserialize_json=True)['emails']    #from Airflow.Admin.Variables    #note: use "double" quotes json body
                                                                                                                #testJamesDAG_recipient_emails = {"emails": [ "jnyh@yahoo.com", "jnyh@yahoo.com" ]}
        except:
            recipient_email = ['jnyh@yahoo.com']

        print('#### recipient_email:', recipient_email)

        addressee = recipient_email[0].split('@')[0].split('.')[0].title()    #first name of the first email in Titlecase
        print(addressee)

        #attach and send email
        file_size2 = Path(excel_file_path2).stat().st_size * 0.000001
        print('#### CSV file consumed {:.3f} MB'.format(file_size2))
        file_size = Path(excel_file_path).stat().st_size * 0.000001
        print('#### Excel file consumed {:.3f} MB'.format(file_size))
        
        if file_size2 + file_size < 20:    #email attachment limit max 20MB
            email_op = EmailOperator(
                task_id='send_email',
                to=recipient_email,
                subject=subject,
                html_content=('Hi ' + addressee + '... <br>Please see attached file(s) as requested. <br><br>Thank you!'),
                files=[excel_file_path2, excel_file_path]
            )
        else:
            email_op = EmailOperator(
                task_id='send_email',
                to=recipient_email,
                subject=subject,
                html_content=('Hi ' + addressee + '... <br>Excel file size has exceeded 20MB. <br><br>Please contact Support.')
            )
        email_op.execute(context)
    
    @task
    def email_on_failure(**kwargs):
        #### to send email when a failure is encountered

        #do something, then an error is encountered
        raise ValueError('Intentionally throwing an error to send an email.')
        #the DAG stops running after this!
    


    print_hello_task = print_hello()
    get_payload_task = get_payload()
    get_task_instance_task = get_task_instance()
    get_some_kwargs_task = get_some_kwargs(my_param='Additional info from kwargs')
    create_excel_task = create_excel()
    build_email_with_attachment_task = build_email_with_attachment('Email from Airflow')
    email_on_failure_task = email_on_failure()
    
    print_hello_task >> get_payload_task >> get_task_instance_task >> get_some_kwargs_task >> create_excel_task >> build_email_with_attachment_task >> email_on_failure_task


dag_instance = my_dag()
