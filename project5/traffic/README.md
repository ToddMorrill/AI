# Experimental Overview
**Summary:** The model architectures and their accuracy scores on the test set are reported below. The best result was 99.36% accuracy on the test set after training a ResNet style network for 20 epochs. The submitted code is a smaller network that converges well in the 10 epochs allotted and achieves a test set accuracy of 98.47%.

*Experimental approach*: I started with a small convolutional neural network (CNN) based architecture and gradually increased both the number of layers and the number of blocks in the network (see notes below for a better sense of what a block is). This incremental approach allowed me to get a sense for how impactful certain design decisions had on the network's performance on the test set. By far the most important design decision was to increase the depth of the network, which can be seen by comparing Experiment 1 to Experiment 2, where the test set accuracy increased from 91.94% to 97.63% by simply adding one additional CNN layer. From there, I continued to increase the model depth and observed increasing accuracy scores.

As networks grow deeper, there are concerns about: 1) information loss, and 2) gradient loss at earlier parts of the network. To address this, I introduced residual connections between blocks, which sums state generated earlier in the network with state generated later in the network. Again, this increased the accuracy score on the test set, though it was important to let this model train for longer (20 epochs).

If I continued to develop this system, I would define a validation set (e.g. 10-20% of the training set) and monitor the validation set loss while training as an early stopping criterion. This would allows us to train as long as the validation set loss continued to decrease at the end of each epoch. Furthermore, it would allow us to experiment with hyperparameters more confidently, without concern of target leakage (overfitting to the test set due to the feedback it provides to network design decisions). Finally, I would inspect the data set more closely and consider augmenting the training data set (e.g. introducing noise into the images, shears, rotations, etc.) to increase the amount of training data the model as access to.

# Experimental Results

**Experiment 1:** Vanilla CNN (accuracy: 0.9194)
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.2
- fully connected -> num_classes

**Experiment 2:** Vanilla CNN with higher dropout (accuracy: 0.8559)
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.5
- fully connected -> num_classes

**Experiment 3:** Multilayer CNN (accuracy: 0.9763)
- input
- convolutional layer with 32 3x3 filters with no padding, ReLU activation
- convolutional layer with 64 3x3 filters with no padding, ReLU activation
- 3x3 max pooling
- flatten image
- dropout: 0.2
- fully connected -> num_classes

**Experiment 3:** Multilayer, Multiblock CNN (really should use a GPU by this point) (accuracy: 0.9764)
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

**Experiment 4:** Multilayer, Multiblock CNN with residual connections (accuracy: 0.9680)
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

**Experiment 5:** Multilayer, Multiblock CNN with residual connections (basically ResNet architecture), follow ResNet details (accuracy: 0.9847)
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

**Experiment 6:** Multilayer, Multiblock CNN with residual connections (basically ResNet architecture), follow ResNet details, add extra block (accuracy: 0.9720)
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

**Experiment 7:** same as experiment 6, but train for 12 epochs (really should be using a validation set for stopping criteria) (accuracy: 0.9807)

**Experiment 8:** same as experiment 6, but train for 15 epochs (really should be using a validation set for stopping criteria) (accuracy: 0.9898)

**Experiment 9:** same as experiment 6, but train for 20 epochs (really should be using a validation set for stopping criteria) (accuracy: 0.9936)