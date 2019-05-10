# Training dataset
import pandas as pd 
import numpy as np
train = pd.read_csv(r'c:\users\markg\downloads\repositories\xanadu-parse\xanadu-parse\train.csv', sep='|')
train_input = train[['Altered File Name','Content Type']]
train_output = train['Resolution']
row_count = train['Altered File Name'].count()

# Transform text to word sequences
import nltk
train_input['tk_afn'] = train_input.apply(lambda row: nltk.word_tokenize(row['Altered File Name']), axis=1) #input
train_input = train_input.drop('Altered File Name', axis=1)

# Turn Series/Movie into 0/1
from sklearn.preprocessing import LabelEncoder
le_content_type = LabelEncoder()
train_input['type_encoded'] = le_content_type.fit_transform(train_input['Content Type'])
train_input = train_input.drop('Content Type', axis=1)

# One hot encoding for resolution
train_output = pd.get_dummies(train_output,prefix=['Resolution'], dummy_na=True)

# Convert to MLB encoded format
from sklearn.preprocessing import MultiLabelBinarizer
mlb_afn = MultiLabelBinarizer() # Altered File Names
mlb_data_afn = pd.DataFrame(mlb_afn.fit_transform(train_input['tk_afn']),columns=mlb_afn.classes_, index=train_input.index)
train_input = train_input.drop('tk_afn', axis=1)
train_input = pd.DataFrame(np.concatenate([mlb_data_afn,train_input], axis=1))
input_column_count = len(train_input.columns)

# Reshape data
train_input = train_input.values.reshape(1,row_count,input_column_count)
train_output = train_output.values.reshape(1,row_count,len(train_output.columns))

# Build the model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
model = Sequential()
model.add(LSTM(input_column_count, input_shape=(row_count,input_column_count), return_sequences=True))
model.add(LSTM(128, return_sequences=True))
model.add(Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))
model.fit(x=train_input, y=train_output, verbose=1, epochs=10)
model.evaluate(x=train_input, y=train_output)