from dotenv import dotenv_values

config_values = dotenv_values(".env")

telegram_token = config_values["TELEGRAM_TOKEN"]
user_id_admin = config_values["USER_ID_ADMIN"]
algorithm = config_values["ALGORITHM"]
secret_key = config_values["SECRET_KEY"]
access_token_exp_minutes = int(config_values["ACCESS_TOKEN_EXPIRE_MINUTES"])