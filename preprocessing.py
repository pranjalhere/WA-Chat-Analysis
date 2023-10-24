import re
import pandas as pd
def preprocess(data):
    mes_pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'

    message_list=re.split(mes_pattern,data)[1:]

    date_pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)'

    date_list=re.findall(date_pattern,data)

    df = pd.DataFrame({'mes_dates': date_list})
    df['mes_dates'] = pd.to_datetime(df['mes_dates'], format='%d/%m/%Y, %I:%M %p')

    users_sep = []
    messages_sep = []
    for temp in message_list:
        input_string = temp
        entry = re.split('([\w\W]+?):\s', temp)
        if entry[1:]:
            first_colon_index = input_string.find(":")
            part1 = input_string[:first_colon_index]
            part2 = input_string[first_colon_index + 1:]
            users_sep.append(part1)
            messages_sep.append(part2)
        else:
            users_sep.append('group_notification')
            messages_sep.append(entry[0])
    users_sep = [s.lstrip(' -') for s in users_sep]
    df['user'] = users_sep
    df['messages'] = messages_sep

    df['year'] = df['mes_dates'].dt.year
    df['month'] = df['mes_dates'].dt.month_name()
    df['day'] = df['mes_dates'].dt.day
    df['hours'] = df['mes_dates'].dt.hour
    df['minutes'] = df['mes_dates'].dt.minute
    df['month_num'] = df['mes_dates'].dt.month
    df['only_date'] = df['mes_dates'].dt.date
    df['day_name'] = df['mes_dates'].dt.day_name()

    period = []
    for hour in df['hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    df = df[df['user'] != 'group_notification']
    df = df.reset_index(drop=True)
    df = df[df['messages'] != ' This message was deleted\n']
    df = df.reset_index(drop=True)
    return df

