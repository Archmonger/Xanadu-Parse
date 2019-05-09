from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Flatten
from keras.optimizers import RMSprop
import pandas as pd 
import numpy as np

data_type_dict = {'text':['altered file name','content type','altered file name','content type']}
output_vars = ['title','season','episode','resolution']

# Training dataset
train = pd.read_csv(r'c:\users\markg\downloads\repositories\xanadu-parse\xanadu-parse\train.csv', sep='|')
train_input = train[['altered file name','content type']]
train_output = train[['title','season','episode','resolution']]
line_count = train_input['altered file name'].count()

## Testing dataset
#test = pd.read_csv(r"C:\Users\Markg\Downloads\Repositories\Xanadu-Parse\Xanadu-Parse\test.csv", sep='|')
#test_input = test[['Altered File Name','Content Type']]
#test_output = test[['Title','Season','Episode','Resolution']]

# Build the model: a single LSTM
model = Sequential()
model.add(LSTM(128, input_shape=(line_count, 2), return_sequences=True))
model.add(Dense(128, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

model.fit(train_input.values, train_output.values)