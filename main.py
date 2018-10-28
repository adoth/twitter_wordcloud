from twitter_wordcloud.create_wordcloud_picture import create_wordcloud_picture
from twitter_wordcloud.write_tweet_to_file import write_tweet_to_file


def main():
    user_name = '@{}'.format(input('account_id > @'))
    file_path = write_tweet_to_file(user_name)
    create_wordcloud_picture(file_path, user_name)


if __name__ == '__main__':
    main()
