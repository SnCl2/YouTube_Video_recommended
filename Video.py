#!/usr/bin/env python
# coding: utf-8

# In[4]:


from pytube import Channel
from pytube import Playlist
from pytube import YouTube
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import multiprocessing 
import time
import telegram.ext
import os


# In[6]:




def get_data(channel_name):
    channel_url=f"https://www.youtube.com/c/{channel_name}"
    print(channel_url)
    channel = Channel(channel_url)
    all_links=channel.video_urls
    title=[]
    keywords=[]
    url=[]
    for i in all_links:
        title.append(YouTube(i).title)
        keywords.append(YouTube(i).keywords)
        url.append(i)
    all_key=[]
    for i in keywords:
        all_key.append(" ".join(i))
    data=[]
    for x,y,z in zip(title,url,all_key):
        d={}
        d['title']=x
        d["url"]=y
        d["keywordes"]=z
        data.append(d)
    df=pd.DataFrame(data)
    try:os.remove(f"{channel_name}.csv")
    except:pass
    df.to_csv(f"{channel_name}.csv")
    print("Done")
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

disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("refresh",refresh))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,give_reply))
updater.start_polling()
updater.idle()


# In[8]:


a=time.time()
get_data("dhruvrathee")
b=time.time()
print(b-a)


# In[ ]:


get_data("dhruvrathee")


# In[ ]:




