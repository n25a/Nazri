import tomli

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
#                               Config
# ----------------------------------------------------------------


class Config:
    app_name: str = ''
    db: Database = Database()
    cache: Cache = Cache()

    def __init__(self):
        with open("config.toml", mode="rb") as fp:
            config = tomli.load(fp)
            self.app_name = config["app"]["app_name"]
            self.db.mysql.name = config["db-mysql"]["name"]
            self.db.mysql.user = config["db-mysql"]["user"]
            self.db.mysql.password = config["db-mysql"]["password"]
            self.cache.CACHE_TTL = config["cache"]["CACHE_TTL"]


# ----------------------------------------------------------------
#                       public config variable
# ----------------------------------------------------------------

c: Config = Config()
