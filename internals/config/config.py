# ----------------------------------------------------------------
#                               DB
# ----------------------------------------------------------------


class Mysql:
    name: str = ''
    user: str = ''
    password: str = ''


class Database:
    mysql: Mysql = Mysql()


# ----------------------------------------------------------------
#                              Cache
# ----------------------------------------------------------------


class Cache:
    CACHE_TTL: int = 0


# ----------------------------------------------------------------
#                             Celery
# ----------------------------------------------------------------


class Celery:
    redis_broker: bool = False
    rabbitMQ_broker: bool = False


# ----------------------------------------------------------------
#                               Config
# ----------------------------------------------------------------


class Config:
    app_name: str = ''
    db: Database = Database()
    cache: Cache = Cache()
    celery: Celery = Celery()


# ----------------------------------------------------------------
#                       public config variable
# ----------------------------------------------------------------

c: Config = Config()
