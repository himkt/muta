import twitter
import os


def create_client() -> twitter.Api:
    return twitter.Api(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token_key=os.getenv("ACCESS_TOKEN_KEY"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )
