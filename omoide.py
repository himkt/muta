import click
import api


@click.command('omoide')
@click.option('--batch_size', type=int, default=300)
@click.option('--max_iter', type=int, default=1)
@click.option('--min_like_count', type=int, default=5)
@click.option('--preserve_conversation/--no_preserve_conversation', default=True)
@click.option('--dry_run/--force', default=False)
def main(
        batch_size: int,
        max_iter: int,
        min_like_count: int,
        preserve_conversation: bool,
        dry_run: bool
):

    client = api.create_client()
    credential = client.VerifyCredentials()

    latest_tweet = client.PostUpdate('[test] Start')
    latest_tweet, *_ = client.GetUserTimeline()
    client.DestroyStatus(latest_tweet.id)
    max_tweet_id = latest_tweet.id

    for _ in range(max_iter):
        ret = client.GetUserTimeline(
            count=batch_size,
            max_id=max_tweet_id,
            screen_name=credential.screen_name
        )

        for tw in ret:
            if preserve_conversation and len(tw.user_mentions) > 0:
                print(f'[conversation] Skip {tw.id} ({tw.text}')
                continue

            if tw.favorite_count < min_like_count:
                message = '[dry-run]' if dry_run else '[delete]'
                message += f' Delete {tw.id}'
                message += f' (#like" {tw.favorite_count}, text: {tw.text})'
                print(message)

                if not dry_run:
                    print('delete')
                    # client.DestroyStatus(tw.id)

        max_tweet_id = min(tw.id for tw in ret) - 1


if __name__ == '__main__':
    main()
