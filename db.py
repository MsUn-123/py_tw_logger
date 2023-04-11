import aiosqlite

from settings import CHANNELS

class DBworker():
    
    def __init__(self, db_name: str):
        self.channel = db_name
        self.db_file = f'{db_name}.sqlite'

    async def execute(self, query, values=None):
        async with aiosqlite.connect(self.db_file) as db:
            if values:
                await db.execute(query, values)
            else:
                await db.execute(query)
            await db.commit()
                
    async def log_message(self, data_dict):
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join('?' * len(data_dict.values()))
        query = f'INSERT INTO main ({columns}) VALUES ({placeholders});'
        await self.execute(query, tuple(data_dict.values()))

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
    #todo: add check method if db exist
    init_databases()