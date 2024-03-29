"""This module implements a deep learning model to classify road signs.

Time spent:
Reading the problem specification: 20 minutes
Implementation & experimentation: 100 minutes
Write-up: 25 minutes
Documentation & formatting: 5 minutes
Total: 150 minutes

Examples:
    $ python3 traffic.py gtsrb
"""
import os
import sys

import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def load_data(data_dir: str) -> tuple:
    """Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered 0
     through NUM_CATEGORIES - 1. Inside each category directory will be some
     number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all of the
     images in the data directory, where each image is formatted as a numpy
     ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should be a
     list of integer labels, representing the categories for each of the
     corresponding `images`.

    Args:
        data_dir (str): Directory containing image data.

    Returns:
        tuple: (images, labels).
    """
    # cv2 to load images as np.arrays
    # loop over folders, then over files
    images, labels = [], []
    for category in os.listdir(data_dir):
        category_path = os.path.join(data_dir, category)
        if not os.path.isdir(category_path):
            # issues with .DS_Store files on MacOS
            continue

        for file in os.listdir(category_path):
            file_path = os.path.join(category_path, file)
            img = cv2.imread(file_path)
            # resize to IMG_WIDTH, IMG_HEIGHT
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            images.append(img)
            labels.append(int(category))

    return images, labels


def get_model() -> keras.Model:
    """Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`. The
     output layer should have `NUM_CATEGORIES` units, one for each category.

    Returns:
        keras.Model: Compiled Keras model.
    """
    # should be a global param but not sure if grading server is importing
    # functions + executing or executing complete modules
    DROPOUT = 0.5

    # input size is (IMG_WIDTH, IMG_HEIGHT, 3)
    inputs = keras.Input((IMG_WIDTH, IMG_HEIGHT, 3))

    # block 1
    x = layers.Conv2D(filters=32,
                      kernel_size=(3, 3),
                      padding='valid',
                      activation='relu',
                      use_bias=True)(inputs)
    x = layers.Conv2D(filters=64,
                      kernel_size=(3, 3),
                      padding='valid',
                      activation='relu',
                      use_bias=True)(x)
    block_1_output = layers.MaxPool2D(pool_size=(3, 3))(x)

    # block 2
    x = layers.Conv2D(filters=64,
                      kernel_size=(3, 3),
                      padding='same',
                      activation='relu',
                      use_bias=True)(block_1_output)
    x = layers.Conv2D(filters=64,
                      kernel_size=(3, 3),
                      padding='same',
                      activation='relu',
                      use_bias=True)(x)
    block_2_output = layers.Add()([x, block_1_output])

    # extra convolutional layer, ResNet style finish
    x = layers.Conv2D(filters=64,
                      kernel_size=(3, 3),
                      padding='valid',
                      activation='relu',
                      use_bias=True)(block_2_output)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(rate=DROPOUT)(x)
    outputs = layers.Dense(NUM_CATEGORIES)(x)

    model = keras.Model(inputs, outputs)
    loss_fxn = keras.losses.CategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam', loss=loss_fxn, metrics=['accuracy'])

    return model


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(np.array(images),
                                                        np.array(labels),
                                                        test_size=TEST_SIZE)

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


if __name__ == "__main__":
    main()
