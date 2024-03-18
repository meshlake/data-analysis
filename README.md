# data-analysis

## requirements

Python 3.11.4

## If this is your first time using it, please create a virtual environment first and then install the dependencies.

## Local development environment

1. Create a virtual environment

```shell
python3 -m venv venv
```

2. Activate virtual environment

```shell
source venv/bin/activate
```

3. Install dependencies

```shell
pip3 install -r requirements.txt
```

## Prepare data

1. Environment variable configuration  
   Create a new .env file, refer to .env.example  
   Configure OPENAI_API_KEY

2. Prepare data  
   Create schema.sql in the /data/default directory  
   schema.sql is the table structure of the database  

   For example  

   CREATE TABLE Breeds (  
   breed_code VARCHAR(10) PRIMARY KEY ,  
   breed_name VARCHAR(80)  
   );  

   CREATE TABLE Charges (  
   charge_id INTEGER PRIMARY KEY ,  
   charge_type VARCHAR(10),  
   charge_amount DECIMAL(19,4)  
   );

   Create sql.json in the /data/default directory  
   sql.json is a combination of questions and sql to assist data analysis

   For example  

   [{  
   "query": "SELECT state FROM Owners INTERSECT SELECT state FROM Professionals",  
   "question": "Which states have both owners and professionals living there?",  
   }]

   Please generate according to the sample structure

3. Run

```shell
# Build data analysis resources, please wait patiently for the construction to complete
python3 main/build.py

# Open the command line dialog box, enter the question, get the answer, enter q to exit
python3 main/start.py
```
