import vk
from PersonAnalyzer import Miner

class ConfigAPI(object):
    __token = None
    api = None

    def init(self):
        print('Вставьте ссылку в строку браузера для получения токена VK API. ')
        print('https://oauth.vk.com/authorize?client_id=7305133&display=page&scope=status,video,photos,friends,wall,notes,groups,docs&response_type=token&v=5.103&state=123456')
        print('После скопируйте ссылку из браузера и вставьте сюда')
        val = str(input())
        self.__get_token_by_link(val)
        self.__vk_api_on()
        Miner.Miner().init(self.api)


    def __get_token_by_link(self, str):
        arr = str.split('=')
        if(len(arr) >= 2):
            arr2 = arr[1].split('&')
            token = arr2[0]
            print(token)
            self.__token = token
        else:
            print('ссылка повреждена, попробуйте еще раз!')
            print(' ')
            self.init()

    def __vk_api_on(self):
        token = self.__token
        try:
            if(token != None):
                session = vk.Session(token)
                self.api = vk.API(session, v=5.103)

                user = self.api.users.get(user_ids=1) #не работает...

                print('Токен подключен!')
                print(' ')
            else:
                print('Токен отсутствует, попробуйте еще раз!')
                print(' ')
                self.init()
        except Exception:
            print('Токен недействителен или поврежден, попробуйте еще раз')
            print(' ')
            self.init()