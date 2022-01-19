import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#load data
filePath = 'MIBOYS20220101.csv'
dataURL = 'https://github.com/Frederick-Jerome-Thompson/RankingMI/blob/main/MIBOYS20220101v2.csv'
allScores = pd.read_csv(dataURL)


#main chart
avgScores = allScores[['age','score']].groupby('age').mean('score')
dist = allScores['score']
dist_age = allScores[allScores['age']==2010]['score']

fig, ax = plt.subplots()
fig.set_figwidth(15)
fig.set_figheight(5)

dist.plot.hist(density=False, ax=ax)
dist_age.plot.hist(density=False, ax=ax)


min_ylim, max_ylim = plt.ylim()
for year in avgScores.index:
  plt.axvline(avgScores['score'][year],color='red')
  if year == 2012:
    plt.text(avgScores['score'][year]*.95, max_ylim*1.05, year)
  elif year == 2004:
    plt.text(avgScores['score'][year]*.98, max_ylim*1.05, year)
  else:
    plt.text(avgScores['score'][year]*.98, max_ylim*1.1, year)




ax.set_ylabel('Teams')
ax.set_xlabel('Goals')
#ax.grid(axis='y')
ax.set_facecolor('#d8dcd6')

st.pyplot(fig)

# #average score table
# st.table(avgScores)

st.title('Ranking Michigan Soccer')
st.caption(allScores['update'][0])

#year input

bYear = st.slider('Birth Year', 2003,2012)

# b year analysis
dist_byear = allScores[allScores['age']==bYear]['ageAdjScore']
fig, ax = plt.subplots()
dist_byear.plot.kde(ax=ax, legend=False, title='Goal Difference: %s' % bYear)
dist_byear.plot.hist(density=True, ax=ax)
ax.set_ylabel('Probability')
ax.grid(axis='y')
ax.set_facecolor('#d8dcd6')
st.pyplot(fig)

st.header('clubs')
clubScores = allScores[['club','score','ageAdjScore']].groupby('club').agg({'score': ['mean', 'min', 'max','std','count'],'ageAdjScore': ['mean', 'min', 'max','std','count']})
st.subheader('Goals')
st.bar_chart(clubScores['score']['mean'])
st.subheader('Goal Difference')
st.bar_chart(clubScores['ageAdjScore']['mean'])

#pick a club
clubOption = st.selectbox(
     'Choose club',
     list(allScores['club'].unique()))

#st.write('You selected:', clubOption)

#data table

df = allScores[allScores['club']==clubOption]
df = df[['age','score','ageAdjScore']].groupby('age').agg({'score': ['mean', 'min', 'max','std','count'],'ageAdjScore': ['mean', 'min', 'max','std','count']})

totalGD = df['ageAdjScore']['mean'].sum()
ageGroups=df['ageAdjScore']['mean'].count()
avgAgeAdj = allScores[allScores['club']==clubOption]['ageAdjScore'].mean()
teams = df['ageAdjScore']['count'].sum()

st.subheader('%s Teams have %s age groups with avg GD in age group: %s (%s teams)' % (clubOption, ageGroups,round(avgAgeAdj,2),teams))

#GD
fig, ax = plt.subplots()

bYears = list(df['ageAdjScore']['mean'].index)
y_pos = np.arange(len(bYears))
avgGD = df['ageAdjScore']['mean'].values

ax.barh(bYears, avgGD, align='center')
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Goal Difference')
ax.set_title('GD by birth year')
ax.set_facecolor('#d8dcd6')
st.pyplot(fig)

st.table(df)

#get teams by age

df = allScores[allScores['club']==clubOption][['age','teamName','score', 'ageAdjScore']]

teamOptionYear = st.selectbox(
     'Select birth year:',
     list(df['age'].unique()))

st.table(df[df['age']==teamOptionYear])

st.header('team')
#pick a team based 
teamOption = st.selectbox(
     'Team?',
     list(allScores[(allScores['club']==clubOption)&(allScores['age']==teamOptionYear)]['teamName'].unique()))


st.metric('birth year',allScores[allScores['teamName']==teamOption]['age'])
st.metric('Goals',allScores[allScores['teamName']==teamOption]['score'])
st.metric('GD',round(allScores[allScores['teamName']==teamOption]['ageAdjScore'],2))

#opponent

st.header('Oponent')
#pick a club
vClub = st.selectbox(
     'Opposing Club',
     list(allScores['club'].unique()))

vClub_age = st.selectbox(
     'age?',
     list(allScores[allScores['club']==vClub]['age'].unique()))

vClub_team = st.selectbox(
     'team?',
     list(allScores[(allScores['club']==vClub)&(allScores['age']==vClub_age)]['teamName'].unique()))

st.metric('birth year',allScores[allScores['teamName']==vClub_team]['age'])
st.metric('Goals',allScores[allScores['teamName']==vClub_team]['score'])
st.metric('GD',round(allScores[allScores['teamName']==vClub_team]['ageAdjScore'],2))
