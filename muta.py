from typing import Set

import click
import time
import api


@click.command()
@click.option("--dry-run", "-d", is_flag=True)
def main(dry_run: bool):
    """Muta (ミュー太)

    CLI tool to mute all followees

    - dry_run (bool): if it is specified, mutaro simurate a deletion.
    """

    client = api.create_client()

    for _list in client.GetListsList():
        print(_list.full_name)

    list_name2list_id = {}
    for list_entity in client.GetListsList():
        list_name2list_id[list_entity.full_name] = list_entity.id

    list_name = input("\nlist name: ")
    if list_name == "":
        members_in_list: Set[int] = set()
    else:
        list_id = list_name2list_id[list_name]
        members_in_list = set(user.id for user in client.GetListMembers(list_id))

    friends = set(client.GetFriendIDs())
    muted_user_ids = set(client.GetMutesIDs())

    user_ids_to_be_muted = friends - members_in_list - muted_user_ids
    for user_id in user_ids_to_be_muted:
        user = client.GetUser(user_id)
        if dry_run:
            print("[dry-run] Mute: ", user.screen_name, user.name)
        else:
            print("Mute: ", user.screen_name, user.name)
            while 1:
                try:
                    client.CreateMute(user_id)
                    break
                except Exception as e:
                    print("Encountered Rate Limit: ", e)
                    time.sleep(15 * 60)

    return 0


if __name__ == "__main__":
    main()
