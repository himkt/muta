from typing import Set

import twitter
import os
import click
import time


CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN_KEY = os.getenv("ACCESS_TOKEN_KEY")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


@click.command()
@click.option("--dry-run", "-d", is_flag=True)
def main(dry_run: bool):
    """Muta (ミュー太)

    CLI tool to mute all followees

    - dry_run (bool): if it is specified, mutaro simurate a deletion.
    """

    api = twitter.Api(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token_key=ACCESS_TOKEN_KEY,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    for _list in api.GetListsList():
        print(_list.full_name)

    list_name2list_id = {}
    for list_entity in api.GetListsList():
        list_name2list_id[list_entity.full_name] = list_entity.id

    list_name = input("\nlist name: ")
    if list_name == "":
        members_in_list: Set[int] = set()
    else:
        list_id = list_name2list_id[list_name]
        members_in_list = set(user.id for user in api.GetListMembers(list_id))

    friends = set(api.GetFriendIDs())
    muted_user_ids = set(api.GetMutesIDs())

    user_ids_to_be_muted = friends - members_in_list - muted_user_ids
    for user_id in user_ids_to_be_muted:
        user = api.GetUser(user_id)
        if dry_run:
            print("[dry-run] Mute: ", user.screen_name, user.name)
        else:
            print("Mute: ", user.screen_name, user.name)
            while 1:
                try:
                    api.CreateMute(user_id)
                    break
                except twitter.error.TwitterError as e:
                    print("Encountered Rate Limit: ", e)
                    time.sleep(15 * 60)

    return 0


if __name__ == "__main__":
    main()
