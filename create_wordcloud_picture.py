import csv
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np


def get_noun(texts):
    t = Tokenizer('user_dic.csv', udic_type='simpledic', udic_enc='UTF-8')
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos == '名詞' or pos == 'カスタム名詞':
                words.append(token.base_form)
    return words


def create_wordcloud_picture(file_path, photo_name):
    print('--- start wordcloud ---')
    with open(file_path, 'r', encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter='\n')
        texts = []
        for line in reader:
            texts.append(line[-1])

    words = get_noun(texts)
    text = ' '.join(words)
    font_path = "meiryob.ttc"
    stopwords = set(STOPWORDS)
    stopwords |= {'こと', 'そう', 'なに', 'これ', 'よう', 'ちゃん', 'わけ', 'うち', 'とき', 'こっち', 'なん', 'ところ', 'いつ', 'さん', 'すぎ', 'たち'}
    twitter_mask = np.array(Image.open('twitter_mask.jpg'))
    image_colors = ImageColorGenerator(twitter_mask)
    wc = WordCloud(background_color="white", font_path=font_path, mask=twitter_mask, stopwords=stopwords)
    wc.generate(text)
    plt.title(photo_name)
    plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
    wc.to_file('pic/{}.png'.format(photo_name))
    plt.axis("off")
    print('--- show img ---')
    plt.show()
