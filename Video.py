#!/usr/bin/env python
# coding: utf-8

# In[4]:

# import library to get youtube data
from pytube import Channel 
from pytube import Playlist
from pytube import YouTube

# import library for modle bulding
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer 
import time
import telegram.ext
import os


# In[6]:



# A function for creating youtube video dataset 
def get_data(channel_name):
    # Making channel url
    channel_url=f"https://www.youtube.com/c/{channel_name}"
    #Creating a channel object
    channel = Channel(channel_url)
    # Making a list of urls of video
    all_links=channel.video_urls
    
    title=[]# It will hold the title of videos
    keywords=[]# It will hold the key wordes of videos
    url=[]# It will hold the url of videos
    # going through all links and fatching there info
    for video_link in all_links:
        title.append(YouTube(i).title)
        keywords.append(YouTube(i).keywords)
        url.append(i)
    #joining all keyes together
    all_key=[]
    for i in keywords:
        all_key.append(" ".join(i))
    data=[]
    # Creating a Data frame with the data
    for x,y,z in zip(title,url,all_key):
        d={}
        d['title']=x
        d["url"]=y
        d["keywordes"]=z
        data.append(d)
    df=pd.DataFrame(data)
    # Saving it in csv
    try:os.remove(f"{channel_name}.csv")
    except:pass
    df.to_csv(f"{channel_name}.csv")
    return


# In[5]:


#function for video
# It takes video description as input
def get_video(input_text,csv):
    df=pd.read_csv(csv)
    #Creating A pandas seris using keywordes and title column
    keywordes_list=df['keywordes']+df['title']
    #converting it in a list
    keywordes_list=keywordes_list.tolist()
    #then append it in keyword list
    keywordes_list.append(input_text)
    #Then a tfidf vector from it
    vec=TfidfVectorizer().fit_transform(keywordes_list)
    # Remove the description from the list 
    keywordes_list.pop()
    #calculate cosine_similarity from the vector, reduce dimantion by flatning it, and convert it in a list
    scor=cosine_similarity(vec[-1],vec[:-1]).flatten().tolist()
    #find the max value and it's index
    index_value =scor.index(max(scor))
    #return the title and url base on the index
    return (df.iloc[index_value]["title"],df.iloc[index_value]["url"])


# In[ ]:



with open("Key.txt","r") as f:
    key = f.read()
# A function for starting massage
def start(updater,context):
    updater.message.reply_text("""
Hi Folks
Give me any description
    """                       )
# A function for refresh and lode new data in csv
def refresh(updater,context):
    updater.message.reply_text("We are updating the video list \nYou willbe notified after completing the process")
    get_data("dhruvrathee")
    updater.message.reply_text("It's ready to go")
# A function for taking the user input amd suggest video
def give_reply(updater,context):
    title,url=get_video(updater.message.text,"dhruvrathee.csv")
    print("Giving reply")
    updater.message.reply_text(f"try this {title} \n {url}")
    
updater = telegram.ext.Updater(key, use_context = True)
disp = updater.dispatcher

#adding the functions in CommandHandler
disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("refresh",refresh))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,give_reply))
updater.start_polling()
updater.idle()


