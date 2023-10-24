from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected_user,df):
    if(selected_user!='Overall'):
        df = df[df['user'] == selected_user]

    #number of messages
    num_messages = df.shape[0]

    #number of words
    words = []
    for mes in df['messages']:
        words.extend(mes.split())

    #number of media items shared
    number_of_media=df[df['messages']==' <Media omitted>\n'].shape[0]

    #number of links
    extractor = URLExtract()
    urls = []
    for mes in df['messages']:
        if extractor.has_urls(mes):
            urls.append(extractor.find_urls(mes))
    links_num=len(urls)
    return len(words), num_messages,number_of_media,links_num

def busy_user(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'Name/Phone','count':'Percentage'})
    return x,df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()

    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df = df[df['messages'] != ' <Media omitted>\n']
    df = df.reset_index(drop=True)

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords and len(word)!=1:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df['messages']=df['messages'].apply(remove_stop_words)
    df_wc=wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc

def most_commonwords(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df = df[df['messages'] != ' <Media omitted>\n']
    df = df.reset_index(drop=True)

    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()

    words = []
    for mes in df['messages']:
        for word in mes.lower().split():
            if word not in stopwords and len(word)!=1:
                words.append(word)

    common_words_df=pd.DataFrame(Counter(words).most_common(20))

    return common_words_df

def emoji_helper(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    emojies = []
    for message in df['messages']:
        for c in message:
            if emoji.is_emoji(c):
                emojies.extend(c)

    emoji_df=pd.DataFrame(Counter(emojies).most_common(len(Counter(emojies))))
    return emoji_df,len(emojies)

def month_time(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline
def daily_time(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def heatmap(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    return df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)

