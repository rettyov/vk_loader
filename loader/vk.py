import vk_api


class Vk(vk_api.VkApi):
    def __init__(self, configs, **kwargs):
        login = configs['auth']['login']
        password = configs['auth']['password']
        super().__init__(login, password, **kwargs)

    def log_in(self):
        try:
            self.auth()
            print('Successful authorization!', end='\n\n')
        except vk_api.AuthError as error_msg:
            print(error_msg)
        return self.get_api()
