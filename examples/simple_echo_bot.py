from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.datatypes.xmpp.errors import LoginError
from kik_unofficial.configuration import env

# Read credentials from the environment or an untracked .env file.
username = env.get("BOT_USERNAME")
password = env.get("BOT_PASSWORD")


# This bot class handles all the callbacks from the kik client
class EchoBot(KikClientCallback):
    def __init__(self):
        if not username or not password or username == "bot_username" or password == "bot_password":
            raise ValueError("Configure BOT_USERNAME and BOT_PASSWORD before running the example")
        self.client = KikClient(self, username, password,
                                host=env.get("KIK_HOST") or None,
                                device_id=env.get("DEVICE_ID") or None,
                                android_id=env.get("ANDROID_ID") or None,
                                kik_node=env.get("BOT_NODE_JID") or None,
                                enable_console_logging=True)
        self.client.wait_for_messages()

    # This method is called when the bot is fully logged in and setup
    def on_authenticated(self):
        self.client.request_roster()  # request list of chat partners

    # This method is called when the bot receives a direct message (chat message)
    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        self.client.send_chat_message(chat_message.from_jid, f'You said "{chat_message.body}"!')

    # This method is called when the bot receives a chat message in a group
    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        if chat_message.body.startswith("!echo "):
            self.client.send_chat_message(chat_message.group_jid, chat_message.body[6:])

    # This method is called if a captcha is required to login
    def on_login_error(self, login_error: LoginError):
        if getattr(login_error, "captcha_url", None):
            login_error.solve_captcha_wizard(self.client)


if __name__ == '__main__':
    # Creates the bot and start listening for incoming chat messages
    callback = EchoBot()
