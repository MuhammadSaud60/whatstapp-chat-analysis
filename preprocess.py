import re
import pandas as pd

def preprocess(context):
    
    context = context.replace('\u202f', ' ')

    lines = context.splitlines()

    pattern = re.compile(
    r'^'
    r'(\d{1,2}/\d{1,2}/\d{2}), ' # For DD/MM/YY
    r'(\d{1,2}:\d{2}) ' # For HH:MM
    r'(AM|PM) - ' # For AM or PM
    r'(?:'
     r'([^:]+?): (.*)'
     r'|'
     r'(.*)'
    r')$')

    records = []

    for line in lines:
        m = pattern.match(line)
        if m:
            date, time, ampm = m.group(1), m.group(2), m.group(3)

            ts = f'{date} {time} {ampm}'

            dt = pd.to_datetime(ts, format='%m/%d/%y %I:%M %p')


            if m.group(4):
                user = m.group(4).strip()
                msg = m.group(5).strip()

            else:
                user = "System"
                msg = m.group(6).strip()



            records.append({
                'date': dt,
                'user': user,
                'message': msg,
                'year': dt.year
            })

        else:
            if records:
                records[-1]['message'] += ' ' + line.strip()

    

    df = pd.DataFrame(records)
    month_num = df['date'].dt.month
    month = df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['month_num'] = month_num
    df['month'] = month
    df['day'] = df['date'].dt.day
    df['minute'] = df['date'].dt.minute

    return df