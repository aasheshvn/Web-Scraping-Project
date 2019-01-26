#!/usr/bin/env python
# coding: utf-8

# In[26]:


####Importing Libraries

import requests
import pandas as pd
from bs4 import BeautifulSoup
from googlesearch import search
import matplotlib.pyplot as plt


# ### Player specfic details from ESPN stats website

# In[42]:


def get_player_link(player,test_or_odi):
    
    player_name=player
    player=player + " espncricinfo"
    
####Performing player search in google
    for j in search(player,tld="com",num=10,start=0,stop=1,pause=2.0):
        search_link=j
        break
        
##Unique player_id for each player
    player_id=search_link.split('/')[-1].split('.')[0] 
    if test_or_odi == 1:
        link="http://stats.espncricinfo.com/ci/engine/player/"+player_id+".html?class=1;template=results;type=allround"
    elif test_or_odi == 2:
        link="http://stats.espncricinfo.com/ci/engine/player/"+player_id+".html?class=2;template=results;type=allround"
    else:
        print("Please enter either 1 or 2")
    print("\nComplete statistics of %s can be viewed from the link below:" %player_name)
    print(link)
    r=requests.get(link)
    content=r.content
    soup=BeautifulSoup(content,"html.parser")
    return soup
# print(soup.prettify())


# ### Player stats played against each country

# In[28]:


def country_against(soup):

    all=soup.find("div",{"class":"pnl650M"}).find_all("tbody")
    country_against=all[1]
    country_list=[]
    
###Get the list of all the country names
    for i in country_against.find_all("b"):
        country_list.append(i.text)

###Get all the player data played against each country
    country_against_data=[]
    l=0
    for i in country_against.find_all("tr",{"class":"data1"}):
        country_against_data.append([])
        k=i.find_all("td")
        count=0
        for j in (range(0,7)):
            if count>1:
                country_against_data[l].append(k[j].text)
            count=count+1
        l=l+1

###Insert the country_against data into dataframe

    df_country_against=pd.DataFrame(country_against_data,index=country_list,columns=["Matches","Runs","HS","Average","100's"])
    df_country_against.rename_axis('Name',axis='columns',inplace=True)
    return df_country_against


# ### Player stats played in each country

# In[29]:


def in_country(soup):

    all=soup.find("div",{"class":"pnl650M"}).find_all("tbody")
    country_in=all[2]
    country_in_list=[]
    
###Get the list of all the country names
    for i in country_in.find_all("b"):
        country_in_list.append(i.text)

###Get all the player data played in each country
    country_in_data=[]

    l=0
    check=0
    for i in country_in.find_all("tr",{"class":"data1"}):
        if check>0:
            country_in_data.append([])
            k=i.find_all("td")   
            count=0
            for j in (range(0,7)):
                if count>1:
                    country_in_data[l].append(k[j].text)
                count=count+1
            l=l+1
        check=check+1
        
###Insert the country_in data into dataframe

    df_country_in=pd.DataFrame(country_in_data,index=country_in_list,columns=["Matches","Runs","HS","Average","100's"])
    df_country_in.rename_axis('Name',axis='columns',inplace=True)
    return df_country_in


# ### Player stats played in each continent

# In[30]:


def in_continent(soup):

    all=soup.find("div",{"class":"pnl650M"}).find_all("tbody")
    continent_in=all[3]
    continent_in_list=[]

###Get the list of all the continent names
    for i in continent_in.find_all("b"):
        continent_in_list.append(i.text)

###Get all the player data played in each continent
    continent_in_data=[]

    l=0
    check=0
    for i in continent_in.find_all("tr",{"class":"data1"}):
        if check>0:
            continent_in_data.append([])
            k=i.find_all("td")   
            count=0
            for j in (range(0,7)):
                if count>1:
                    continent_in_data[l].append(k[j].text)
                count=count+1
            l=l+1
        check=check+1

###Insert the continent_in_data into dataframe
    df_continent_in=pd.DataFrame(continent_in_data,index=continent_in_list,columns=["Matches","Runs","HS","Average","100's"])
    df_continent_in.set_index([continent_in_list])
    return df_continent_in


# ### Player stats in Home/Away/Neutral Venues

# In[31]:


def home_away_neutral(soup):
    
    all=soup.find("div",{"class":"pnl650M"}).find_all("tbody")
    home_away_neutral=all[4]
    home_away_neutral_list=[]
    for i in home_away_neutral.find_all("b"):
        home_away_neutral_list.append(i.text)

###Get all the player data played across venues
    home_away_neutral_data=[]

    l=0
    check=0
    for i in home_away_neutral.find_all("tr",{"class":"data1"}):
        if check>0:
            home_away_neutral_data.append([])
            k=i.find_all("td")   
            count=0
            for j in (range(0,7)):
                if count>1:
                    home_away_neutral_data[l].append(k[j].text)
                count=count+1
            l=l+1
        check=check+1

###Insert the home_away_neutral_data into dataframe

    df_home_away_neutral=pd.DataFrame(home_away_neutral_data,index=home_away_neutral_list,columns=["Matches","Runs","HS","Average","100's"])
    df_home_away_neutral.set_index([home_away_neutral_list])
    return df_home_away_neutral


# ### Year wise player stats

# In[32]:


def year_wise(soup):

    all=soup.find("div",{"class":"pnl650M"}).find_all("tbody")
    year_wise=all[5]
    year_wise_list=[]
    
###Get all the years the player has played
    for i in year_wise.find_all("b"):
        year_wise_list.append(i.text)

###Get all the player data played in each year    
    year_wise_data=[]
    l=0
    check=0
    for i in year_wise.find_all("tr",{"class":"data1"}):
        if check>0:
            year_wise_data.append([])
            k=i.find_all("td")   
            count=0
            for j in (range(0,7)):
                if count>1:
                    year_wise_data[l].append(k[j].text)
                count=count+1
            l=l+1
        check=check+1

###Insert the year wise player data into dataframe
    df_year_wise=pd.DataFrame(year_wise_data,index=year_wise_list,columns=["Matches","Runs","HS","Average","100's"])
    df_year_wise.set_index([year_wise_list])
    return df_year_wise


# ### Search for players and visually compare the stats

# In[43]:


def main():
    player1=input("Enter player 1's name: ")
    player2=input("Enter player 2's name: ")
    test_or_odi=int(input("What would you like to compare? 1. Test Statistics 2. ODI Statistics: \n"))
    soup1=get_player_link(player1,test_or_odi)
    soup2=get_player_link(player2,test_or_odi)
    print("\n1. Played against each country")
    print("2. Played in each country")
    print("3. Played in each continent")
    print("4. Played in home/away/neutral")
    print("5. Year-wise\n")
    
    option=int(input("Select an option from the above menu for stats comparison:\n "))
    if (option == 1):
        player1_data=country_against(soup1)
        player2_data=country_against(soup2)
    elif (option == 2):
        player1_data=in_country(soup1)
        player2_data=in_country(soup2)
    elif (option == 3):
        player1_data=in_continent(soup1)
        player2_data=in_continent(soup2)
    elif (option ==4):
        player1_data=home_away_neutral(soup1)
        player2_data=home_away_neutral(soup2)
    elif (option == 5):
        player1_data=year_wise(soup1)
        player2_data=year_wise(soup2)
    
    player1_data.replace('-','0',inplace=True)
    player2_data.replace('-','0',inplace=True)
    x=player1_data.index.tolist()
    y=player2_data.index.tolist()
    common=list(set(x) & set(y))
    common.sort()
    diff1=list(set(x)-set(y))
    for i in diff1:
        player1_data.drop(i,inplace=True)
    diff2=list(set(y)-set(x))
    for i in diff2:
        player2_data.drop(i,inplace=True) 
     
    print("\n1. Matches played")
    print("2. Runs scored")
    print("3. HS")
    print("4. Average")
    print("5. 100's scored")
    print("6. All\n")
    stat_required=int(input("Select a statistic from the above menu that needs to be compared:\n "))
    
    if (stat_required == 1 or stat_required == 6):   
        player1_Matches=player1_data.Matches.tolist()
        player1_Matches=[int(i) for i in player1_Matches]
        player2_Matches=player2_data.Matches.tolist()
        player2_Matches=[int(i) for i in player2_Matches]
        df=pd.DataFrame({player1:player1_Matches,player2:player2_Matches},index=common)
        ax=df.plot.bar(rot=0,figsize=(16,5))
        ax.set_ylabel("Matches played")
        fig = plt.gcf()
        plt.show()
        fig.savefig('Matches Played.png',bbox_inches='tight')
        
    if (stat_required == 2 or stat_required == 6):
        player1_runs=player1_data.Runs.tolist()
        player1_runs=[int(i) for i in player1_runs]
        player2_runs=player2_data.Runs.tolist()
        player2_runs=[int(i) for i in player2_runs]
        df=pd.DataFrame({player1:player1_runs,player2:player2_runs},index=common)
        ax=df.plot.bar(rot=0,figsize=(16,5))
        ax.set_ylabel("Runs scored")
        fig = plt.gcf()
        plt.show()
        fig.savefig('Runs Scored.png',bbox_inches='tight')
    if (stat_required == 3 or stat_required == 6):
        player1_HS=player1_data.HS.tolist()
        player1_HS=[i.rstrip('*') for i in player1_HS]
        player1_HS=[int(i) for i in player1_HS]
        player2_HS=player2_data.HS.tolist()
        player2_HS=[i.rstrip('*') for i in player2_HS]
        player2_HS=[int(i) for i in player2_HS]
        df=pd.DataFrame({player1:player1_HS,player2:player2_HS},index=common)
        ax=df.plot.bar(rot=0,figsize=(16,5))
        ax.set_ylabel("Highest Scores")
        fig = plt.gcf()
        plt.show()
        fig.savefig('Highest Scores.png',bbox_inches='tight')
    if (stat_required ==4 or stat_required == 6):
        player1_average=player1_data.Average.tolist()
        player1_average=[float(i) for i in player1_average]
        player2_average=player2_data.Average.tolist()
        player2_average=[float(i) for i in player2_average]
        df=pd.DataFrame({player1:player1_average,player2:player2_average},index=common)
        ax=df.plot.bar(rot=0,figsize=(16,5))
        ax.set_ylabel("Average")
        fig = plt.gcf()
        plt.show()
        fig.savefig('Average.png',bbox_inches='tight')
    if (stat_required == 5 or stat_required == 6):
        player1_100=player1_data["100's"].tolist()
        player1_100=[int(i) for i in player1_100]
        player2_100=player2_data["100's"].tolist()
        player2_100=[int(i) for i in player2_100]
        df=pd.DataFrame({player1:player1_100,player2:player2_100},index=common)
        ax=df.plot.bar(rot=0,figsize=(16,5))
        ax.set_ylabel("100's Scored")
        fig = plt.gcf()
        plt.show()
        fig.savefig('Hundreds.png',bbox_inches='tight')
    
main()
    
    


# In[ ]:




