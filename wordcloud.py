import csv
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from os import path

d = path.dirname(__file__)


def get_noun(texts):
    t = Tokenizer()
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos == '名詞' or pos == 'カスタム名詞':
                words.append(token.base_form)
    return words


def main():
    with open(file_name, 'r', encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter='\n')
        texts = []
        for line in reader:
            texts.append(line[-1])

    words = get_noun(texts)
    text = ' '.join(words)
    fpath = "meiryob.ttc"
    twitter_mask = np.array(Image.open(path.join(d, 'twitter_mask.png')))
    wc = WordCloud(background_color="white", font_path=fpath, mask=twitter_mask)
    wc.generate(text)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()


main()
