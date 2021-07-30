import argparse
import pyodbc
import pandas as pd

parser = argparse.ArgumentParser(description='Upload Data to Database through CSV')
parser.add_argument('--input_csv', type=str, help='CSV file path')
args = parser.parse_args()

server = 'irisdatabasemlops1.database.windows.net'
database = 'Irisdatabase'
username = 'irisadmin'
password = 'Batman@007'   
driver= '{ODBC Driver 17 for SQL Server}'

# Import CSV
data = pd.read_csv(args.input_csv)
df = pd.DataFrame(data, columns= ['SepalLengthCm','SepalWidthCm','PetalLengthCm', 'PetalWidthCm', 'Species'])

createTablesql = "IF Object_Id('dbo.IRISData', 'U') IS NOT NULL \
BEGIN \
DROP TABLE dbo.IRISData \
END \
CREATE TABLE dbo.IRISData \
(SepalLengthCm FLOAT NOT NULL,\
SepalWidthCm FLOAT NOT NULL,\
PetalLengthCm FLOAT NOT NULL,\
PetalWidthCm FLOAT NOT NULL,\
Species INT NOT NULL);"

with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute(createTablesql)
        for index, row in df.iterrows():
            cursor.execute('INSERT INTO dbo.IRISData (SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm, Species) VALUES (?,?,?,?,?)', row.SepalLengthCm, row.SepalWidthCm, row.PetalLengthCm, row.PetalWidthCm, row.Species)
        cursor.commit()