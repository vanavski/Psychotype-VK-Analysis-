from vk.exceptions import VkAPIError
import vk

class Miner(object):
    api = None

    def init(self, api):
        print('Введите айди пользователя:')
        id = str(input())
        self.api = api
        if (self.__check_account(id, api)):
            user = self.__get_mined_data(id)
            print(user)
        else:
            print('Пользователь скрыт, удален, заблокирован или не существует')
            self.init(api)
        return user

    def __get_mined_data(self, id):
        user = self.api.users.get(user_ids=id,
                             fields='photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group')
        return user

    def __check_account(self, us_id, api):
        try:
            user = api.users.get(user_ids=us_id,
                                 fields='photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group')

            print('friend id: {} '.format(user[0]['id']))
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