import re
import pandas as pd


def processors(datas):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w\w\s-\s'

    messages = re.split(pattern, datas)[1:]
    dates = re.findall(pattern, datas)

    data = pd.DataFrame({'user_message': messages, 'message_date': dates})

    data['message_date'] = pd.to_datetime(data['message_date'], format='%m/%d/%y, %H:%M %p - ')
    data.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for i in data['user_message']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    data['user'] = users
    data['messages'] = messages
    data.drop(columns=['user_message'], axis=1, inplace=True)

    data['year'] = data['date'].dt.year
    data['month_num'] = data['date'].dt.month
    data['month'] = data['date'].dt.month_name()
    data['day'] = data['date'].dt.day
    data['day_name'] = data['date'].dt.day_name()
    data['hour'] = data['date'].dt.hour
    data['minute'] = data['date'].dt.minute

    period = []
    for hour in data[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))

        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))

        else:
            period.append(str('hour') + "-" + str(hour + 1))

    data['period'] = period
    return data
