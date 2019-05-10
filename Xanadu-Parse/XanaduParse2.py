import pandas as pd 
import numpy as np
train = pd.read_csv(r'c:\users\markg\downloads\repositories\xanadu-parse\xanadu-parse\train.csv', sep='|')
train_input = train['Altered File Name']
train_output = train['Resolution']
test = pd.read_csv(r'c:\users\markg\downloads\repositories\xanadu-parse\xanadu-parse\test.csv', sep='|')
test_input = test['Altered File Name']
test_output = test['Resolution']
total_inputs = train_input.append(test_input, ignore_index=True)


# Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

tokenizer_obj = Tokenizer()
tokenizer_obj.fit_on_texts(total_inputs)
max_length = max([len(s.split()) for s in total_inputs])
vocab_size = len(tokenizer_obj.word_index) + 1
train_input_tokens = tokenizer_obj.texts_to_sequences(train_input)
test_input_tokens = tokenizer_obj.texts_to_sequences(test_input)
train_input_pad = pad_sequences(train_input_tokens, maxlen=max_length, padding='post')
test_input_pad = pad_sequences(test_input_tokens, maxlen=max_length, padding='post')

# fuck this
train_output = pd.get_dummies(train_output,prefix=['Resolution'], dummy_na=True)

# Model
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GRU
from keras.layers.embeddings import Embedding
embedding_dim = 100
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_length))
model.add(GRU(units=32, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(10,activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(train_input_pad, train_output.values, batch_size=32, epochs=25, validation_data=(test_input_pad, test_output), verbose=2)