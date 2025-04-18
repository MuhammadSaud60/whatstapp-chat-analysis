import pandas as pd
import numpy as np
import emoji
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def fetches(selected_user, df):
    
   
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Total Messages
    num_messages = df.shape[0]
       
    # Count Total Words
    num_words = []
    for word in df['message']:
        num_words.extend(word.split())

    total_words =  len(num_words) 

    # Count Total Media Files shared
    total_mf = df[df['message'].str.lower().str.contains('media omitted')].shape[0]

    #count emoji
    total_emoji = []
    for msg in df['message']:
        total_emoji += [c for c in msg if emoji.is_emoji(c)]


    return num_messages, total_words, total_mf, len(total_emoji)

    


def active_users(df):

    x = df['user'].value_counts().head()
    fig, ax = plt.subplots()

    ax.bar(x.index,x.values, color='green')
    plt.xticks(rotation=80)

    percent_df = pd.DataFrame({
        'User': x.index,
        'Message Count': x.values,
        'Percentage': np.round((x.values / df.shape[0]) * 100, 2)
    })

    return fig, percent_df


def word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'].str.contains('<Media omitted>|Messages and calls are end-to-end encrypted', na=False) == False]

    text = temp['message'].str.cat(sep=" ")

    wc = WordCloud(width=500, height=350, background_color='white')
    df_wc = wc.generate(text)

    fig, ax = plt.subplots()
    ax.imshow(df_wc)

    return df_wc, fig


def timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(f"{timeline['month'][i]} - {timeline['year'][i]}")
    
    timeline['time'] = time
    fig, ax = plt.subplots()

    ax.plot(timeline['time'], timeline['message'], color='black')
    plt.xticks(rotation='vertical')

    return fig


def per_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    per_day = df.groupby('day_name').count()['message'].reset_index()

    fig, ax = plt.subplots()

    ax.bar(per_day['day_name'], per_day['message'], color='red')

    return fig