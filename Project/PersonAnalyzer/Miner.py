from vk.exceptions import VkAPIError
import vk
import pandas as pd
from PersonAnalyzer.Bag_of_Words import Bag_Words

class Miner(object):
    api = None

    def init(self, api):
        print('Введите айди группы:')
        id = str(input())
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
                user = Bag_Words.bag_of_words(Bag_Words, df)
                ndf = pd.concat([ndf, user])
                ndf = ndf['text'].value_counts()

        print(ndf)
            # else:
            #     print('Пользователь скрыт, удален, заблокирован или не существует')
            #     self.init(api)
        # return user

    def __get_mined_data(self, id):
        user = self.api.users.get(user_ids=id,
                             fields='photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group')
        return user

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
                return False


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

    def get_photo_text(self, us_id):
        text = ''
        photo = self.api.photos.getAll(owner_id=us_id, count=200)
        for i in range(len(photo['items'])):
            text = text + ' ' + photo['items'][i]['text']
        return text

    def get_video_text(self, us_id):
        video = self.api.video.get(owner_id=us_id, count=200)
        text = ''
        for i in range(len(video['items'])):
            text = text + ' ' + video['items'][0]['description']
        return text

    def get_groups_text(self, us_id):
        groups = self.api.groups.get(user_id=us_id)
        g_info = self.api.groups.getById(group_ids=groups['items'], fields=['description', 'status'])
        text = ''
        for i in range(len(g_info)):
            text = text + ' ' + g_info[i]['name'] + ' ' + g_info[i]['description'] + ' ' + g_info[i]['status']
        return text