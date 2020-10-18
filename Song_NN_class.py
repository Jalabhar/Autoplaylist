import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import callbacks
from keras.regularizers import l2
from sklearn.preprocessing import StandardScaler as Scaler
import numpy as np
import pandas as pd


def Classifier():
    scaler = Scaler()
    es = callbacks.EarlyStopping(
        monitor="val_loss",
        min_delta=0,
        patience=500,
        verbose=0,
        mode="auto",
        baseline=None,
        restore_best_weights=True,
    )
    mc = tf.keras.callbacks.ModelCheckpoint(
        'best_model.h5',
        monitor="val_accuracy",
        verbose=0,
        save_best_only=True,
        save_weights_only=False,
        mode="auto",
        save_freq="epoch",
    )
    in_data = 'clustered.csv'
    data = pd.read_csv(in_data)
    data = data.dropna()
    id = data['id']
    data = data.drop(columns=['id'])
    step = 1
    train_data_0 = data
    train_label = train_data_0['cluster']
    train_data = train_data_0.drop(
        columns=['cluster'])
    train_data = train_data.fillna(0)
    train_label = train_label.fillna(0)
    train_data = scaler.fit_transform(train_data)
    # D = data.drop(columns=['cluster'])
    # D = Scaler.transform()
    n_layers = 2
    model = Sequential()
    model.add(Dense(16, input_dim=len(train_data[0]), activation='relu'))
    for _ in range(n_layers):
        model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense((1 + np.max(train_label.values)), activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    model.fit(train_data, train_label, epochs=250, batch_size=50,
              verbose=2, callbacks=[es, mc], validation_split=0.2)
    model.load_weights('best_model.h5')
    probs = model.predict(train_data)
    predictions = np.argmax(probs, axis=-1)
    P = pd.DataFrame(probs)
    dp = pd.DataFrame(predictions, columns=['predicted_cluster'])
    dp['predicted_prob'] = np.max(probs, axis=-1)
    P.to_csv('Song_Probs.csv', index=False)
    dp.to_csv('Song_preds.csv', index=False)
