# -*- coding: utf-8 -*-
"""RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fYITvHv1gOiopD6Nsly_7EBv-uHWLRB6
"""

import tensorflow as tf
tf.test.gpu_device_name()

from google.colab import drive
drive.mount('/content/drive')

from tensorflow.python.client import device_lib
device_lib.list_local_devices()


import sys
sys.path.append('/content/drive/My Drive')

#loading all the libraries
from time import time
import pandas as pd

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

import tensorflow as tf


from tensorflow.python.keras.models import Model, Sequential
from keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.layers import Input, Embedding, LSTM, GRU, Conv1D, Conv2D, GlobalMaxPool1D, Dense, Dropout,SpatialDropout1D
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from util import make_w2v_embeddings
from keras.utils import to_categorical
from util import split_and_zero_padding
from util import ManDist
from util import text_to_word_list
from keras.optimizers import SGD
from sklearn.preprocessing import OneHotEncoder
import numpy as np

TRAIN_EXCEL = '/content/drive/My Drive/MALSTM_V3-1.xlsx'

train_df = pd.read_excel(TRAIN_EXCEL)
for q in ['Resume', 'JD','Score']:
    train_df[q + '_n'] = train_df[q]

train_df

embedding_dim = 300
max_seq_length = 70
use_w2v = True

import nltk
nltk.download('stopwords')

train_df, embeddings = make_w2v_embeddings(train_df, embedding_dim=embedding_dim, empty_w2v=use_w2v)

train_df['Score_n'],embeddings

validation_size = int(len(train_df) * 0.3)
print(validation_size)
training_size = len(train_df) - validation_size
print(training_size)

X = train_df[['Resume_n', 'JD_n']]
X

train_df.loc[train_df['Score'] == 5, 'LABEL'] = 4
train_df.loc[train_df['Score'] == 4, 'LABEL'] = 3
train_df.loc[train_df['Score'] == 3, 'LABEL'] = 2
train_df.loc[train_df['Score'] == 2, 'LABEL'] = 1
train_df.loc[train_df['Score'] == 1, 'LABEL'] = 0
train_df

Y = to_categorical(train_df['Score'])
Y

X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size)

X_train = split_and_zero_padding(X_train, max_seq_length)
X_validation = split_and_zero_padding(X_validation, max_seq_length)

assert X_train['left'].shape == X_train['right'].shape
assert len(X_train['left']) == len(Y_train)

batch_size = 16
n_epoch = 50
n_hidden = 100
n_most_common_words = 5000
n_epoch

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential()
model.add(Embedding(n_most_common_words, embedding_dim, input_length= max_seq_length))
model.add(SpatialDropout1D(0.3))
model.add(layers.SimpleRNN((256), dropout=0.3, recurrent_dropout=0.3))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='softmax'))
shared_model = model

left_input = Input(shape=(max_seq_length,), dtype='int32')
right_input = Input(shape=(max_seq_length,), dtype='int32')

rnn_distance = ManDist()([shared_model(left_input), shared_model(right_input)])
model = Model(inputs=[left_input, right_input], outputs=[rnn_distance])
model

left_input = Input(shape=(max_seq_length,), dtype='int32')
right_input = Input(shape=(max_seq_length,), dtype='int32')
# opt = SGD(lr=0.01, momentum=0.9)
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
print(model.summary())

training_start_time = time()
rnn_trained = model.fit([X_train['left'], X_train['right']], Y_train,
                           batch_size=batch_size,epochs=n_epoch,
                           validation_data=([X_validation['left'], X_validation['right']], Y_validation),callbacks=[EarlyStopping(monitor='val_loss',patience=7, min_delta=0.0001)])

training_end_time = time()
print("Training time finished.\n%d epochs in %12.2f" % (n_epoch,
                                                        training_end_time - training_start_time))

model.save('./data/RNN.h5')

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
plt.plot(rnn_trained.history['accuracy'])
plt.plot(rnn_trained.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='best')
plt.savefig('./data/Accuracy.png')

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
plt.plot(rnn_trained.history['loss'])
plt.plot(rnn_trained.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='best')
plt.savefig('./data/loss.png')

print(str(rnn_trained.history['accuracy'][-1])[:6] +
      "(max of accuracy out of all the epochs trained: " + str(max(rnn_trained.history['accuracy']))[:6] + ")")

print(str(rnn_trained.history['val_accuracy'][-1])[:6] +
      "(max of val_accuracy of all the epochs trained: " + str(max(rnn_trained.history['val_accuracy']))[:6] + ")")
print("Done.")