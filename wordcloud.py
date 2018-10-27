import csv
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
from os import path


d = path.dirname(__file__)


def get_noun(texts):
    t = Tokenizer('user_dic.csv', udic_type='simpledic', udic_enc="utf8")
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos == '名詞' or pos == 'カスタム名詞':
                words.append(token.base_form)
    return words


def main(user_name, file_path):
    print('--- start wordcloud ---')
    with open(file_path, 'r', encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter='\n')
        texts = []
        for line in reader:
            texts.append(line[-1])

    words = get_noun(texts)
    text = ' '.join(words)
    fpath = "meiryob.ttc"
    stopwords = set(STOPWORDS)
    stopwords |= {'こと', 'そう', 'なに', 'これ', 'よう', 'ちゃん', 'わけ', 'うち', 'とき', 'こっち', 'なん', 'ところ', 'いつ', 'さん', 'すぎ'}
    twitter_mask = np.array(Image.open(path.join(d, 'twitter_mask.jpg')))
    image_colors = ImageColorGenerator(twitter_mask)
    wc = WordCloud(background_color="white", font_path=fpath, mask=twitter_mask, stopwords=stopwords)
    wc.generate(text)
    plt.title(user_name)
    plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
    wc.to_file('pic/{}.png'.format(user_name))
    plt.axis("off")
    print('--- show img ---')
    plt.show()
