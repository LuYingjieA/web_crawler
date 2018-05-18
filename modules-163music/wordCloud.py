import jieba.analyse
from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

# 先读取热歌榜歌曲的评论
with open("song_comments.txt", encoding="utf8") as f:
    # print(f.read())
    comments = f.read()

# 开始 jieba 分词
result = jieba.analyse.textrank(comments, topK=50, withWeight=True)
words = dict()
for i in result:
    words[i[0]] = i[1]
print(words)

# 这里选择一张背景图
image = Image.open("../source/1.png")
graph = np.array(image)
wc = WordCloud(font_path="../source/simhei.ttf", background_color="White", max_words=50, mask=graph)
wc.generate_from_frequencies(words)
image_color = ImageColorGenerator(graph)
plt.imshow(wc)
plt.imshow(wc.recolor(color_func=image_color))
plt.axis("off")
plt.show()
wc.to_file('comments.png')

