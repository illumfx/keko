from twitchio import Client

class TwitchClient(Client):
    """Needed for livestream status.
    """

    def __init__(self, env):
        super().__init__(client_id=env.TWITCH_CLIENT_ID, client_secret=env.TWITCH_CLIENT_SECRET)