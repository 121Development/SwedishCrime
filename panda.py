import pandas as pd
import DBConnector as db


db.whichConnection(0)

def queryToDF():
    SQLQuery = pd.read_sql_query(
    '''select
    title, updated, event_time, category, category_detail, location, summary, title, latRandom AS latitude, longRandom AS longitude
    from events''', db.conn
    )

    # SQLQuery = pd.read_sql_query(db.read_query(
    # '''select
    # title, updated, event_time, category, category_detail, location, summary, title, latRandom, longRandom
    # from events''', db.conn
    # ))

    #df = pd.DataFrame(SQLQuery, columns=['title', 'updated', 'event_time', 'category', 'category_detail', 'location', 'summary', 'title', 'latRandom', 'longRandom'])
    df = pd.DataFrame(SQLQuery, columns=['title', 'updated', 'event_time', 'category', 'category_detail', 'location', 'summary', 'title', 'latitude', 'longitude'])

    #print (df)
    #print (df.dtypes)

    # df['latitude'] = df['latitude'].astype(float)
    # df['longitude'] = df['longitude'].astype(float)

    df['latitude'] = df['latitude'].apply(pd.to_numeric)
    df['longitude'] = df['longitude'].apply(pd.to_numeric)
    df = df.fillna(0)
    
    #print (df.dtypes)
    #print(df["latitude"])
    return df

queryToDF()