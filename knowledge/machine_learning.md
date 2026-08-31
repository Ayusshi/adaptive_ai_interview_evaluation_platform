# Machine Learning Knowledge Base

## Overfitting

Overfitting occurs when a model learns the training data too closely, including noise and patterns that do not generalize.

An overfit model usually performs very well on training data but poorly on unseen validation or test data.

## Underfitting

Underfitting occurs when a model is too simple to learn the important patterns in the data.

An underfit model performs poorly on both training and unseen data.

## Diagnosing Overfitting

A common way to identify overfitting is to compare training and validation or test performance.

A large gap between training performance and validation performance can indicate overfitting.

## Reducing Overfitting

Common techniques include:

- Regularization
- Reducing model complexity
- Cross-validation
- Dropout for neural networks
- Early stopping
- Data augmentation
- Increasing the amount of training data

## Model Evaluation

Training performance alone is not sufficient to determine whether a model generalizes well.

Validation and test performance should also be considered.