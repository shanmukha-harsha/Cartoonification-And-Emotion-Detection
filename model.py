# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B2Zqql5TJJGWX91k-Wh1O9Tqk5OeZ_5l
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib. pyplot as plt
import numpy as np
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential #Initialise neural network model as a sequential network
from keras.layers import Conv2D #Convolution operation
from keras.layers .normalization import BatchNormalization
from keras.regularizers import 12
from keras.layers import Activation #Applies activation function
from keras.layers import Dropout#Prevents overfitting by randomly converting few outputs to zero
from keras.layers import MaxPooling2D # Maxpooling function
from keras.layers import Flatten# Converting 2D arrays into a 1D linear vector
from keras.layers import Dense # Regular fully connected neural network
from keras import optimizers
from keras.callbacks import ReduceLROnPlateau, Earlystopping, TensorBoard, Modelcheckpoint
from sklearn.metrics import accuracy_score
def load_data(dataset_path):
  data=[]
  test_data = []
  test_labels = []
  labels=[]
  with open(dataset_path, 'r' ) as file :
    for line_no, line in enumerate(file.readlines ()) :
      if 0 < l ine no<= 35887:
        curr_class, line, set_type = line.split(', ')
        image_data = np.asarray([int(x) for x in line.split()]).reshape(48, 48)
        image_data =image_data.astype(np. uint8) / 255 .0
        if (set_type.strip() == 'PrivateTest ' ):
          test_data.append(image_data)
          test_labels.append(curr_class)
        else:
          data.append(image_data)
          labels.append(curr_class)
  test_data = np.expand_dims(test_data, -1)
  test_labels = to_categorical(test_labels, num classes= 7)
  data= np.expand_dims(data, -1)
  labels= to_categorical(labels, num_classes = 7)
  ret urn np.array(data), np .array(labels), np.array(test_data), np .array(test_label s)
dataset_path = "/content/fer2013 .csv"
train_data, train_labels, test_data, test_labels = load_data(dataset_path)
print("Number of images in Training set:", len(train_data))
print("Number of images in Test set :", len(test_data))

epochs= 50
batch_size= 64
learning_rate = 0.001
model = sequential()
model.add(conv2D(64, (3, 3), activation= 'relu' , input_shape=(48, 48,1), kernel_regularizer=l2(0.01)))
model.add(Conv2D(64, (3, 3), padding= 'same',activation= 'relu' ))
model.add(BatchNormali zation())
model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2)))
model.add(Dropout(0 .5))
model.add(conv2D(128, (3, 3), padding= 'same', activation= 'relu' ))
model.add(BatchNormalization())
model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout (0 .5))
model.add(Conv2D(256, (3, 3), padding='same', activation= 'relu'))
model.add(BatchNormalization())
model.add(Conv2D(256, (3, 3), padding= "same", activation= "relu'))
model.add(BatchNormalization())
model.add(Conv2D(256, (3, 3), padding= "same' , activation= 'relu' ))
model.add(BatchNormalization())
model.add(MaxPooling2D (pool_size=(2, 2)))
model.add(Dropout(0.5))
model.add(Conv2D(512, (3, 3), padding= "same", activation='relu'))
model.add(BatchNormalization())
model.add(Conv2D(512, (3, 3), padding= "same ' , activation= 'relu' ))
model.add(BatchNormalization())
model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0 .5))
model.add(Flatten())
model.add(Dense(512, activation='relu') )
model.add(Dropout(0 .5))
model.add(Dense(256, activation=' relu') )
model.add(Dropout(0 .5))
model.add(Dense(128, activation= 'relu' ))
model.add(Dropout(0 .5))
model.add(Dense(64, activation= ' relu' ))
model.add(Dropout(0 .5))
model.add(Dense(7, activation= 'softmax'))
adam = optimizers .Adam(lr = learning_rate)
model.compile(optimizer = adam, loss= 'categorical_crossentropy' , metrics= [ 'accuracy'])
print(model .summary())
lr_reducer = ReduceLROnPlateau(monitor= 'val_loss', factor=0.95, patience=3)
early_stopper = Earlystopping(monitor='val_acc ', min_delta=0, patience=6, mode='auto')
checkpointer = Mode1Checkpoint( '/content/weights.hd5', monitor='val_loss', verbose=l, save_best_only=True)
model.fit(train_data, train_labels,epochs=epochs,batch_size=batch_size, validation_split=0.2,shuffle=True, callbacks=[lr_reducer,checkpointer,early_stopper])
from keras .models import model_from_json
model_json = model.to_json()
with open("/content/model.json", 'V') as json_file:
  json_f i le .write(model_j son)
#serialize weights to HDF5
model.save_weights("/content/model .hs")
print("Saved model to disk")