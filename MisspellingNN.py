model = Sequential()
model.add(Bidirectional(LSTM(output_size, activation='relu',                       return_sequences=True, dropout=dropout),
                        merge_mode='sum',
                        input_shape=(None, input_size),
                        batch_input_shape=(batch_size, None, input_size)))
model.add(Bidirectional(LSTM(output_size, activation='relu', return_sequences=True,
                             dropout=dropout), merge_mode='sum'))
model.add(Bidirectional(LSTM(output_size, activation='relu', return_sequences=True,
                             dropout=dropout), merge_mode='sum'))
model.compile(loss='mse', optimizer=Adam(
    lr=0.001, clipnorm=1), metrics=['mse'])