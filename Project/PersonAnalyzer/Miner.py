from vk.exceptions import VkAPIError
import vk
import pandas as pd
from PersonAnalyzer.Bag_of_Words import Bag_Words
import re
import collections
import time

class Miner(object):
    api = None

    def init(self, api):
        self.api = api
        print('Введите номер режима:')
        print('1 Текст пользователей групп')
        print('2 Обработать текст из файла')
        inp = str(input())

        if(inp == '1' or inp == '2' or inp == '3'):
            if (inp == '1'):
                print('Введите айди группы')
                p = re.compile('[0-9]')
                inp = str(input())
                if p.match(inp) == None:
                    print('Введент недопустимый символ')
                    self.init(api)
                else:
                    self.get_users_group_text(inp, api)

            if (inp == '2'):
                print('Введите айди группы')
                p = re.compile('[0-9]')
                inp = str(input())
                if p.match(inp) == None:
                    print('Введент недопустимый символ')
                else:
                    self.clean_data(inp)

            if (inp == '3'):

                deq = collections.deque(maxlen=1000000000)
                for i in range(100):
                    print(i)
                    self.get_photo_text(58914437)
                    # deq = collections.deque(maxlen=100000000000)
                    self.get_time(1000000000, deq)

        else:
            print('Введен неправильный номер, попробуйте еще раз!')
            self.init(api)


    def get_time(self, t, deq):
        deq.appendleft(time.time())
        if len(deq) == t:
            time.sleep(max(1 + deq[3] - deq[0], 0))

    def get_users_group_text(self, id, api):
        members = self.api.groups.getMembers(group_id=id)
        df = pd.DataFrame(columns=['id', 'text'])

        deq = collections.deque(maxlen=4)

        for i in range(len(members['items'])):
            if (self.__check_account(members['items'][i], api)):

                self.get_time(4, deq)

                text = self.get_text_data(members['items'][i], deq)
                d = {'id': [members['items'][i]], 'text': text}
                ndf = pd.DataFrame(data=d)
                df = pd.concat([df, ndf])

        df.to_csv('{}.csv'.format(id))

    def clean_data(self, id):
        bw = Bag_Words
        nlp = bw.init(bw)
        df = pd.read_csv('{}.csv'.format(id))
        cleaned_data = bw.bag_of_words(bw, df, nlp)

        cleaned_data.to_csv('output_group.csv')

    def __check_account(self, us_id, api):
        try:
            user = api.users.get(user_ids=us_id,
                                 fields='photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group')

            print('Обрабатывается: {} {} {}'.format(user[0]['first_name'], user[0]['last_name'], user[0]['id']))
            if (user[0].get('deactivated') != None):
                print('deactivated account: {}'.format(user[0]['id']))
                return False
            elif (user[0]['is_closed'] == 'True'):
                print('private account: {}'.format(user[0]['id']))
                return False
            else:
                return True
        except VkAPIError as e:
            if e.code == 18:
                #                 or VkAPIError.code == 30 or VkAPIError.code == 113 or VkAPIError.code == 203:
                print('account #{} is closed or deactivated!'.format(user[0]['id']))
                return False

    def get_text_data(self, us_id, deq):
        k = ''
        text = self.__get_wall_text(us_id)
        k = k + ' ' + text

        self.get_time(500000, deq)

        text = self.get_photo_text(us_id)
        k = k + ' ' + text

        self.get_time(500000,deq)

        text = self.__get_video_text(us_id)
        k = k + ' ' + text

        self.get_time(500000, deq)

        text = self.__get_groups_text(us_id)
        k = k + ' ' + text
        return k

    def __get_wall_text(self, us_id):
        wall = self.api.wall.get(owner_id=us_id)
        text = ''
        for i in range(len(wall['items'])):
            text = text + ' ' + wall['items'][i]['text']
            if (wall['items'][i].get('copy_history') != None):
                for j in range(len(wall['items'][i]['copy_history'])):
                    text = text + ' ' + wall['items'][i]['copy_history'][j]['text']
                    if (wall['items'][i]['copy_history'][j].get('attachments') != None):
                        for k in range(len(wall['items'][i]['copy_history'][j]['attachments'])):
                            if (wall['items'][i]['copy_history'][j]['attachments'][k].get('photo') != None):
                                text = text + ' ' + wall['items'][i]['copy_history'][j]['attachments'][k]['photo'][
                                    'text']
        return text

    def get_photo_text(self, us_id):
        text = ''
        deq = collections.deque(maxlen=1000000000)
        # self.get_time(15, deq)
        photo = self.api.photos.getAll(owner_id=us_id)
        for i in range(len(photo['items'])):
            # self.get_time(15, deq)
            text = text + ' ' + photo['items'][i]['text']
        return text

    def __get_video_text(self, us_id):
        video = self.api.video.get(owner_id=us_id)
        text = ''
        for i in range(len(video['items'])):
            text = text + ' ' + video['items'][0]['description']
        return text

    def __get_groups_text(self, us_id):
        groups = self.api.groups.get(user_id=us_id)
        g_info = self.api.groups.getById(group_ids=groups['items'], fields=['description', 'status'])
        text = ''
        for i in range(len(g_info)):
            if (g_info[i].get('name') != None):
                text = text + ' ' + g_info[i]['name']
            if (g_info[i].get('description') != None):
                text = text + ' ' + g_info[i]['description']
            if (g_info[i].get('status') != None):
                text = text + ' ' + g_info[i]['status']
        return text


# TODO: check users with errors
