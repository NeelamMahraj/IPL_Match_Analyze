#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# load match dataset and ball datset into jupyter notebook
m_data = pd.read_csv('D:/archive (1)/Match.csv')
b_data = pd.read_csv('D:/archive (1)/ball.csv')


# In[3]:


# print first 5 rows of the dataset
m_data.head()


# In[4]:


# print first 5 rows of the dataset

b_data.head()


# In[5]:


# Show null values in match dataset 
m_data.isnull().sum()


# In[6]:


#Show null values in ball dataset
b_data.isnull().sum()


# In[7]:


# how many rows & columns are present in match dataset
m_data.shape


# In[8]:


# how many rows & columns are present in ball dataset

b_data.shape


# In[9]:


# how many matches are played ,in which city and by which teams.
print('Match played so far:',m_data.shape[0])
print('\n Cities played at:\n',m_data['city'].unique())
print('\n Team ,played match :\n', m_data['team1'].unique())


# In[10]:


# Extract year from the date column
m_data['Season'] = pd.DatetimeIndex(m_data['date']).year
m_data.head()


# In[11]:


# Total number of matches held from 2008 to 2020

m_season = m_data.groupby(['Season'])['id'].count().reset_index().rename(columns={'id':'Matches'})
m_season


# In[12]:


# Bar Graph to show the number of matches played

sns.countplot(m_data['Season'])
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel('Season',fontsize=10)
plt.ylabel('Count',fontsize=10)
plt.title('Total Matches played in each season',fontsize=10,fontweight='bold')


# In[13]:


# merge 2 columns from match dataset with ball dataset

s_data = m_data[['id','Season']].merge(b_data,left_on ='id',right_on='id',how='left').drop('id',1)
s_data


# In[14]:


# Total runs in each season
season = s_data.groupby(['Season'])['total_runs'].sum().reset_index()
p = season.set_index('Season')
ax = plt.axes()
ax.set(facecolor = 'white')
sns.lineplot(data=p,palette='magma')
plt.title("Total runs in each season",fontsize=12,fontweight='bold')
plt.show()


# In[15]:


# Runs scored per match each season
runs = pd.concat([m_season,season.iloc[:,1]],axis=1)
runs['Runs scored per match'] = runs['total_runs']/runs['Matches']
runs.set_index('Season',inplace=True)
runs


# In[16]:


# number of tosses won by each team
toss = m_data['toss_winner'].value_counts()
ax = plt.axes()
ax.set(facecolor='white')
sns.set(rc={'figure.figsize':(15,10)},style='darkgrid')
ax.set_title('No of tosses won by each team',fontsize=15,fontweight='bold')
sns.barplot(y=toss.index,x=toss ,orient='h',palette='icefire',saturation=1)
plt.xlabel('# of tosses won')
plt.ylabel('Teams')
plt.show()


# In[17]:


# Toss decision across each seasons
ax = plt.axes()
ax.set(facecolor='white')
sns.countplot(x='Season',hue='toss_decision',data=m_data,palette="magma",saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=15)
plt.xlabel('\n Season',fontsize=15)
plt.ylabel('\n Count',fontsize=15)
plt.title('Toss decision seasons',fontsize=12,fontweight='bold')
plt.show()


# In[18]:


# how many matches wins by wickets and by runs and how much gets tie
m_data['result'].value_counts()


# In[19]:


#which stadium is best for winning by wickets
m_data.venue[m_data.result != 'runs'].mode()


# In[20]:


#which stadium is best for winning by runs
m_data.venue[m_data.result != 'wickets'].mode()


# In[21]:


# best stadium after winning the toss
m_data.venue[m_data.toss_winner=='Kings XI Punjab'][m_data.winner=='Kings XI Punjab'].mode()


# In[22]:


m_data.venue[m_data.toss_winner=='Mumbai Indians'][m_data.winner=='Mumbai Indians'].mode()


# In[23]:


m_data.winner[m_data.result != 'runs'].mode()


# In[24]:


m_data.winner[m_data.result != 'wickets'].mode()


# In[25]:


# winning toss = winning match
toss = m_data['toss_winner'] == m_data['winner']
plt.figure(figsize=(10,5))
sns.countplot(toss)
plt.show()


# In[26]:


plt.figure(figsize=(12,4))
sns.countplot(m_data.toss_decision[m_data.toss_winner == m_data.winner])
plt.show()


# In[27]:


# Now Use Ball dataset 
# Analyze particular player and his performance 
player = (b_data['batsman']=='SK Raina')
df_r = b_data[player]
df_r.head()


# In[28]:


# find dismissal_kind
df_r['dismissal_kind'].value_counts().plot.pie(autopct='%1.1f%%',shadow=True,rotatelabels=True)
plt.title('Dissmissal_kind',fontsize=15,fontweight='bold')
plt.show()


# In[29]:


# runs scored by shuraish raina
def count(df_r,runs):
    return len(df_r[df_r['batsman_runs']==runs])*runs


# In[30]:


print("Runs scored from 1's :",count(df_r,1))
print("Runs scored from 2's :",count(df_r,2))
print("Runs scored from 3's :",count(df_r,3))
print("Runs scored from 4's :",count(df_r,4))
print("Runs scored from 5's :",count(df_r,5))
print("Runs scored from 6's :",count(df_r,6))


# In[32]:


# find max result Margin
m_data[m_data['result_margin']==m_data['result_margin'].max()]


# In[33]:


# find min result Margin
m_data[m_data['result_margin']==m_data['result_margin'].min()]


# In[36]:


# top 10 Batsman with highest runs
runs = b_data.groupby(['batsman'])['batsman_runs'].sum().reset_index()
runs.columns = ['Batsman','runs']
y = runs.sort_values(by='runs',ascending=False).head(10).reset_index().drop('index',axis=1)
y


# In[40]:


# visualize above results 
ax = plt.axes()
ax.set(facecolor='White')
sns.barplot(x=y['Batsman'],y=y['runs'],palette='rocket',saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel('\n player',fontsize=15)
plt.ylabel('Total Run',fontsize=15)
plt.title('Top 10 runs scorer in IPL',fontsize=15,fontweight='bold')


# In[47]:


# Highest Man Of the Match winner
ax = plt.axes()
ax.set(facecolor='purple')
m_data.player_of_match.value_counts()[:10].plot(kind='bar')
plt.xlabel('Player')
plt.ylabel('count')
plt.title('Highest MOM of the macth winner',fontsize=15,fontweight='bold')


# In[ ]:




