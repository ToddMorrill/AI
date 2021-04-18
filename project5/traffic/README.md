# Experiment Results

**Experiment 1:** Vanilla CNN
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.2
- fully connected -> num_classes
- softmax

accuracy: 0.9194

**Experiment 2:** Vanilla CNNm higher dropout
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.5
- fully connected -> num_classes
- softmax

accuracy: 0.8559

**Experiment 3:** Multilayer CNN
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- convolutional layer with 64 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.2
- fully connected -> num_classes
- softmax

accuracy: 0.9763

**Experiment 3:** Multilayer CNN with Residual Connection
- input
- block 1
    - convolutional layer with 32 3x3 filters with no padding, ReLU activation
    - convolutional layer with 64 3x3 filters with no padding, ReLU activation
- block 2
    - convolutional layer with 64 3x3 filters with no padding, ReLU activation
    - convolutional layer with 64 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.2
- fully connected -> num_classes
- softmax

accuracy: 0.9763