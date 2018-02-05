from requests_oauthlib import OAuth1Session
import json
from time import sleep
from setting import CK, CS, AT, AS


def input_data(user_name):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    params = {'screen_name': user_name,
              'exclude_replies': True,
              'include_rts': False,
              'count': 200}

    twitter = OAuth1Session(CK, CS, AT, AS)

    return url, params, twitter


def clean_data(file_name):
    with open(file_name, 'r', encoding="UTF-8") as f:
        texts = []
        for line in f:
            if line != '\n' or line[:4] != 'http':
                text = line.split('http')[0]
                if text != '\n' and text != []:
                    texts.append(text)

    file = open(file_name, 'w', encoding="UTF-8")

    for text in texts:
        file.writelines(text)

    file.close()


def main():
    user_name = user_name
    file_name = file_name
    url, params, twitter = input_data(user_name)
    f_out = open(file_name, 'w', encoding="UTF-8")

    for j in range(3):
        res = twitter.get(url, params=params)

        if res.status_code == 200:

            limit = res.headers['x-rate-limit-remaining']
            print("API remain: " + limit)
            if limit == 1:
                sleep(60 * 15)

            timeline = json.loads(res.text)
            for i in range(len(timeline)):
                if i != len(timeline) - 1:
                    f_out.write(timeline[i]['text'] + '\n')
                else:
                    f_out.write(timeline[i]['text'] + '\n')
                    params['max_id'] = timeline[i]['id'] - 1

    f_out.close()
    clean_data(file_name)


if __name__ == '__main__':
    main()
