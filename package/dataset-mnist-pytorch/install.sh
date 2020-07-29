#! /bin/bash

echo -e "import torchvision\ntorchvision.datasets.MNIST('.', download=True)" | python
