import aiosqlite

from settings import CHANNELS

class DBworker():
    
    def __init__(self):
        ...

    async def execute(self, _channel, _query, _values=None):
        db_file = f'{_channel}.sqlite'
        async with aiosqlite.connect(db_file) as db:
            await db.execute(_query, _values)
            await db.commit()
                
    async def log_message(self, _channel, _data_dict):
        columns = ', '.join(_data_dict.keys())
        placeholders = ', '.join('?' * len(_data_dict.values()))
        query = f'INSERT INTO main ({columns}) VALUES ({placeholders});'
        await self.execute(_channel, query, tuple(_data_dict.values()))

    async def get_stats(self, _channel):
        db_file = f'{_channel}.sqlite'
        async with aiosqlite.connect(db_file) as db:
            full_response = []
            cursor = await db.cursor()
            total = await cursor.execute('SELECT COUNT(*) AS total_messages FROM main;')
            response_total = await total.fetchall()
            total_msgs = response_total[0][0]
            
            highest = await cursor.execute('''SELECT username, COUNT(*) AS num_messages FROM main
            GROUP BY username ORDER BY num_messages DESC LIMIT 1;''')
            response_highest = await highest.fetchall()
            highest_user = response_highest[0][0]

            unique = await cursor.execute('''SELECT COUNT(DISTINCT username) as unique_names_count FROM main;''')
            response_unique = await unique.fetchall()
            unique_users = response_unique[0][0]

            avg = await cursor.execute('''SELECT AVG(num_messages) AS avg_messages_per_user
                FROM (
                    SELECT username, COUNT(*) AS num_messages
                    FROM main
                    GROUP BY username
                ) subquery; ''')
            response = await avg.fetchall()
            avg_perUser = round(response[0][0], 2)
            
            chat_response = f'''Total messages: {total_msgs}, 
                                Unique users: {unique_users},
                                Messages per user: {avg_perUser},
                                Most messagges from: {highest_user},'''

            return chat_response


def init_databases():
        #todo: overhaul db initiation, change to aiosqlite methods
        import sqlite3
        for channel in CHANNELS:
            db = sqlite3.connect(f'{channel}.sqlite')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS main(
                    type INTEGER,
                    datetime DATETIME,
                    username TEXT,
                    content TEXT,
                    raw_data TEXT
                ) 
            ''')

if __name__ == '__main__': 
    ...
    #todo: add check method if db exist on startup
    init_databases()