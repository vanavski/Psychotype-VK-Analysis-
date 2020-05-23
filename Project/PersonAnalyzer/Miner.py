from vk.exceptions import VkAPIError
import vk
import pandas as pd
from PersonAnalyzer.Bag_of_Words import Bag_Words
import re
import time
import collections
import warnings
import openpyxl

class Miner(object):
    api = None
    deq = None

#Обработчик комманд для специальных методов
    def init(self, api):
        self.api = api
        self.deq = collections.deque(maxlen=4)
        print('Введите номер режима:')
        print('1 Обработать группу')
        print('2 Обработать пользователя')
        print('3 Информация о фото пользователя')
        print('4 Получить топ тематик групп пользователя')
        print('5 Получить топ близких друзей по интересам')
        inp = str(input())

        if (inp == '1' or inp == '2' or inp == '3' or inp == '4' or inp == '5' or inp=='0'):
            if (inp == '0'):
                return 0
            if (inp == '1'):
                print('Введите айди группы')
                p = re.compile('[0-9]')
                inp = str(input())
                if p.match(inp) == None:
                    print('Введент недопустимый символ')
                    self.init(api)
                else:
                    self.get_users_group_text(inp, api) #обрабатываются все пользователи группы
                    self.init(api)

            if (inp == '2'):
                print('Введите айди пользователя')
                p = re.compile('[0-9]')
                inp = str(input())
                if p.match(inp) == None:
                    print('Введент недопустимый символ')
                else:
                    if (self.__check_account(inp, self.api)):
                        self.__get_user_data(inp)
                        self.init(api)

            if (inp == '3'):
                print('Введите айди пользователя')
                p = re.compile('[0-9]')
                inp = str(input())
                if p.match(inp) == None:
                    print('Введент недопустимый символ')
                else:
                    if (self.__check_account(inp, self.api)):
                        self.get_photos_info(inp)
                        self.init(api)

            if (inp == '4'):
                print('Введите айди пользователя')
                p = re.compile('[0-9]')
                inp = str(input())
                if p.match(inp) == None:
                    print('Введент недопустимый символ')
                else:
                    if (self.__check_account(inp, self.api)):
                        self.get_group_tematics(inp)
                        self.init(api)

            if (inp == '5'):
                print('Введите айди пользователя')
                p = re.compile('[0-9]')
                inp = str(input())
                if p.match(inp) == None:
                    print('Введент недопустимый символ')
                else:
                    if (self.__check_account(inp, self.api)):
                        self.get_closed_friends(inp)
                        self.init(api)

        else:
            print('Введен неправильный номер, попробуйте еще раз!')
            self.init(api)

    #получает все данные по пользователям из групп
    def get_users_group_text(self, inp, api):
        print('Введите айди группы:')
        id = inp
        self.api = api

        members = api.groups.getMembers(group_id=id)
        ndf = pd.DataFrame(columns=['text', 'count'])

        for i in range(len(members['items'])):
            if (self.__check_account(members['items'][i], api)):
                text = self.__get_text_data(members['items'][i])
                text_sentiment_columns = ['Text']
                data = list()
                data.append(text)
                df = pd.DataFrame(data=data, columns=['Text'])
                cleaned_df = Bag_Words.bag_of_words(Bag_Words, df)

                ndf = pd.concat([ndf, cleaned_df])
                print(ndf)

                # ndf = ndf['text'].value_counts()
                ndf.to_csv('output{}.csv'.format(id))
        print(ndf)

    # получает текстовые данные
    def __get_user_data(self, id):
        ndf = pd.DataFrame(columns=['text', 'count'])
        text = self.__get_text_data(id)
        text_sentiment_columns = ['Text']
        data = list()
        data.append(text)
        df = pd.DataFrame(data=data, columns=['Text'])
        cleaned_df = Bag_Words.bag_of_words(Bag_Words, df)

        ndf = pd.concat([ndf, cleaned_df])
        print(ndf)
        ndf.to_excel('user{}.xlsx'.format(id))
        print('')
        print('Информация хранится в файле user{}.xlsx'.format(id))
        print('')

    #метод проверяет пользователя на существование и наличие ограничений
    def __check_account(self, us_id, api):
        try:
            user = api.users.get(user_ids=us_id,
                                 fields='photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group')

            print('Обрабатывается: {} {}'.format(user[0]['first_name'], user[0]['last_name']))
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
                self.init(api)
                return False

    #метод собирает всевозможные текстовые данные со страницы
    def __get_text_data(self, us_id):
        k = ''
        text = self.get_wall_text(us_id)
        k = k + ' ' + text
        text = self.get_photo_text(us_id)
        k = k + ' ' + text
        text = self.get_video_text(us_id)
        k = k + ' ' + text
        text = self.get_groups_text(us_id)
        k = k + ' ' + text
        return k

        return 0

    #данные со стены
    def get_wall_text(self, us_id):
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

    #данные под фотками
    def get_photo_text(self, us_id):
        text = ''
        photo = self.api.photos.getAll(owner_id=us_id, count=200)
        for i in range(len(photo['items'])):
            text = text + ' ' + photo['items'][i]['text']
        return text

    #данные под видео
    def get_video_text(self, us_id):
        video = self.api.video.get(owner_id=us_id, count=200)
        text = ''
        for i in range(len(video['items'])):
            text = text + ' ' + video['items'][0]['description']
        return text

    #данные групп
    def get_groups_text(self, us_id):
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


    #Получаем статистику по фотографии юзера
    def get_photos_info(self, id):
        photos = self.api.photos.getAll(owner_id=id, extended=1, count=200, no_service_albums=0)
        df = pd.DataFrame(columns=['user_id', 'likes', 'reposts', 'text', 'album_id'])
        for i in range(len(photos['items'])):
            df.loc[i, 'user_id'] = photos['items'][i]['owner_id']
            df.loc[i, 'album_id'] = photos['items'][i]['album_id']
            df.loc[i, 'likes'] = photos['items'][i]['likes']['count']
            df.loc[i, 'reposts'] = photos['items'][i]['reposts']['count']
            df.loc[i, 'text'] = photos['items'][i]['text']
        df = df.sort_values(by='likes', ascending=False)
        df = df.reset_index()
        df = df.drop('index', axis=1)

        avatars = df[df['album_id'] == -6]

        top_count = avatars['likes'][0]
        summ = avatars['likes'].sum()
        summ = summ / len(avatars['likes'])
        print('Среднее кол-во лайков: {}, остальная информация в файле photos_info{}'.format(summ, id))
        df.to_excel('photos_info{}.xlsx'.format(id))
        return df

    #метод чистит от неинформативных тематик групп
    def clean_activities(self, activity):
        while 'Закрытая группа' in activity:
            activity.remove('Закрытая группа')
        while 'Открытая группа' in activity:
            activity.remove('Открытая группа')
        return activity

    #Получить топ тематик групп пользователя
    def get_group_tematics(self, us_id):
        warnings.filterwarnings('ignore')
        a = self.get_groups_activity(us_id)
        a = self.clean_activities(a)
        adf = pd.DataFrame(data=a, columns=['type'])
        uniq = set(a)
        udf = pd.DataFrame(data=uniq, columns=['type'])
        udf['count'] = 0
        for i in range(len(udf)):
            count = adf[adf['type'] == udf['type'][i]].count()
            udf['count'][i] = count
        udf = udf.sort_values(by='count', ascending=False)
        udf = udf.reset_index()
        udf = udf.drop('index', axis=1)
        print('')
        print('Топ тематик групп:')
        print(udf)
        print('')
        udf.to_excel("tematics{}.xlsx".format(us_id))
        return udf


    #получение пересечения джакарда
    def jaccard(self, l1, l2):
        intersec = len(l1.intersection(l2))
        union = len(l1.union(l2))
        return intersec / union

    #получить информацию о группе
    def get_groups_activity(self, id):
        self.deq.appendleft(time.time())
        if len(self.deq) == 4:
            time.sleep(max(1 + self.deq[3] - self.deq[0], 0))
        groups = self.api.groups.get(user_id=id, fields=['activity'], extended=1)
        activities = []
        for group in groups['items']:
            try:
                activities.append(group['activity'])
            except Exception:
                continue
        return activities

    # Получить топ близких друзей
    def get_closed_friends(self, us_id):
        deq = collections.deque(maxlen=4)
        deq.appendleft(time.time())
        if len(deq) == 4:
            time.sleep(max(1 + deq[3] - deq[0], 0))
        my_activities = self.get_groups_activity(us_id)
        df = pd.DataFrame(columns=['friend_name', 'jaccard'])
        i = 0
        friends = self.api.friends.get(user_id=us_id, extended=1, fields='nickname')['items']
        timer = len(friends) / 60 * 0.87
        print('метод займет примерно: {} минут'.format(timer))
        for friend in friends:
            try:
                activities = self.get_groups_activity(friend['id'])
                similarity = self.jaccard(set(my_activities), set(activities))
                friend_name = friend['first_name'] + ' ' + friend['last_name']
                df.loc[i] = [friend_name, similarity]
                i += 1
            except Exception:
                continue
        df = df.sort_values(by='jaccard', ascending=False)
        print('')
        print('Топ близких друзей:')
        print('')
        print(df)
        print('')
        df.to_excel('closedFriends{}.xlsx'.format(us_id))
        return df