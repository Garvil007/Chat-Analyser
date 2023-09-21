from urlextract import URLExtract
from wordcloud import WordCloud as wc
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_data(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    num_message = df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    media_msg = df[df['messages'] == '<Media omitted>\n'].shape[0]

    links = []
    for msg in df['messages']:
        links.extend(extract.find_urls(msg))

    return num_message, len(words), media_msg, len(links)


def most_busy(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    f = open('stop_words_hinglish.txt', 'r')
    stop_words = f.read()

    new_df = df[df['user'] != 'group_notification']
    new_df = new_df[new_df['messages'] != '<Media omitted>\n']
    new_df = new_df[new_df['messages'] != 'This message was deleted\n']

    words = []

    def remove_stop_words(msg):
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)

    wcld = wc(width=500, height=500, min_font_size=10, background_color='white')
    new_df['messages'] = new_df['messages'].apply(remove_stop_words)
    df_wc = wcld.generate(df['messages'].str.cat(sep=" "))
    return df_wc


def common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('stop_words_hinglish.txt', 'r')
    stop_words = f.read()

    new_df = df[df['user'] != 'group_notification']
    new_df = new_df[new_df['messages'] != '<Media omitted>\n']
    new_df = new_df[new_df['messages'] != 'This message was deleted\n']

    words = []

    for msg in new_df['messages']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    dfr = pd.DataFrame(Counter(words).most_common(20))

    return dfr


def emoji_count(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for msg in df['messages']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def timeline_month(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def timeline_daily(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    dtimeline = df.groupby('day').count()['messages'].reset_index()

    return dtimeline

def activity_map_weekly(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def activity_map_monthly(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_map = df.pivot_table(index='day_name', columns='period', values="messages", aggfunc='count').fillna(0)

    return activity_map
