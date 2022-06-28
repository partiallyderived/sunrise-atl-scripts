import sys

import util


def main() -> None:
    # Sends the direct message found in "msg.txt" to each person on Slack.
    if len(sys.argv) > 1:
        print(f'{sys.argv[0]} does not expect any arguments', file=sys.stderr)
        sys.exit(1)
    with open('msg.txt') as f:
        msg = f.read()
    slack = util.get_client()
    users = util.get_users(slack, util.joined_filter)
    for user in users:
        slack.chat_postMessage(channel=user['id'], text=msg)


if __name__ == '__main__':
    main()
