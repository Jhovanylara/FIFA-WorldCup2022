import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from PIL import Image
import streamlit as st
from plotly.subplots import make_subplots
from db import engine
from lists import *
col1,col2,col3=st.columns(3)
with col2:
    st.image('https://raw.githubusercontent.com/Jhovanylara/FIFA-WorldCup2022/master/Images/vecteezy_mondial-fifa-world-cup-qatar-2022-official-logo-champion_8785666.jpg', width=200)

Grupo=st.selectbox("Select a Group:", (Grupos))
if Grupo=='GroupA':
    Grupo=GroupA
elif Grupo=='GroupB':
    Grupo=GroupB
elif Grupo=='GroupC':
    Grupo=GroupC
elif Grupo=='GroupD':
    Grupo=GroupD
elif Grupo=='GroupE':
    Grupo=GroupE
elif Grupo=='GroupF':
    Grupo=GroupF
elif Grupo=='GroupG':
    Grupo=GroupG
elif Grupo=='GroupH':
    Grupo=GroupH


Team=st.selectbox("Select a Team:", (Grupo))

def getlocal(FIFATeam):
    R1=f'''SELECT Year, Stage, `Home Team Name` AS `home_team`, `Away Team Name` AS `away_team`, `Home Team Goals` AS `home_score`, `Away Team Goals` AS `away_score`, `Half-time Home Goals`, `Half-time Away Goals`, `Home result` AS `home_result`, `MatchID`
    FROM matches
    WHERE `Home Team Name` = '{FIFATeam}'
    GROUP BY `MatchID`
    ;'''

    df=pd.read_sql(R1, engine)
    
    return df

def wcgetlocal(FIFATeam):
    R1=f'''SELECT `year`, `stage`, `home_team`, `away_team`, `home_score`, `away_score`, `outcome`, `winning_team`
    FROM wcmatches
    WHERE `home_team` = '{FIFATeam}'
    ;'''

    df=pd.read_sql(R1, engine)
    
    return df

def getvisit(FIFATeam):
    R1=f'''SELECT Year, Stage, `Home Team Name` AS `home_team`, `Away Team Name` AS `away_team`, `Home Team Goals` AS `home_score`, `Away Team Goals`  AS `away_score`, `Half-time Home Goals`, `Half-time Away Goals`, `Home result` AS `home_result`, `MatchID`
    FROM matches
    WHERE `Away Team Name` = '{FIFATeam}'
    GROUP BY `MatchID`
    ;'''

    df=pd.read_sql(R1, engine)
    return df

def wcgetvisit(FIFATeam):
    R1=f'''SELECT `year`, `stage`, `home_team`, `away_team`, `home_score`, `away_score`, `outcome`, `winning_team`
    FROM wcmatches
    WHERE `away_team` = '{FIFATeam}'
    ;'''

    df=pd.read_sql(R1, engine)
    
    return df

    

df1=getlocal(Team)
df2=getvisit(Team)
df3=wcgetlocal(Team)
df4=wcgetlocal(Team)


tab1, tab2, tab3= st.tabs(['Local',"Visitor","Global"])
with tab1:
    '''### As local:'''
    if df3.empty:
        f"This is the first appearance of {Team} in the World Cup."
    else:
        G1=df3['home_score'].sum()
        G2=df3['away_score'].sum()
        G1_1=df1['home_score'].sum()
        G2_1=df1['away_score'].sum()
        G3=df1['Half-time Home Goals'].sum()
        G4=df1['Half-time Away Goals'].sum()
        partidos=len(df3.axes[0])
        wins_local=df3.outcome.value_counts().H
        lost_local=df3.outcome.value_counts().A
        if 'D' in df3['outcome'].unique():
            tied_local=df3.outcome.value_counts().D
        else:
            tied_local=0

        f"{Team} has scored {G1} goals and conceded {G3} goals, in {partidos} matches."
        f"In the first half has scored {G3} goals and conceded {G4} goals."
        f"The {round((1-G3/G1_1)*100,1)}% of their goals are scored in the second half."
        f"The {round((1-G4/G2_1)*100,1)}% of conceded goalas are scored in the second half."
        f"Has won as local {wins_local} matches, has lost {lost_local} matches and has tied {tied_local} matches. With a {round((wins_local/partidos)*100,1)}% win rate."

        df1=df1.sort_values(by=['Year'])
        
with tab2:
    '''### As a visitor:'''
    if df3.empty:
        f"This is the first appearance of {Team} in the World Cup."
    else:
        G5=df4['home_score'].sum()
        G6=df4['away_score'].sum()
        G5_1=df2['home_score'].sum()
        G6_1=df2['away_score'].sum()
        G7=df2['Half-time Home Goals'].sum()
        G8=df2['Half-time Away Goals'].sum()
        partidos_visit=len(df2.axes[0])
        wins_visit=df4.outcome.value_counts().A #Se pone como Lost porque al ser visitante, si ha perido el local, ha ganado el visitante.
        lost_visit=df4.outcome.value_counts().H
        if 'D' in df4['outcome'].unique():
            tied_visit=df4.outcome.value_counts().D
        else:
            tied_visit=0
        f"{Team} has scored {G6} goals and conceded {G5} goals, in {partidos_visit} matches."
        f"In the first half has scored {G8} goals and conceded {G7} goals."
        f"The {round((1-G8/G6_1)*100,1)}% of their goals are scored in the second half."
        f"The {round((1-G7/G5_1)*100,1)}% of conceded goalas are scored in the second half."
        f"Has won as local {wins_visit} matches, has lost {lost_visit} and has tied {tied_visit} matches. With a {round((wins_visit/partidos_visit)*100,1)}% win rate."

with tab3:
    '''### In all World Cup matches:'''
    if df1.empty:
        f"This is the first appearance of {Team} in the World Cup."
    else:
        Anotados=G1+G6
        Anotados_2014=G1_1+G6_1
        Recibidos=G2+G5
        Recibidos_2014=G2_1+G5_1
        Anotados1T=G3+G8
        Recibidos1T=G4+G7
        Partidos_totales=partidos+partidos_visit
        wins=wins_local+wins_visit
        lost=lost_local+lost_visit
        tied=tied_local+tied_visit

        f"{Team} has scored {Anotados} goals and conceded {Recibidos} goals, in {Partidos_totales} matches."
        f"In the first half has scored  {Anotados1T} goals and conceded {Recibidos1T} goals"
        f"The {round((1-Anotados1T/Anotados_2014)*100,1)}% of their goals are scored in the second half."
        f"The {round((1-Recibidos1T/Recibidos_2014)*100,1)}% of conceded goals are scored in the second half."
        f"{Team} has won {wins} matches, has lost {lost} matches and has tied {tied}  matches. With a {round((wins/Partidos_totales)*100,1)}% win rate."

        lista1=df1['away_team'].unique()
        Enfrentamientos1=[]
        for i in lista1:
            a=df1['away_team'].str.count(i).sum()
            # a=df1[df1['away_team']==i]['away_team'].count()
            Enfrentamientos1.append(a)
       
        Rivales1=pd.DataFrame(list(zip(lista1,Enfrentamientos1)), columns=['Rival', 'Matches'])
        
        lista2=df2['home_team'].unique()
        Enfrentamientos2=[]
        for j in lista2:
            a=df2['home_team'].str.count(j).sum()
            #a=df2[df2['home_team']==i]['home_team'].count()
            Enfrentamientos2.append(a)
       
        Rivales2=pd.DataFrame(list(zip(lista2,Enfrentamientos2)), columns=['Rival', 'Matches'])
        
        Rivales=pd.concat([Rivales1, Rivales2], ignore_index=True)
        Rivales = Rivales.groupby('Rival', as_index=False).agg({'Matches':'sum'})
        Rivales=Rivales.sort_values(["Matches"], ascending=False)
        

        trace  = go.Bar(
                x=Rivales['Rival'].tolist()[:20],
                y=Rivales['Matches'].tolist(),
                showlegend = False
                )

        layout = go.Layout(       
                        title={'text': 'Top 20 rivals faced',
                                'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top' },                            
                        xaxis_title='Rivals',
                        yaxis_title='# of matches'
                        )
        data = [trace]
        fig = go.Figure(data=data,layout = layout)
        st.plotly_chart(fig)