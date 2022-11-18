from sqlalchemy import create_engine, MetaData
import pandas as pd

matches=pd.read_csv('WorldCupMatches.csv')
cups=pd.read_csv('WorldCups.csv')

matches=matches.dropna(how='all')
matches.drop(columns=['Win conditions','Attendance','City','Stadium','Referee','Assistant 1', 'Assistant 2', 'Home Team Initials','Away Team Initials'], inplace=True)

#Creamos una base de datos SQL llamada 'FIFA'
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Uwovuqo_86@localhost/FIFA"

#Ingestamos nuestros dataframes con engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn, conn.begin(): 
    matches.to_sql("matches", conn, if_exists='append', index=False)
    cups.to_sql("cups", conn, if_exists='append', index=False)
    
meta= MetaData()