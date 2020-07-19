import requests
from datetime import datetime
import time
import settings


access_token = settings.API_KEY
api_version = 5.101
offset = 0
count = 100
owner_id_inputed = input('Введите сообщество: ')
# publicdarkperm   -  проверочная группа

# сделать def. это что бы принимать не только имя, то и когда группа имеет просто id******

check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName', {
        'screen_name': owner_id_inputed,
        'access_token': access_token,
        'v': api_version,
        })
owner_id = (0 - check_inputed.json()["response"]['object_id'])
print(owner_id)

# проверка ввода domain
# print('Ошибка ввода. Перепроверьте, что введенный домен существует')

def posts_collector(access_token, api_version, offset, count, owner_id):
    posts = []
    post_read = 0
    req_wall = requests.get('https://api.vk.com/method/wall.get', {
                # 'domain': domain,
                'owner_id': owner_id,
                'offset': 0,
                'count': 1,
                'access_token': access_token,
                'v': api_version,
                'extended': 1              
                })
    wall_post_number = req_wall.json()['response']['count']
    print(wall_post_number)
    while post_read < wall_post_number:
        req_wall = requests.get('https://api.vk.com/method/wall.get', {
                # 'domain': domain,
                'owner_id': owner_id,
                'offset': post_read,
                'count': count,
                'access_token': access_token,
                'v': api_version,
                'extended': 1
                })
        time.sleep(0.5)
        got_posts = req_wall.json()['response']['items']
        for post in got_posts:
            posts.append({
                'id': post['id'],
                'text': post['text'],
                'date': datetime.fromtimestamp(post['date']).strftime('%d/%m/%y %H:%M'),
                'owner_id': post['owner_id'],
                'post_likes': post['likes']['count']
                })
        post_read += len(got_posts)
        #print(post_read)       
    #print('len posts = ', len(posts))
    print(posts)
    return posts

posts_collector(access_token, api_version, offset, count, owner_id)



posts = posts_collector(access_token, api_version, offset, count, owner_id)


def comments_collector(posts, access_token, api_version, offset, owner_id):
    comments = []
    for post in posts:
        req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                            #'domain': domain,
                            'offset': 0,
                            'count': 100,
                            'access_token': access_token,
                            'v': api_version,
                            'post_id': post['id'],
                            'owner_id': post['owner_id'],
                            'need_likes': 1
                            })
        wall_comm_number = req_comms.json()['response']['count']
        comm_read = len(req_comms.json()['response']['items'])
        # print(req_comms.json()['response']['items'])
        all_comments = req_comms.json()['response']['items']
        for comms in all_comments:
            if comms['thread']['count'] > 0:
                req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                            # 'domain': domain,
                            
                            'offset': 0,
                            'count': 100,
                            'access_token': access_token,
                            'v': api_version,
                            'post_id': post['id'],
                            'comment_id': comms['id'],
                            'owner_id': post['owner_id'],
                            'need_likes': 1
                            })
                thread_comments = req_comms.json()['response']['items']
                for thread_comms in thread_comments:
                    comments.append({
                        'post_id': thread_comms['post_id'],
                        'id_comm': thread_comms['id'],
                        'comms': thread_comms['text'],
                        'count_likes': comms['likes']['count'],
                        'date': datetime.fromtimestamp(thread_comms['date']).strftime('%d/%m/%y %H:%M')
                        })
                comm_read += comms['thread']['count']
            if 'post_id' in comms.keys():  # берем только комменты, где есть post_id (и текст)
                comments.append({
                    'post_id': comms['post_id'],
                    'id_comm': comms['id'],
                    'comms': comms['text'],
                    'count_likes': comms['likes']['count'],
                    'date': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M')
                    })
        while comm_read < wall_comm_number:
            time.sleep(0.5)
            req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                            # 'domain': domain,
                            'offset': comm_read,
                            'count': 100,
                            'access_token': access_token,
                            'v': api_version,
                            'post_id': post['id'],
                            'owner_id': post['owner_id'],
                            'need_likes': 1
                            })
            all_comments = req_comms.json()['response']['items']
            print(len(all_comments))
            for comms in all_comments:
                if comms['thread']['count'] > 0:
                    req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                                # 'domain': domain,
                                'offset': 0,
                                'count': 100,
                                'access_token': access_token,
                                'v': api_version,
                                'post_id': post['id'],
                                'comment_id': comms['id'],
                                'owner_id': post['owner_id'],
                                'need_likes': 1
                                })
                    thread_comments = req_comms.json()['response']['items']
                    for thread_comms in thread_comments:
                        comments.append({
                            'post_id': thread_comms['post_id'],
                            'id_comm': thread_comms['id'],
                            'comms': thread_comms['text'],
                            'count_likes': comms['likes']['count'],
                            'date': datetime.fromtimestamp(thread_comms['date']).strftime('%d/%m/%y %H:%M')
                            })
                    comm_read += comms['thread']['count']
                if 'post_id' in comms.keys():  # берем только комменты, где есть post_id (и текст)
                    comments.append({
                        'post_id': comms['post_id'],
                        'id_comm': comms['id'],
                        'comms': comms['text'],
                        'count_likes': comms['likes']['count'],
                        'date': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M')
                        })
            comm_read += len(all_comments)   
        #print('post ok')                 
    #print(f'len comments = {len(comments)}')
    print(comments)
    return comments

comments_collector(posts, access_token, api_version, offset, owner_id)

if __name__ == "__main__":
    print('все отработано')