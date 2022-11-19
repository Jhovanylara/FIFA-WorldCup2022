from sqlalchemy import create_engine, MetaData
import pandas as pd

matchesURL='https://raw.githubusercontent.com/Jhovanylara/FIFA-WorldCup2022/master/config/WorldCupMatches.csv'
cupsURL='https://raw.githubusercontent.com/Jhovanylara/FIFA-WorldCup2022/master/config/WorldCups.csv'
matches=pd.read_csv(matchesURL)
cups=pd.read_csv(cupsURL)

matches=matches.dropna(how='all')
matches.drop(columns=['Win conditions','Attendance','City','Stadium','Referee','Assistant 1', 'Assistant 2', 'Home Team Initials','Away Team Initials'], inplace=True)
matches=matches.replace({'German DR':'Germany','Germany FR':'Germany'})

#Creamos una nueva columna con el resultado del local, (Win, tie o Lost)
def wins(row):
    if row['Home Team Goals']> row['Away Team Goals']:
        return 'Won'
    if row['Home Team Goals']==row['Away Team Goals']:
        return 'Tied'
    if row['Home Team Goals']< row['Away Team Goals']:
        return 'Lost'

matches['Home result']=matches.apply(lambda row: wins(row), axis=1)
#Creamos una base de datos SQL llamada 'FIFA'
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Uwovuqo_86@localhost/FIFA"

#Ingestamos nuestros dataframes con engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn, conn.begin(): 
    matches.to_sql("matches", conn, if_exists='append', index=False)
    cups.to_sql("cups", conn, if_exists='append', index=False)
    
meta= MetaData()