# Experiment Results

**Experiment 1:** Vanilla CNN
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.2
- fully connected -> num_classes

accuracy: 0.9194

**Experiment 2:** Vanilla CNNm higher dropout
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.5
- fully connected -> num_classes

accuracy: 0.8559

**Experiment 3:** Multilayer CNN
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- convolutional layer with 64 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.2
- fully connected -> num_classes

accuracy: 0.9763

**Experiment 3:** Multilayer, Multiblock CNN (really should use a GPU by this point)
- input
- block 1
    - convolutional layer with 32 3x3 filters with no padding, ReLU activation
    - convolutional layer with 64 3x3 filters with no padding, ReLU activation
- block 2
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.2
- fully connected -> num_classes

accuracy: 0.9764

**Experiment 4:** Multilayer, Multiblock CNN with residual connections
- input
- block 1
    - convolutional layer with 32 3x3 filters with no padding, ReLU activation
    - convolutional layer with 64 3x3 filters with no padding, ReLU activation
- block 2
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - add block 1 output to block 2 output (residual connection)
- flatten image
- dropout: 0.2
- fully connected -> num_classes

accuracy: 0.9680

**Experiment 5:** Multilayer, Multiblock CNN with residual connections (basically ResNet architecture), follow ResNet details
- input
- block 1
    - convolutional layer with 32 3x3 filters with no padding, ReLU activation
    - convolutional layer with 64 3x3 filters with no padding, ReLU activation
- block 2
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - add block 1 output to block 2 output (residual connection)
- convolutional layer
- global average pooling
- fully connected (256)
- dropout: 0.5
- fully connected -> num_classes

accuracy: 0.9847

**Experiment 6:** Multilayer, Multiblock CNN with residual connections (basically ResNet architecture), follow ResNet details, add extra block
- input
- block 1
    - convolutional layer with 32 3x3 filters with no padding, ReLU activation
    - convolutional layer with 64 3x3 filters with no padding, ReLU activation
- block 2
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - add block 1 output to block 2 output (residual connection)
- block 3
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - convolutional layer with 64 3x3 filters with padding, ReLU activation
    - add block 2 output to block 3 output (residual connection)
- convolutional layer
- global average pooling
- fully connected (256)
- dropout: 0.5
- fully connected -> num_classes

accuracy: 0.9720

**Experiment 7:** same as experiment 6, but train for 12 epochs (really should be using a validation set for stopping criteria)

accuracy: 0.9807

**Experiment 8:** same as experiment 6, but train for 15 epochs (really should be using a validation set for stopping criteria)

accuracy: 0.9898