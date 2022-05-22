
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)
import datetime
pd.set_option('display.max_rows', None)
from plotly.subplots import make_subplots



#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

# Titre
st.title('Projet Covid 19 💊💉🤮')

# Subheader
st.subheader('Realise par : ELBOUHSSAINI Ahmed Walid , GAIO DOS SANTOS Lucas')
st.subheader('|Storytelling :')

"""
Durant cette presentation nous allons vous presenter l'historique covid 19 et son impact sur un peu partout dans le monde , ceci est la premiere fois ou nous utilisons la methode du Storytelling pour presenter des donnees

"""

st.markdown('---')

#-----------------------------------------------------------------------
url = 'https://raw.githubusercontent.com/walidelbou/Projet-Covid-B3/main/covid_19_data.csv'
data = pd.read_csv(url, delimiter=',')
data["Province/State"]= data["Province/State"].fillna('Unknown')
data[["Confirmed","Deaths","Recovered"]] =data[["Confirmed","Deaths","Recovered"]].astype(int)
data['Country/Region'] = data['Country/Region'].replace('Mainland China', 'China')
data['Active_case'] = data['Confirmed'] - data['Deaths'] - data['Recovered']
Data = data[data['ObservationDate'] == max(data['ObservationDate'])].reset_index()
Data_world = Data.groupby(["ObservationDate"])[["Confirmed","Active_case","Recovered","Deaths"]].sum().reset_index()


#------------------------------------------------------------------------
data_over_time= data.groupby(["ObservationDate"])[["Confirmed","Active_case","Recovered","Deaths"]].sum().reset_index().sort_values("ObservationDate",ascending=True).reset_index(drop=True)
st.header("Covid-19 dans le Monde - Representation graphique des donnees :")



col1, col2 = st.columns(2)

with col1:
    labels = ["Cas positifs","Soignes","Morts"]
values = Data_world.loc[0, ["Active_case","Recovered","Deaths"]]
fig = px.pie(Data_world, values=values, names=labels,color_discrete_sequence=['rgb(77,146,33)','rgb(69,144,185)','rgb(77,77,77)'],hole=0.7)
fig.update_layout(
    title='Cas totals : '+str(Data_world["Confirmed"][0]),
)
st.plotly_chart(fig)

with col2:
    st.header("")
    fig = go.Figure()
fig.add_trace(go.Scatter(x=data_over_time.index, y=data_over_time['Confirmed'],
                    mode='lines',
                    name='Confirmed cases'))


fig.update_layout(
    title='Evolution des cas confirmes dans le monde',
        template='plotly_white',
      yaxis_title="Cas confirmes",
    xaxis_title="Jours",

)

st.plotly_chart(fig, use_container_width=True)


#-----------------------------------------------------------------------

fig = go.Figure()


fig.add_trace(go.Scatter(x=data_over_time.index, y=data_over_time['Active_case'],
                    mode='lines',marker_color='yellow',
                    name='Active cases',line=dict( dash='dot')))

fig.update_layout(
    title='Evolution des cas actifs dans le monde',
        template='plotly_dark',
      yaxis_title="Cas actifs",
    xaxis_title="Jours",

)

st.plotly_chart(fig, use_container_width=True)

#-----------------------------------------------------------------------

fig = go.Figure()

fig.add_trace(go.Scatter(x=data_over_time.index, y=data_over_time['Recovered'],
                    mode='lines',
                    name='Recovered cases',marker_color='green'))

fig.update_layout(
    title='Evolution des cas soignes',
        template='plotly_white',
      yaxis_title="Cas soignes",
    xaxis_title="Jours",

)

st.plotly_chart(fig, use_container_width=True)


#--------------------------------------------------------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(x=data_over_time.index, y=data_over_time['Deaths'],name='Deaths',
                                   marker_color='pink',mode='lines',line=dict( dash='dot') ))

fig.update_layout(
    title='Evolution des morts',
        template='plotly_white',
     yaxis_title="Morts",
    xaxis_title="Jours",

)

st.plotly_chart(fig, use_container_width=True)

#---------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    fig = go.Figure(go.Bar(
            x=data_over_time['ObservationDate'],
            y=data_over_time['Confirmed'],
           ))
fig.update_layout(
    title='Cas confirmes chaque jour',
    template='plotly_white',
     xaxis_title="Cas confirmes",
    yaxis_title="Jours",
)
st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure(go.Bar(
            x=data_over_time['ObservationDate'],
            y=data_over_time['Active_case'],
    marker_color='rgb(253,187,132)'
           ))
fig.update_layout(
    title='Cas actifs chaque jour',
    template='plotly_dark',
     xaxis_title="Cas actifs",
    yaxis_title="Jours",
)
fig.show()
st.plotly_chart(fig, use_container_width=True)

with col3:
    st.header("")
    fig = go.Figure(go.Bar(
            x=data_over_time['ObservationDate'],
            y=data_over_time['Recovered'],
    marker_color='rgb(178,24,43)'
           ))
fig.update_layout(
    title='Cas soignes chaque jour',
    template='plotly_white',
     xaxis_title="Cas soignes",
    yaxis_title="Jours",
)
fig.show()
st.plotly_chart(fig, use_container_width=True)


fig = go.Figure(go.Bar(
            x=data_over_time['ObservationDate'],
            y=data_over_time['Deaths'],
    marker_color='rgb(13,48,100)'
           ))
fig.update_layout(
    title='Morts chaque jour',
    template='plotly_white',
     xaxis_title="Morts",
    yaxis_title="Jours",
)
st.plotly_chart(fig, use_container_width=True)

# cas confirmes dans chaque pays
Data_per_country = Data.groupby(["Country/Region"])["Confirmed","Active_case","Recovered","Deaths"].sum().reset_index().sort_values("Confirmed",ascending=False).reset_index(drop=True)

headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'

fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Pays</b>','<b>Cas confirmes</b>'],
    line_color='darkslategray',
    fill_color=headerColor,
    align=['left','center'],
      
    font=dict(color='white', size=12)
  ),
  cells=dict(
    values=[
      Data_per_country['Country/Region'],
      Data_per_country['Confirmed'],
      ],
    line_color='darkslategray',
    # 2-D list of colors for alternating rows
    fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*len(Data_per_country)],
    align = ['left', 'center'],
    font = dict(color = 'darkslategray', size = 11)
    ))
])
fig.update_layout(
    title='Cas confirmes dans chaque Pays',
)
st.plotly_chart(fig, use_container_width=True)

fig = go.Figure(go.Bar(
            x=Data_per_country['Confirmed'],
            y=Data_per_country['Country/Region'],
            orientation='h'))
fig.update_layout(
    title='Cas confirmes dans chaque pays',
    template='plotly_white',
     xaxis_title="Cas confirmes",
    yaxis_title="Pays",
)
st.plotly_chart(fig, use_container_width=True)


fig = go.Figure(go.Bar(
            x=Data_per_country['Active_case'],
            y=Data_per_country['Country/Region'],
            orientation='h',
            marker_color='#DC3912',))
fig.update_layout(
    title='Cas actifs dans chaque pays',
    template='plotly_white',
    xaxis_title="Cas actifs",
    yaxis_title="Pays",
)
st.plotly_chart(fig, use_container_width=True)

fig = go.Figure(go.Bar(
            x=Data_per_country['Recovered'],
            y=Data_per_country['Country/Region'],
            orientation='h',
            marker_color='#2CA02C',))
fig.update_layout(
    title='Cas soignes dans chaque pays',
    template='plotly_white',
     xaxis_title="Cas soignes",
    yaxis_title="Pays",
)
st.plotly_chart(fig, use_container_width=True)

fig = go.Figure(go.Bar(
            x=Data_per_country['Deaths'],
            y=Data_per_country['Country/Region'],
            orientation='h',
            marker_color='black',))
fig.update_layout(
    title='Morts dans chaque pays',
    template='plotly_white',
    xaxis_title="Morts",
    yaxis_title="Pays",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader('Un peu de Cartographie 😉')
fig = px.choropleth(Data_per_country, locations=Data_per_country['Country/Region'],
                    color=Data_per_country['Confirmed'],locationmode='country names', 
                    hover_name=Data_per_country['Country/Region'], 
                    color_continuous_scale=px.colors.sequential.Tealgrn,template='plotly_dark', )
fig.update_layout(
    title='Cas confirmes dans chaque pays',
)
st.plotly_chart(fig, use_container_width=True)

fig = px.choropleth(Data_per_country, locations=Data_per_country['Country/Region'],
                    color=Data_per_country['Active_case'],locationmode='country names', 
                    hover_name=Data_per_country['Country/Region'], 
                    color_continuous_scale=px.colors.sequential.Tealgrn,template='plotly_white', )
fig.update_layout(
    title='Cas actifs dans chaque pays',
)
st.plotly_chart(fig, use_container_width=True)

fig = px.choropleth(Data_per_country, locations=Data_per_country['Country/Region'],
                    color=Data_per_country['Recovered'],locationmode='country names', 
                    hover_name=Data_per_country['Country/Region'], 
                    color_continuous_scale=px.colors.sequential.Tealgrn,template='plotly_white', )
fig.update_layout(
    title='Cas soignes dans chaque pays',
)
st.plotly_chart(fig, use_container_width=True)

fig = px.choropleth(Data_per_country, locations=Data_per_country['Country/Region'],
                    color=Data_per_country['Deaths'],locationmode='country names', 
                    hover_name=Data_per_country['Country/Region'], 
                    color_continuous_scale=px.colors.sequential.Tealgrn,template='plotly_dark', )
fig.update_layout(
    title='Morts dans chaque pays',
)
st.plotly_chart(fig, use_container_width=True)

data_per_country = data.groupby(["Country/Region","ObservationDate"])[["Confirmed","Active_case","Recovered","Deaths"]].sum().reset_index().sort_values("ObservationDate",ascending=True).reset_index(drop=True)

fig = px.choropleth(data_per_country, locations=data_per_country['Country/Region'],
                    color=data_per_country['Confirmed'],locationmode='country names', 
                    hover_name=data_per_country['Country/Region'], 
                    color_continuous_scale=px.colors.sequential.deep,
                    animation_frame="ObservationDate")
fig.update_layout(

    title='Evolution des cas confirmes dans chaque pays',
)
st.plotly_chart(fig, use_container_width=True)


fig = px.choropleth(data_per_country, locations=data_per_country['Country/Region'],
                    color=data_per_country['Recovered'],locationmode='country names', 
                    hover_name=data_per_country['Country/Region'], 
                    color_continuous_scale=px.colors.sequential.deep,
                    animation_frame="ObservationDate")
fig.update_layout(
    title='Evolution des cas soignes dans chaque pays',
)
st.plotly_chart(fig, use_container_width=True)


fig = px.choropleth(data_per_country, locations=data_per_country['Country/Region'],
                    color=data_per_country['Deaths'],locationmode='country names', 
                    hover_name=data_per_country['Country/Region'], 
                    color_continuous_scale=px.colors.sequential.Tealgrn,
                    animation_frame="ObservationDate")
fig.update_layout(
    title='Evolution des morts dans chaque pays',
    template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)


fig = go.Figure(data=[go.Bar(
            x=Data_per_country['Country/Region'][0:10], y=Data_per_country['Confirmed'][0:10],
            text=Data_per_country['Confirmed'][0:10],
            textposition='auto',
            marker_color='black',
            

        )])
fig.update_layout(
    title='Top 10 des pays infectes',
    xaxis_title="Pays",
    yaxis_title="Cas confirmes",
        template='plotly_white'

)
st.plotly_chart(fig, use_container_width=True)


fig = go.Figure(data=[go.Scatter(
    x=Data_per_country['Country/Region'][0:10],
    y=Data_per_country['Confirmed'][0:10],
    mode='markers',
    
    marker=dict(
        color=100+np.random.randn(500),
        size=(Data_per_country['Confirmed'][0:10]/25000),
        showscale=True
        )
)])

fig.update_layout(
    title='Top 10 des pays infectes',
    xaxis_title="Pays",
    yaxis_title="Cas confirmes",
    template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)

Recovered_per_country = Data.groupby(["Country/Region"])["Recovered"].sum().reset_index().sort_values("Recovered",ascending=False).reset_index(drop=True)



fig = go.Figure(data=[go.Bar(
            x=Recovered_per_country['Country/Region'][0:10], y=Recovered_per_country['Recovered'][0:10],
            text=Recovered_per_country['Recovered'][0:10],
            textposition='auto',
            marker_color='green',

        )])
fig.update_layout(
    title='Top 10 des pays infectes',
    xaxis_title="Pays",
    yaxis_title="Cas soignes",
    template='plotly_white'
)
st.plotly_chart(fig, use_container_width=True)


fig = go.Figure(data=[go.Scatter(
    x=Recovered_per_country['Country/Region'][0:10],
    y=Recovered_per_country['Recovered'][0:10],
    mode='markers',
    marker=dict(
        color=100+np.random.randn(500),
        size=(Data_per_country['Recovered'][0:10]/20000),
        showscale=True
        )
)])
fig.update_layout(
    title='Top 10 des pays infectes',
    xaxis_title="Pays",
    yaxis_title="Cas soignes",
    template='plotly_white'

)
st.plotly_chart(fig, use_container_width=True)

Deaths_per_country = Data.groupby(["Country/Region"])["Deaths"].sum().reset_index().sort_values("Deaths",ascending=False).reset_index(drop=True)





fig = go.Figure(data=[go.Bar(
            x=Deaths_per_country['Country/Region'][0:10], y=Deaths_per_country['Deaths'][0:10],
            text=Deaths_per_country['Deaths'][0:10],
            textposition='auto',
            marker_color='black'

        )])
fig.update_layout(
    title='Top 10 des pays infectes',
    xaxis_title="Pays",
    yaxis_title="Morts",
        template='plotly_white'

)
st.plotly_chart(fig, use_container_width=True)


fig = go.Figure(data=[go.Scatter(
    x=Deaths_per_country['Country/Region'][0:10],
    y=Deaths_per_country['Deaths'][0:10],
    mode='markers',
    marker=dict(
        color=[145, 140, 135, 130, 125, 120,115,110,105,100],
        size=Deaths_per_country['Deaths'][0:10]/1000,
        showscale=True
        )
)])
fig.update_layout(
    title='Top 10 des pays infectes',
    xaxis_title="Pays",
    yaxis_title="Morts",
        template='plotly_white'
)
st.plotly_chart(fig, use_container_width=True)


#--------------------- FRANCE ----------------------------------

st.header("Covid-19 en France 💙🤍💗:")
Data_france = data [(data['Country/Region'] == 'France') ].reset_index(drop=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=Data_france['ObservationDate'], y=Data_france['Confirmed'],
                    mode='lines',
                    name='Confirmed cases'))

fig.add_trace(go.Scatter(x=Data_france['ObservationDate'], y=Data_france['Active_case'],
                    mode='lines',
                    name='Active cases',line=dict( dash='dot')))
fig.add_trace(go.Scatter(x=Data_france['ObservationDate'], y=Data_france['Deaths'],name='Deaths',
                                   marker_color='black',mode='lines',line=dict( dash='dot') ))
fig.add_trace(go.Scatter(x=Data_france['ObservationDate'], y=Data_france['Recovered'],
                    mode='lines',
                    name='Recovered cases',marker_color='green'))
fig.update_layout(
    title='Evolution des cas en France',
        template='plotly_dark'

)

st.plotly_chart(fig, use_container_width=True)

Data_france_last = Data_france[Data_france['ObservationDate'] == max(Data_france['ObservationDate'])].reset_index()
Data_france_last

colors = ['rgb(2,58,88)','rgb(65,171,93)', 'rgb(127,0,0)']
labels = ["Active cases","Recovered","Deaths"]
values = Data_france_last.loc[0, ["Active_case","Recovered","Deaths"]]

fig = go.Figure(data=[go.Pie(labels=labels,
                             values=values)])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
st.plotly_chart(fig, use_container_width=True)


#----------------------- CHINE --------------------------------
st.header("Covid-19 en Chine 🐉💛💖:")
Data_China = data [(data['Country/Region'] == 'China') ].reset_index(drop=True)


Data_china_last = Data_China[Data_China['ObservationDate'] == max(Data_China['ObservationDate'])].reset_index()
Data_china_last.head()
Data_china_per_state= Data_china_last.groupby(["Province/State"])["Confirmed","Active_case","Recovered","Deaths"].sum().reset_index().sort_values("Confirmed",ascending=False).reset_index(drop=True)
fig = go.Figure(go.Bar(
            x=Data_china_per_state['Active_case'],
            y=Data_china_per_state['Province/State'],
            orientation='h',
            marker_color='#DC3912',))
fig.update_layout(
    title='Cas actifs dans chaque region',
    template='plotly_white',
    xaxis_title="Cas actifs",
    yaxis_title="Region",
)
st.plotly_chart(fig, use_container_width=True)

fig = go.Figure(go.Bar(
            x=Data_china_per_state['Recovered'],
            y=Data_china_per_state['Province/State'],
            orientation='h',
            marker_color='green',))
fig.update_layout(
    title='Cas soignes dans chaque region',
    template='plotly_white',
    xaxis_title="Cas soignes",
    yaxis_title="Region",
)
st.plotly_chart(fig, use_container_width=True)

Data_china_total= Data_china_last.groupby(["Country/Region"])["Confirmed","Deaths","Recovered","Active_case"].sum().reset_index().reset_index(drop=True)

labels = ["Cas Actifs","Cas soignes","Morts"]
values = Data_china_total.loc[0, ["Active_case","Recovered","Deaths"]]
df = px.data.tips()
fig = px.pie(Data_china_total, values=values, names=labels, color_discrete_sequence=['green','royalblue','darkblue'], hole=0.5)
fig.update_layout(
    title='Cas totals en chine : ',
)
st.plotly_chart(fig, use_container_width=True)

Data_china_op= Data_China.groupby(["ObservationDate","Country/Region"])["Confirmed","Deaths","Recovered","Active_case"].sum().reset_index().reset_index(drop=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=Data_china_op['ObservationDate'], y=Data_china_op['Confirmed'],
                    mode='lines',
                    name='Cas confirmes'))


fig.add_trace(go.Scatter(x=Data_china_op['ObservationDate'], y=Data_china_op['Active_case'],
                    mode='lines',
                    name='Cas actifs',line=dict( dash='dot')))
fig.add_trace(go.Scatter(x=Data_china_op['ObservationDate'], y=Data_china_op['Deaths'],name='Deaths',
                                   marker_color='black',mode='lines',line=dict( dash='dot') ))
fig.add_trace(go.Scatter(x=Data_china_op['ObservationDate'], y=Data_china_op['Recovered'],
                    mode='lines',
                    name='Cas soignes',marker_color='green'))

fig.update_layout(
    title='Evolution des cas en chine',
        template='plotly_white'

)

st.plotly_chart(fig, use_container_width=True)


#--------------------------------- Italie --------------------------
st.header("Covid-19 en Italie 🍕:")

Data_Italy = data [(data['Country/Region'] == 'Italy') ].reset_index(drop=True)
Data_italy_last = Data_Italy[Data_Italy['ObservationDate'] == max(Data_Italy['ObservationDate'])].reset_index()
Data_italy= Data_italy_last.groupby(["Country/Region"])["Confirmed","Deaths","Recovered","Active_case"].sum().reset_index().reset_index(drop=True)

labels = ["Cas actifs","Cas soignes","Morts"]
values = Data_italy.loc[0, ["Active_case","Recovered","Deaths"]]
df = px.data.tips()
fig = px.pie(Data_italy, values=values, names=labels, color_discrete_sequence=['royalblue','green','darkblue'], hole=0.5)
fig.update_layout(
    title='Cas totals en italie : '+str(Data_italy["Confirmed"][0]),
)
st.plotly_chart(fig, use_container_width=True)



Data_italy_per_state= Data_italy_last.groupby(["Province/State"])["Confirmed","Deaths","Recovered","Active_case"].sum().reset_index().sort_values("Confirmed",ascending=False).reset_index(drop=True)

fig = px.pie(Data_italy_per_state, values=Data_italy_per_state['Confirmed'], names=Data_italy_per_state['Province/State'],
             title='Cas confirmes en Italie',
            hole=.5)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(Data_italy_per_state, values=Data_italy_per_state['Recovered'], names=Data_italy_per_state['Province/State'],
             title='Cas soignes en Italie',
            )
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(Data_italy_per_state, values=Data_italy_per_state['Deaths'], names=Data_italy_per_state['Province/State'],
             
             title='Morts en italie',
            )
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)



#------------------------------- USA --------------------------------------
st.header("Covid-19 en USA 🍔:")

Data_US = data [(data['Country/Region'] == 'US') ].reset_index(drop=True)
Data_us_last = Data_US[Data_US['ObservationDate'] == max(Data_US['ObservationDate'])].reset_index()
Data_us_total= Data_us_last.groupby(["Country/Region"])["Confirmed","Deaths","Recovered","Active_case"].sum().reset_index().reset_index(drop=True)

Data_us_per_state= Data_us_last.groupby(["Province/State"])["Confirmed","Active_case","Deaths"].sum().reset_index().sort_values("Confirmed",ascending=False).reset_index(drop=True)

fig = px.pie(Data_us_per_state, values=Data_us_per_state['Confirmed'], names=Data_us_per_state['Province/State'],
             title='Cas confirmes aux USA:',
            hole=.2)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(Data_us_per_state, values=Data_us_per_state['Active_case'], names=Data_us_per_state['Province/State'],
             title='Cas actifs aux USA:',
            hole=.2)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(Data_us_per_state, values=Data_us_per_state['Deaths'], names=Data_us_per_state['Province/State'],
             title='Morts aux USA:',
            hole=.2)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

Data_US_op= Data_US.groupby(["ObservationDate","Country/Region"])["Confirmed","Deaths","Recovered","Active_case"].sum().reset_index().reset_index(drop=True)

fig = go.Figure()

fig.add_trace(go.Scatter(x=Data_US_op.index, y=Data_US_op['Recovered'],
                    mode='lines',
                    name='Recovered cases',marker_color='green'))

fig.update_layout(
    title='Evolution des cas soignes aux USA :',
        template='plotly_white'

)

st.plotly_chart(fig, use_container_width=True)


fig = go.Figure()

fig.add_trace(go.Scatter(x=Data_US_op.index, y=Data_US_op['Deaths'],name='Deaths',
                                   marker_color='white',mode='lines',line=dict( dash='dot') ))

fig.update_layout(
    title='Evolution des morts aux USA :',
        template='plotly_dark'

)

st.plotly_chart(fig, use_container_width=True)

#----------------- ESPAGNE --------------------------
st.header("Covid-19 en Espagne 🐂🍺:")

Data_Spain = data [(data['Country/Region'] == 'Spain') ].reset_index(drop=True)
Data_spain = Data_Spain[Data_Spain['ObservationDate'] == max(Data_Spain['ObservationDate'])].reset_index()
Data_spain_last= Data_spain.groupby(["Country/Region"])["Confirmed","Deaths","Recovered","Active_case"].sum().reset_index().reset_index(drop=True)

labels = ["Cas actifs","Cas soignes","Morts"]
values = Data_spain_last.loc[0, ["Active_case","Recovered","Deaths"]]
df = px.data.tips()
fig = px.pie(Data_spain_last, values=values, names=labels, color_discrete_sequence=['royalblue','green','darkblue'], hole=0.5)
fig.update_layout(
    title='Cas totals en espagne : '+str(Data_spain_last["Confirmed"][0]),
)
st.plotly_chart(fig, use_container_width=True)

Data_spain_per_state= Data_spain.groupby(["Province/State"])["Confirmed","Deaths","Recovered","Active_case"].sum().reset_index().sort_values("Confirmed",ascending=False).reset_index(drop=True)

fig = px.treemap(Data_spain_per_state, path=['Province/State'], values=Data_spain_per_state['Confirmed'], height=700,
                 title='Cas confirmes en Espagne', color_discrete_sequence = px.colors.qualitative.Dark2)
fig.data[0].textinfo = 'label+text+value'
st.plotly_chart(fig, use_container_width=True)

fig = px.treemap(Data_spain_per_state, path=['Province/State'], values=Data_spain_per_state['Recovered'], height=700,
                 title='Cas soignes en Espagne', color_discrete_sequence = px.colors.qualitative.Dark2)
fig.data[0].textinfo = 'label+text+value'
st.plotly_chart(fig, use_container_width=True)

fig = px.treemap(Data_spain_per_state, path=['Province/State'], values=Data_spain_per_state['Active_case'], height=700,
                 title='Cas actifs en Espagne :', color_discrete_sequence = px.colors.sequential.deep)
fig.data[0].textinfo = 'label+text+value'
st.plotly_chart(fig, use_container_width=True)

fig = px.treemap(Data_spain_per_state, path=['Province/State'], values=Data_spain_per_state['Deaths'], height=700,
                 title='Morts en Espagne :', color_discrete_sequence = px.colors.sequential.deep)
fig.data[0].textinfo = 'label+text+value'
st.plotly_chart(fig, use_container_width=True)



#----------------------- Comparaison entre differents pays ( apres 3 semaines du premier cas detecte)----------
st.header("Et si on comparait entre les pays ? 🤔:")

def getDate(date,weeks):

    datein = datetime.datetime.strptime(date, "%m/%d/%Y")
    threeWeeks = datetime.timedelta(weeks =weeks)
    datefinal = (datein + threeWeeks)
    
    return(datefinal.strftime('%m/%d/%Y'))

Data_Ger = data [(data['Country/Region'] == 'Germany') ].reset_index(drop=True)
Data_france_after_twoweeks = Data_france[ Data_france['ObservationDate'] < getDate(min(Data_france['ObservationDate']),2) ].reset_index()
Data_italy_after_twoweeks = Data_Italy[Data_Italy['ObservationDate'] < getDate(min(Data_Italy['ObservationDate']),2) ].reset_index()
Data_spain_after_twoweeks = Data_Spain[Data_Spain['ObservationDate'] < getDate(min(Data_Spain['ObservationDate']),2) ].reset_index()
Data_germany_after_twoweeks = Data_Ger[Data_Ger['ObservationDate'] < getDate(min(Data_Ger['ObservationDate']),2) ].reset_index()

fig = make_subplots(rows=2, cols=2,
                    specs=[[{"secondary_y": True}, {"secondary_y": True}],
                           [{"secondary_y": True}, {"secondary_y": True}]],
                   subplot_titles=("France : "+str(Data_france_after_twoweeks['Confirmed'].max()),
                                   " Italie : "+ str(Data_italy_after_twoweeks['Confirmed'].max()),
                                   "  Espagne : "+ str(Data_spain_after_twoweeks['Confirmed'].max()),
                                   " Allemagne : "+ str(Data_germany_after_twoweeks['Confirmed'].max())
                                  ))

# Top left
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_france_after_twoweeks)+1)), y=Data_france_after_twoweeks['Confirmed'], 
                name="Cas confirmes en France"),row=1, col=1, secondary_y=False)


# Top right
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_italy_after_twoweeks)+1)), y=Data_italy_after_twoweeks['Confirmed'], 
               name="Cas confirmes en Italie"), row=1, col=2, secondary_y=False,
)

# Bottom left
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_spain_after_twoweeks)+1)), y=Data_spain_after_twoweeks['Confirmed'], 
               name="Cas confirmes en Espagne"),row=2, col=1, secondary_y=False,
)


# Bottom right
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_germany_after_twoweeks)+1)), y=Data_germany_after_twoweeks['Confirmed'], 
               name="Cas confirmes en Allemagne"),row=2, col=2, secondary_y=False,
)
# Update xaxis properties
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")

# Update yaxis properties
fig.update_yaxes(title_text="Cas confirmes")
fig.update_yaxes(title_text="Cas confirmes")
fig.update_yaxes(title_text="Cas confirmes")
fig.update_yaxes(title_text="Cas confirmes")

fig.update_layout(
    title_text="Cas confirmes dans les deux premieres semaines",
    width=800,
)

st.plotly_chart(fig, use_container_width=True)


fig = make_subplots(rows=2, cols=2,
                    specs=[[{"secondary_y": True}, {"secondary_y": True}],
                           [{"secondary_y": True}, {"secondary_y": True}]],
                   subplot_titles=("France : "+str(Data_france_after_twoweeks['Recovered'].max()),
                                   " Italie : "+ str(Data_italy_after_twoweeks['Recovered'].max()),
                                   "  Espagne : "+ str(Data_spain_after_twoweeks['Recovered'].max()),
                                   " Allemagne : "+ str(Data_germany_after_twoweeks['Recovered'].max())
                                  ))

# Top left
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_france_after_twoweeks)+1)), y=Data_france_after_twoweeks['Recovered'], 
                name="Cas confirmes en France"),row=1, col=1, secondary_y=False)


# Top right
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_italy_after_twoweeks)+1)), y=Data_italy_after_twoweeks['Recovered'], 
               name="Cas confirmes en Italie"), row=1, col=2, secondary_y=False,
)

# Bottom left
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_spain_after_twoweeks)+1)), y=Data_spain_after_twoweeks['Recovered'], 
               name="Cas confirmes en Espagne"),row=2, col=1, secondary_y=False,
)


# Bottom right
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_germany_after_twoweeks)+1)), y=Data_germany_after_twoweeks['Recovered'], 
               name="Cas confirmes en Allemagne"),row=2, col=2, secondary_y=False,
)
# Update xaxis properties
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")

# Update yaxis properties
fig.update_yaxes(title_text="Cas soignes")
fig.update_yaxes(title_text="Cas soignes")
fig.update_yaxes(title_text="Cas soignes")
fig.update_yaxes(title_text="Cas soignes")

fig.update_layout(
    title_text="Cas Soignes dans les deux premieres semaines",
    width=800,
)

st.plotly_chart(fig, use_container_width=True)


fig = make_subplots(rows=2, cols=2,
                    specs=[[{"secondary_y": True}, {"secondary_y": True}],
                           [{"secondary_y": True}, {"secondary_y": True}]],
                   subplot_titles=("France : "+str(Data_france_after_twoweeks['Deaths'].max()),
                                   " Italie : "+ str(Data_italy_after_twoweeks['Deaths'].max()),
                                   "  Espagne : "+ str(Data_spain_after_twoweeks['Deaths'].max()),
                                   " Allemagne : "+ str(Data_germany_after_twoweeks['Deaths'].max())
                                  ))

# Top left
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_france_after_twoweeks)+1)), y=Data_france_after_twoweeks['Deaths'], 
                name="Cas morts en France"),row=1, col=1, secondary_y=False)


# Top right
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_italy_after_twoweeks)+1)), y=Data_italy_after_twoweeks['Deaths'], 
               name="Cas morts en Italie"), row=1, col=2, secondary_y=False,
)

# Bottom left
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_spain_after_twoweeks)+1)), y=Data_spain_after_twoweeks['Deaths'], 
               name="Cas morts en Espagne"),row=2, col=1, secondary_y=False,
)


# Bottom right
fig.add_trace(
    go.Scatter(x=list(range(1,len(Data_germany_after_twoweeks)+1)), y=Data_germany_after_twoweeks['Deaths'], 
               name="Cas morts en Allemagne"),row=2, col=2, secondary_y=False,
)
# Update xaxis properties
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")
fig.update_xaxes(title_text="Jours")

# Update yaxis properties
fig.update_yaxes(title_text="Cas morts")
fig.update_yaxes(title_text="Cas morts")
fig.update_yaxes(title_text="Cas morts")
fig.update_yaxes(title_text="Cas morts")

fig.update_layout(
    title_text="Cas morts dans les deux premieres semaines",
    width=800,
)

st.plotly_chart(fig, use_container_width=True)






#------------------------------------------------- quelques modeles de prediction / Machine Learning -----------------

#---------- Regression lineaire -----------------------
st.header("Prediction via regression lineaire 🔮🧙‍♂️")

data["ObservationDate"] = pd.to_datetime(data["ObservationDate"])
datewise = data.groupby(["ObservationDate"]).agg({"Confirmed":'sum',"Recovered":'sum',"Deaths":'sum'})
datewise["Days Since"] = datewise.index-datewise.index[0]
datewise["Days Since"] = datewise["Days Since"].dt.days

train_ml=datewise.iloc[:int(datewise.shape[0]*0.95)]
valid_ml=datewise.iloc[int(datewise.shape[0]*0.95):]
model_scores=[]

from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression(normalize = True)

lin_reg.fit(np.array(train_ml["Days Since"]).reshape(-1,1),np.array(train_ml["Confirmed"]).reshape(-1,1))

prediction_valid_linreg = lin_reg.predict(np.array(valid_ml["Days Since"]).reshape(-1,1))

from sklearn.metrics import mean_squared_error
model_scores.append(np.sqrt(mean_squared_error(valid_ml["Confirmed"],prediction_valid_linreg)))

fig = plt.figure(figsize=(11,6))
prediction_linreg=lin_reg.predict(np.array(datewise["Days Since"]).reshape(-1,1))
plt.plot(datewise["Confirmed"],label="Cas actuellement confirmes")
plt.plot(datewise.index,prediction_linreg, linestyle='--',label="Cas predits via la regression",color='red')
plt.xlabel('Date')
plt.ylabel('Cas confirmes')
plt.title("Cas confirmes utilisant la regression lineaire")
plt.xticks(rotation=90)
st.plotly_chart(fig, use_container_width=True)


#--------------------------- SVM -------------------------
st.header("Prediction via SVM 🔮🧙‍♂️")


train_ml = datewise.iloc[:int(datewise.shape[0]*0.95)]
valid_ml = datewise.iloc[int(datewise.shape[0]*0.95):]
from sklearn.svm import SVR
svm = SVR(C = 1, degree = 5, kernel = 'poly', epsilon = 0.01) # initialisation du modele
svm.fit(np.array(train_ml["Days Since"]).reshape(-1,1), np.array(train_ml["Confirmed"]).reshape(-1,1))
prediction_valid_svm = svm.predict(np.array(valid_ml["Days Since"]).reshape(-1,1))
model_scores.append(np.sqrt(mean_squared_error(valid_ml["Confirmed"], prediction_valid_svm)))

fig = plt.figure(figsize = (11,6))
prediction_svm = svm.predict(np.array(datewise["Days Since"]).reshape(-1,1))
plt.plot(datewise["Confirmed"],label = "Cas de train confirmes",linewidth = 3)
plt.plot(datewise.index,prediction_svm, linestyle = '--',label = "SVR",color = 'red')
plt.xlabel('Date')
plt.ylabel('Cas confirmes')
plt.title("Cas confirmes utilisant la prediction du SVM")
plt.xticks(rotation = 90)
st.plotly_chart(fig, use_container_width=True)


st.header("Merci pour votre attention ✨")
