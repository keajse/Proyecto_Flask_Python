class Config:
    SECRET_KEY='GraciasDios**'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST='localhost'
    MYSQL_USER='root'
    MYSQL_PASSWORD=''
    MYSQL_DB='tienda'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}