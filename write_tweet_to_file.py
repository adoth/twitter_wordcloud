from requests_oauthlib import OAuth1Session
from time import sleep
from twitter_wordcloud.setting import CK, CS, AT, AS


URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'


def get_response(request, params):
    res = request.get(URL, params=params)
    res.raise_for_status()
    limit = res.headers['x-rate-limit-remaining']
    print('The remaining {}'.format(limit))
    if limit == 1:
        sleep(60 * 15)
    return res


def write_tweet(timeline, file):
    if not timeline:
        return
    for tweet_index in range(len(timeline)):
        text = timeline[tweet_index]['text']
        tweet = text.split('http')[0].replace('\n', '')
        if tweet:
            file.write(tweet + '\n')


def access_api(request, params, file):
    for _ in range(100):
        res = get_response(request, params)
        timeline = res.json()
        write_tweet(timeline, file)
        if timeline:
            params['max_id'] = timeline[len(timeline)-1]['id'] - 1
        else:
            break


def write_tweet_to_file(user_name):
    print('--- start writing ---')
    params = {'screen_name': user_name,
              'exclude_replies': True,
              'include_rts': False,
              'count': 200}

    request = OAuth1Session(CK, CS, AT, AS)
    file_name = '{}.csv'.format(user_name)
    file_path = 'tweet/{}'.format(file_name)

    with open(file_path, 'w', encoding='UTF-8') as f:
        access_api(request, params, f)

    print('--- finish writing ---')
    return file_path

