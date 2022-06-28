import os

from everyaction import EAClient, EAFindFailedException
from slack_sdk import WebClient

import util


def main() -> None:
    # Adds the "Slack Member" activist code to each user in Slack.
    slack_client = WebClient(os.environ["SLACK_TOKEN"])
    emails = util.get_emails(slack_client, util.joined_filter)
    ea_client = EAClient()
    slack_code = ea_client.activist_codes.find("Slack Member").id
    for email in emails:
        try:
            ea_client.people.apply_activist_code(slack_code, email=email)
            print(f"Added {email}")
        except EAFindFailedException:
            print(f"Could not find {email}")
            

if __name__ == "__main__":
    main()
