import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from PIL import Image
import streamlit as st
from plotly.subplots import make_subplots
from config.db import engine
from lists import *

Grupo=st.selectbox("Select a Group:", (Grupos))
if Grupo=='GrupoA':
    Grupo=GrupoA
elif Grupo=='GrupoB':
    Grupo=GrupoB
elif Grupo=='GrupoC':
    Grupo=GrupoC
elif Grupo=='GrupoD':
    Grupo=GrupoD
elif Grupo=='GrupoE':
    Grupo=GrupoE
elif Grupo=='GrupoF':
    Grupo=GrupoF
elif Grupo=='GrupoG':
    Grupo=GrupoG
elif Grupo=='GrupoH':
    Grupo=GrupoH


Team=st.selectbox("Select a Team:", (Grupo))

def getlocal(FIFATeam):
    R1=f'''SELECT Year, Stage, `Home Team Name`, `Away Team Name`, `Home Team Goals`, `Away Team Goals`, `Half-time Home Goals`, `Half-time Away Goals`, `Home result`
    FROM matches
    WHERE `Home Team Name` = '{FIFATeam}'
    ;'''

    df=pd.read_sql(R1, engine)
    
    return df


def getvisit(FIFATeam):
    R1=f'''SELECT Year, Stage, `Home Team Name`, `Away Team Name`, `Home Team Goals`, `Away Team Goals`, `Half-time Home Goals`, `Half-time Away Goals`, `Home result`
    FROM matches
    WHERE `Away Team Name` = '{FIFATeam}'
    ;'''

    df=pd.read_sql(R1, engine)
    return df

df1=getlocal(FIFATeam=Team)
df2=getvisit(FIFATeam=Team)


tab1, tab2, tab3= st.tabs(['Local',"Visitante","Global"])
with tab1:
    '''### Como local:'''
    if df1.empty:
        f"Es la primera participación de {Team} en copas del mundo."
    else:
        G1=df1['Home Team Goals'].sum()
        G2=df1['Away Team Goals'].sum()
        G3=df1['Half-time Home Goals'].sum()
        G4=df1['Half-time Away Goals'].sum()
        partidos=df1['Year'].count()
        wins_local=df1[df1['Home result']=='Won']['Home result'].count()
        lost_local=df1[df1['Home result']=='Lost']['Home result'].count()
        tied_local=df1[df1['Home result']=='Tied']['Home result'].count()

        f"{Team} ha anotado {G1} goles y ha recibido {G3} goles, en {partidos} partidos."
        f"En el primer tiempo anotó {G3} goles y recibió {G4} goles."
        f"El {round((1-G3/G1)*100,1)}% de sus goles los hace en el segundo tiempo."
        f"El {round((1-G4/G2)*100,1)}% de goles recibidos son en el segundo tiempo."
        f"Ha ganado como local {wins_local} partidos, ha perdido {lost_local} y ha empatado {tied_local} partidos. Con una tasa de victorias del {round((wins_local/partidos)*100,1)}%"

with tab2:
    '''### Como visitante:'''
    if df2.empty:
        f"Es la primera participación de {Team} en copas del mundo."
    else:
        G5=df2['Home Team Goals'].sum()
        G6=df2['Away Team Goals'].sum()
        G7=df2['Half-time Home Goals'].sum()
        G8=df2['Half-time Away Goals'].sum()
        partidos_visit=df2['Year'].count()
        wins_visit=df2[df2['Home result']=='Lost']['Home result'].count() #Se pone como Lost porque al ser visitante, si ha perido el local, ha ganado el visitante.
        lost_visit=df2[df2['Home result']=='Won']['Home result'].count()
        tied_visit=df2[df2['Home result']=='Tied']['Home result'].count()
        f"{Team} ha anotado {G6} goles y ha recibido {G5} goles, en {partidos_visit} partidos."
        f"En el primer tiempo anotó {G8} goles y recibió {G7} goles."
        f"El {round((1-G8/G6)*100,1)}% de sus goles los hace en el segundo tiempo."
        f"El {round((1-G7/G5)*100,1)}% de goles recibidos son en el segundo tiempo."
        f"Ha ganado como visitante {wins_visit} partidos, ha perdido {lost_visit} y ha empatado {tied_visit} partidos. Con una tasa de victorias del {round((wins_visit/partidos_visit)*100,1)}%"

with tab3:
    '''### En todos los partidos de copa del mundo:'''
    if df1.empty:
        f"Es la primera participación de {Team} en copas del mundo."
    else:
        Anotados=G1+G6
        Recibidos=G2+G5
        Anotados1T=G3+G8
        Recibidos1T=G4+G7
        Partidos_totales=partidos+partidos_visit
        wins=wins_local+wins_visit
        lost=lost_local+lost_visit
        tied=tied_local+tied_visit

        f"{Team} ha anotado {Anotados} goles y ha recibido {Recibidos} goles, en {Partidos_totales} partidos."
        f"En el primer tiempo anotó {Anotados1T} goles y recibió {Recibidos1T} goles"
        f"El {round((1-Anotados1T/Anotados)*100,1)}% de sus goles los hace en el segundo tiempo ({Anotados-Anotados1T})."
        f"El {round((1-Recibidos1T/Recibidos)*100,1)}% de goles recibidos son en el segundo tiempo."
        f"Ha ganado {wins} partidos, ha perdido {lost} partidos y ha empatado {tied} partidos. Con una tasa de victorias del {round((wins/Partidos_totales)*100,1)}%."

        lista=df2['Home Team Name'].unique()
        Enfrentamientos=[]
        for i in lista:
            a=df2[df2['Home Team Name']==i]['Home Team Name'].count()
            Enfrentamientos.append(a)
       
        Rivales=pd.DataFrame(list(zip(lista,Enfrentamientos)), columns=['Rival', 'Enfrentamientos'])
        Rivales=Rivales.sort_values(["Enfrentamientos"], ascending=False)
        

        trace  = go.Bar(
                x=Rivales['Rival'].tolist(),
                y=Rivales['Enfrentamientos'].tolist(),
                showlegend = False
                )

        layout = go.Layout(                                    
                        xaxis_title='Rivales',
                        yaxis_title='Cantidad enfrentamientos'
                        )
        data = [trace]
        fig = go.Figure(data=data,layout = layout)
        st.plotly_chart(fig)