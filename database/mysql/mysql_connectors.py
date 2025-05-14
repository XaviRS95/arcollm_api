import aiomysql
from config.config import MYSQL_CONFIG

class MySQLReadWriteConnector:
    def __init__(self):
        self.connect = None

    async def start_connection(self):
        self.connect = await aiomysql.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['readwriteuser'],
            password=MYSQL_CONFIG['readwriteuserpasswd'],
            db=MYSQL_CONFIG['db'],
            port=int(MYSQL_CONFIG['port'])
        )

    async def close_connection(self):
        if self.connect is not None:
            self.connect.close()