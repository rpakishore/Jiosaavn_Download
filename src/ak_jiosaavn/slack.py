from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import sys
import getpass

if sys.platform=="win32":
    import keyring

def getpwd(item: str, username: str) -> str:
    if sys.platform=="win32":
        pwd = keyring.get_password(item, username)
        if not pwd:
            print("Password is not saved in keyring.")
            pwd = getpass.getpass(
                f"Enter the password for `{item}` corresponding to \
                    Username `{username}`: ")
            choice = input("Would you like to save this pwd to keyring?(Y|n): ")
            if choice.strip().lower() in ['', 'y','n']:
                if choice.strip().lower() != 'n':
                    keyring.set_password(item, username, pwd)
    else:
        pwd = getpass.getpass(
            f"Enter the password for `{item}` corresponding to \
                Username`{username}`  : ")
    return pwd

class Slack:
    def __init__(self):
        self.client = WebClient(token=getpwd('Slack-pythonbot', 'token'))
        return
    
    def __repr__(self) -> str:
        return "Slack()"

    def __str__(self) -> str:
        return "Slack class instance"
    
    def channel_id(self, channel_name: str) -> str:
        """Returns channel id for the specified channel name"""
        return getpwd('Slack-pythonbot', channel_name)

    def msg(self, message:str, channel:str="python"):
        """Sends Slack message
        Args:
            message (str): Message to be sent
            channel (str, optional): Slack channel to send the message to. \
                Defaults to "#python".
        """
        err = 0
        try:
            self.client.chat_postMessage(channel=self.channel_id(channel),text=message)
        except SlackApiError as e:
            print(f'NG - Slack message not sent: {str(e)}')
            err = 1
        return err
    
    def post_block(self, block: dict, channel: str):
        """Posts the constructed block to slack chat
        """
        err = 0
        try:
            self.client.chat_postMessage(channel=self.channel_id(channel),blocks=block)
        except SlackApiError as e:
            print(f'NG - Slack message not sent: {str(e)}')
            err = 1
        return err

class SlackBlock:
    def __init__(self):
        self.block = []
        return
    
    def __repr__(self) -> str:
        return "SlackBlock()"

    def __str__(self) -> str:
        return "SlackBlock class instance"
    
    def mrkdwn(self, text:str, image_url:str=None,image_alt_text:str="") -> dict:
        """Adds markdown element to block message
        Args:
            text (str): Text to display
            image_url (str, optional): Image to display. Defaults to None.
            image_alt_text (str, optional): Alt string for image. Defaults to "".
        """ 
        if not image_url:
            self.block.append({"type": "section",
                               "text": {"type": "mrkdwn","text": text}})
        else:
            self.block.append({"type": "section",
                               "text": {"type": "mrkdwn","text": text},
                               "accessory": {"type": "image",
                                             "image_url": image_url,
                                             "alt_text": image_alt_text}})
        return self.block
    
    def divider(self) -> dict:
        """Adds divider to the block message
        """
        self.block.append({"type": "divider"})
        return self.block
    
    def image(self, title_txt: str, image_url: str, image_alt_text: str="") -> dict:
        self.block.append({"type": "image",
                           "title": {"type": "plain_text","text": title_txt},
                           "image_url": image_url,
                           "alt_text": image_alt_text})
        return self.block
    
    def header(self, text: str) -> dict:
        self.block.append({"type": "header",
                           "text": {"type": "plain_text","text": text}})
        return self.block