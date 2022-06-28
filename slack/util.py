import os
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from slack_sdk import WebClient

# Text resulting in an @channel.
AT_CHANNEL = "<!channel>"

# Type of JSON objects.
JSONType = Union[
    int, float, bool, str, List["JSONType"], Dict[str, "JSONType"], None
]


def email(user: JSONType) -> str:
    # Gives the email of a user from their Slack profile.
    # noinspection PyTypeChecker
    return user["profile"]["email"]


def first_name(user: JSONType) -> str:
    # Gives the first name of a user from their Slack profile.
    return real_name(user).split(maxsplit=1)[0]


def find_channel(client: WebClient, name: str) -> Optional[JSONType]:
    # Finds the channel with exactly the given name.
    channels = client.conversations_list(
        types="public_channel,private_channel", exclude_archived=1
    )["channels"]
    for channel in channels:
        if channel["name"] == name:
            return channel
    return None


def find_channels(
    client: WebClient, names: Iterable[str]
) -> Dict[str, JSONType]:
    # Finds the channels whose name exactly matches one in names.
    names = set(names)
    channels = client.conversations_list(
        types="public_channel,private_channel", exclude_archived=1
    )["channels"]
    return {c["name"]: c for c in channels if c["name"] in names}


def get_client() -> WebClient:
    # Create the Slack client using the SLACK_TOKEN environment variable.
    return WebClient(token=os.environ["SLACK_TOKEN"])


def get_emails(
    client: WebClient, filter_fn: Callable[[JSONType], bool] = lambda x: True
) -> List[str]:
    # Get the emails for all Slack users whose JSON data satisfies the given
    # predicate.
    return [
        email(u) for u in get_users(client, filter_fn)
        if "email" in u["profile"]
    ]


def get_members(client: WebClient, channel: str) -> List[str]:
    # Get all users in the given Slack channel.
    return get_records(client.conversations_members, "members", channel=channel)


def get_records(
    method: Callable, result_key: str, *args: Any, **kwargs: Any
) -> List[JSONType]:
    # Get all paginated records from the given method. result_key is the JSON
    # key giving the current page of results. args and kwargs will be passed to
    # each invocation of method.
    data = method(*args, **kwargs).data
    results = data[result_key]
    while cursor := data["response_metadata"]["next_cursor"]:
        data = method(*args, cursor=cursor, **kwargs).data
        results += data[result_key]
    return results


def get_users(
    client: WebClient, filter_fn: Callable[[JSONType], bool] = lambda x: True
) -> List[JSONType]:
    # Get all Slack users satisfying the given predicate.
    return [
        m for m in get_records(client.users_list, "members") if filter_fn(m)
    ]


def joined_filter(member: JSONType) -> bool:
    # Get all users who have joined the Slack. This excludes invited users,
    # deleted users, and bots.
    return (
        human_filter(member)
        and not member.get("is_invited_user")
        and not member.get("deleted")
    )


def human_filter(member: JSONType) -> bool:
    # Predicate which returns True iff a user corresponds to a human.
    return not member["is_bot"]


def real_name(user: JSONType) -> str:
    # Gives the real name of a user from their Slack profile.
    # noinspection PyTypeChecker
    return user["profile"]["real_name"]
