from wordcloud import WordCloud
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('netflix_titles.csv')

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ['#AF0404', '#FF0000'])
text = str(list(df['title'])).replace(',', '').replace('[', '').replace("'", '').replace(']', '').replace('.', '')
image = Image.open('Netflix.png')

new_image = Image.new("RGBA", image.size, "WHITE")
new_image.paste(image, mask=image)
mask = np.array(new_image)

wordcloud = WordCloud(background_color = '#252525', font_path='fonts/bebas_neue/BebasNeue-Regular.otf', width = 1000,  height = 400,colormap=cmap, max_words = 150, mask = mask).generate(text)

plt.figure(figsize=(10,10))
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig('netflix.png', dpi = 600)
plt.show()