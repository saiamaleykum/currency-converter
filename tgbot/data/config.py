from environs import Env


env = Env()
env.read_env()


BOT_TOKEN: str = env.str("BOT_TOKEN") 
REDIS_URL: str = env.str("REDIS_URL")
NUM_CUR_IN_MSG: int = env.int("NUM_CUR_IN_MSG", 10)