from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Flatten
from keras.optimizers import RMSprop
import pandas as pd 
import numpy as np

# Training dataset
train = pd.read_csv(r'c:\users\markg\downloads\repositories\xanadu-parse\xanadu-parse\train.csv', sep='|')
train_input = train[['Altered File Name','Content Type']]
train_output = train[['Title','Season','Episode','Resolution']]
line_count = train_input['Altered File Name'].count()
train_input = train_input.values.reshape(1,line_count,2)
train_output = train_output.values.reshape(1,line_count,4)

#automater_inputs = Automater(data_type_dict=input_vars, output_var=None)
#automater_outputs = Automater(data_type_dict=output_vars, output_var=None)
#automater_inputs.fit(train_input)
#automater_outputs.fit(train_output)
#x = automater_inputs.transform(train_input)
#y = automater_outputs.transform(train_output)

## Testing dataset
#test = pd.read_csv(r"C:\Users\Markg\Downloads\Repositories\Xanadu-Parse\Xanadu-Parse\test.csv", sep='|')
#test_input = test[['Altered File Name','Content Type']]
#test_output = test[['Title','Season','Episode','Resolution']]

# Build the model: a single LSTM
model = Sequential()
model.add(LSTM(128, input_shape=(line_count,2), return_sequences=True))
#model.add(Dense(128, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

model.fit(train_input, train_output)