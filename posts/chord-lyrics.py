from collections import Counter
import numpy as np 
import nltk
from nltk import bigrams  
import mne.viz 
import matplotlib.pyplot as plt
import matplotlib

def co_occurrence_matrix(corpus):
    vocab = set(corpus)
    vocab = list(vocab)
    vocab_to_index = { word:i for i, word in enumerate(vocab) }
    bi_grams = list(bigrams(corpus))
    bigram_freq = nltk.FreqDist(bi_grams).most_common(len(bi_grams))
    matrix = np.zeros((len(vocab), len(vocab)))
    for bigram in bigram_freq:
        current = bigram[0][1]
        previous = bigram[0][0]
        count = bigram[1]
        p_curr = vocab_to_index[current]
        p_prev = vocab_to_index[previous]
        matrix[p_curr][p_prev] = count 
    return matrix, vocab


song = '''Work it
Make it
Do it
Makes us
Harder
Better
Faster
Stronger
More than
Hour
Hour
Never
Ever
After
Work is
Over
Work it
Make it
Do it
Makes us
Harder
Better
Faster
Stronger
Work it harder, make it better
Do it faster, makes us stronger
More than ever, hour after hour
Work is never over
Work it harder, make it better
Do it faster, makes us stronger
More than ever, hour after hour
Work is never over
Work it harder, make it better
Do it faster, makes us stronger
More than ever, hour after hour
Work is never over
Work it harder, make it better
Do it faster, makes us stronger
More than ever, hour after hour
Work is never over
Work it harder, make it better
Do it faster, makes us stronger
More than ever, hour after hour
Work is never over
Work it harder, make it better
Do it faster, makes us
More than ever hour after hour
Work is never over
Work it harder, make it better
Do it faster, makes us stronger
More than ever, hour after hour
Work is never over
Work it harder, make it
Do it faster, makes us
More than ever, hour after hour
Work is never over
Work it harder, make it better
Do it faster, makes us stronger
More than ever, hour after hour
Work is never over
Work it, make it better
Do it faster makes us stronger
More than ever, hour after hour
Work is never over
Work it, make it better
Do it faster makes us stronger
More than ever, hour after hour
Work is never over
Work it, make it better
Do it faster makes us stronger
More than ever, hour after hour
Work is never over
Work it harder
Do it faster
More than ever, hour
Work is never over
Work it harder, make it better
Do it faster makes us stronger
More than ever hour after hour
Work is never over'''.replace('\n', ' ').replace(',', '').replace('.', ' ').lower()

matrix, vocab = co_occurrence_matrix(song.split())
fig = plt.figure(figsize = (8,8), facecolor='black')
matplotlib.rcParams['font.family'] = 'monospace'
ax = fig.add_axes(rect = (0, 0, 1, 1), projection = 'polar')
fig, axes = mne.viz.circle._plot_connectivity_circle(matrix, vocab,ax=ax, colormap='gist_ncar', colorbar_size=.5, title ='Harder, Better, Faster, Stronger\n\nby Daft Punk')
fig.savefig('daft_punk.png', dpi = 300)