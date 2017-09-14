import keras
from keras.models import Model
from keras.layers import Input, Dense
from keras.layers.convolutional import Conv2D, MaxPooling2D


inputs = Input(shape=(32,32,1))
c1 = Conv2D(6, (5,5), input_shape=(32,32,1), activation='sigmoid')(inputs)
s2 = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(c1)
c3 = Conv2D(16, (5,5), activation='sigmoid')(s2)
s4 = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(c3)
c5 = Conv2D(120, (5,5), activation='sigmoid')(s4)
f6 = Dense(84, activation="tanh")(c5)
f7 = Dense(10, activation="softmax")(f6)
model = Model(inputs=inputs, outputs=f7)

model.summary()