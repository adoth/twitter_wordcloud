from requests_oauthlib import OAuth1Session
import json
from time import sleep

import twitter_wordcloud.wordcloud as word
from twitter_wordcloud.setting import CK, CS, AT, AS


def input_data(user_name):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    params = {'screen_name': user_name,
              'exclude_replies': True,
              'include_rts': False,
              'count': 200}

    twitter = OAuth1Session(CK, CS, AT, AS)

    return url, params, twitter


def clean_data(file_path):
    with open(file_path, 'r', encoding="UTF-8") as f:
        texts = []
        for line in f:
            if line != '\n' or line[:4] != 'http':
                text = line.split('http')[0]
                if text != '\n' and text != []:
                    texts.append(text)

    file = open(file_path, 'w', encoding="UTF-8")

    for text in texts:
        if text:
            file.writelines(text)

    file.close()


def main():
    print('--- start ---')
    user_name = '@{}'.format(input('account_id > @'))
    file_name = '{}.csv'.format(user_name)
    file_path = 'tweet/{}'.format(file_name)
    url, params, twitter = input_data(user_name)
    f_out = open(file_path, 'w', encoding="UTF-8")

    for j in range(100):
        res = twitter.get(url, params=params)

        if res.status_code == 200:

            limit = res.headers['x-rate-limit-remaining']
            print("API remain: " + limit)
            if limit == 1:
                sleep(60 * 15)

            timeline = json.loads(res.text)
            if not timeline:
                break
            for i in range(len(timeline)):
                if i != len(timeline) - 1:
                    f_out.write(timeline[i]['text'] + '\n')
                else:
                    f_out.write(timeline[i]['text'] + '\n')
                    params['max_id'] = timeline[i]['id'] - 1

    f_out.close()
    print('--- finish file ---')
    clean_data(file_path)
    word.main(user_name, file_path)


if __name__ == '__main__':
    main()
