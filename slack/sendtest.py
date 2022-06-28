import sys

import util


def main() -> None:
    # Used to test "senddms.py" with a message to check formatting, etc.
    if len(sys.argv) != 2:
        print(
            f"{sys.argv[0]} expects exactly one argument (the ID of the user "
                f"to send the message to).",
            file=sys.stderr
        )
        sys.exit(1)
    user_id = sys.argv[1]
    with open("msg.txt") as f:
        msg = f.read()
    slack = util.get_client()
    slack.chat_postMessage(channel=user_id, text=msg)


if __name__ == "__main__":
    main()
