from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
#from keras.layers import Flatten
#from keras.preprocessing.text import text_to_word_sequence
#from keras.preprocessing.text import one_hot
#from keras.preprocessing.text import Tokenizer
import pandas as pd 
import numpy as np

# Training dataset
train = pd.read_csv(r'c:\users\markg\downloads\repositories\xanadu-parse\xanadu-parse\train.csv', sep='|')
train_input = train[['Altered File Name','Content Type']]
train_output = train[['Title','Season','Episode','Resolution']]
line_count = train_input['Altered File Name'].count()
train_input = train_input.values.reshape(1,line_count,2)
train_output = train_output.values.reshape(1,line_count,4)

## Testing dataset
#test = pd.read_csv(r"C:\Users\Markg\Downloads\Repositories\Xanadu-Parse\Xanadu-Parse\test.csv", sep='|')
#test_input = test[['Altered File Name','Content Type']]
#test_output = test[['Title','Season','Episode','Resolution']]

# Build the model: a single LSTM
model = Sequential()
model.add(LSTM(4, input_shape=(line_count,2), return_sequences=True))
model.add(LSTM(128, input_shape=(line_count,2), return_sequences=True))
model.add(Dense(20, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

model.fit(train_input, train_output)