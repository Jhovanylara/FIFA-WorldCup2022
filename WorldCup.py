import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from PIL import Image
import streamlit as st
from plotly.subplots import make_subplots
from config.db import engine
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
    R1=f'''SELECT Year, Stage, `Home Team Name` AS `home_team`, `Away Team Name` AS `away_team`, `Home Team Goals` AS `home_goals`, `Away Team Goals` AS `away_goals`, `Half-time Home Goals`, `Half-time Away Goals`, `Home result` AS `home_result`, `MatchID`
    FROM matches
    WHERE `Home Team Name` = '{FIFATeam}'
    GROUP BY `MatchID`
    ;'''

    df=pd.read_sql(R1, engine)
    
    return df


def getvisit(FIFATeam):
    R1=f'''SELECT Year, Stage, `Home Team Name` AS `home_team`, `Away Team Name` AS `away_team`, `Home Team Goals` AS `home_goals`, `Away Team Goals`  AS `away_goals`, `Half-time Home Goals`, `Half-time Away Goals`, `Home result` AS `home_result`, `MatchID`
    FROM matches
    WHERE `Away Team Name` = '{FIFATeam}'
    GROUP BY `MatchID`
    ;'''

    df=pd.read_sql(R1, engine)
    return df

df1=getlocal(Team)
df2=getvisit(Team) #FIFATeam=Team


tab1, tab2, tab3= st.tabs(['Local',"Visitor","Global"])
with tab1:
    '''### As local:'''
    if df1.empty:
        f"This is the first appearance of {Team} in the World Cup."
    else:
        G1=df1['home_goals'].sum()
        G2=df1['away_goals'].sum()
        G3=df1['Half-time Home Goals'].sum()
        G4=df1['Half-time Away Goals'].sum()
        partidos=len(df1.axes[0])
        wins_local=df1.home_result.value_counts().Won
        lost_local=df1.home_result.value_counts().Lost
        tied_local=df1.home_result.value_counts().Tied

        f"{Team} has scored {G1} goals and conceded {G3} goals, in {partidos} matches."
        f"In the first half has scored {G3} goals and conceded {G4} goals."
        f"The {round((1-G3/G1)*100,1)}% of their goals are scored in the second half."
        f"The {round((1-G4/G2)*100,1)}% of conceded goalas are scored in the second half."
        f"Has won as local {wins_local} matches, has lost {lost_local} matches and has tied {tied_local} matches. With a {round((wins_local/partidos)*100,1)}% win rate."

        df1=df1.sort_values(by=['Year'])
        
with tab2:
    '''### As a visitor:'''
    if df2.empty:
        f"This is the first appearance of {Team} in the World Cup."
    else:
        G5=df2['home_goals'].sum()
        G6=df2['away_goals'].sum()
        G7=df2['Half-time Home Goals'].sum()
        G8=df2['Half-time Away Goals'].sum()
        partidos_visit=len(df2.axes[0])
        wins_visit=df2.home_result.value_counts().Lost #Se pone como Lost porque al ser visitante, si ha perido el local, ha ganado el visitante.
        lost_visit=df2.home_result.value_counts().Won
        tied_visit=df2.home_result.value_counts().Tied
        f"{Team} has scored {G6} goals and conceded {G5} goals, in {partidos_visit} matches."
        f"In the first half has scored {G8} goals and conceded {G7} goals."
        f"The {round((1-G8/G6)*100,1)}% of their goals are scored in the second half."
        f"The {round((1-G7/G5)*100,1)}% of conceded goalas are scored in the second half."
        f"Has won as local {wins_visit} matches, has lost {lost_visit} and has tied {tied_visit} matches. With a {round((wins_visit/partidos_visit)*100,1)}% win rate."

with tab3:
    '''### In all World Cup matches:'''
    if df1.empty:
        f"This is the first appearance of {Team} in the World Cup."
    else:
        Anotados=G1+G6
        Recibidos=G2+G5
        Anotados1T=G3+G8
        Recibidos1T=G4+G7
        Partidos_totales=partidos+partidos_visit
        wins=wins_local+wins_visit
        lost=lost_local+lost_visit
        tied=tied_local+tied_visit

        f"{Team} has scored {Anotados} goals and conceded {Recibidos} goals, in {Partidos_totales} matches."
        f"In the first half has scored  {Anotados1T} goals and conceded {Recibidos1T} goals"
        f"The {round((1-Anotados1T/Anotados)*100,1)}% of their goals are scored in the second half ({Anotados-Anotados1T})."
        f"The {round((1-Recibidos1T/Recibidos)*100,1)}% of conceded goals are scored in the second half."
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
                        xaxis_title='Rivals',
                        yaxis_title='Matches'
                        )
        data = [trace]
        fig = go.Figure(data=data,layout = layout)
        st.plotly_chart(fig)