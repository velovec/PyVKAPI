import requests
import getpass
import urllib
import pickle
import os

APP_ID = "2054573"
APP_TOKEN = "KUPNPTTQGApLFVOVgqdx"
APP_SCOPE = "friends,groups,photos,audio,video,offline"


class VKApi:

    def __init__(self):
        if os.path.exists('vk_api.dat'):
            data = pickle.load(open('vk_api.dat'))
            self.access_token = data['ACCESS_TOKEN']
        else:
            user_name = raw_input("Enter your VK Login: ")
            pass_word = getpass.getpass("Enter your VK Password: ")

            self.access_token = self.auth(user_name, pass_word)

            pickle.dump({
                'ACCESS_TOKEN': self.access_token,
            }, open('vk_api.dat', 'w'))

    def auth(self, login, password):
        out = requests.get("https://oauth.vk.com/token?" + urllib.urlencode({
            "grant_type": "password",
            "client_id": APP_ID,
            "client_secret": APP_TOKEN,
            "username": login,
            "password": password,
            "scope": APP_SCOPE
        })).json()

        if "access_token" not in out:
            print out
        return out["access_token"]

    def call(self, method, **call_params):
        params = {
            'access_token': self.access_token,
        }
        params.update(call_params)

        request_params = "&".join(["%s=%s" % (str(key), urllib.quote(str(params[key]))) for key in params.keys()])
        request_url = "https://api.vk.com/method/" + method + "?" + request_params

        resp = requests.get(request_url).json()

        if "error" in resp:
            raise Exception("ERROR: " + str(resp))
        else:
            return resp["response"]