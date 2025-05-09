import aiomysql
from config.config import MYSQL_CONFIG

def build_url_connection(MYSQL_CONFIG) -> str:
    uri = ''
    return uri

class MySQLReadWriteConnector:
    def __init__(self):
        self.url = build_url_connection(MYSQL_CONFIG=MYSQL_CONFIG)
        self.connect = aiomysql.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['readwriteuser'],
            password=MYSQL_CONFIG['readwriteuserpasswd'],
            db=MYSQL_CONFIG['db'],
            port=MYSQL_CONFIG['port']
        )