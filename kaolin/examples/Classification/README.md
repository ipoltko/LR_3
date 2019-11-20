# Train a Pointcloud classifier in 5 lines of code

> **Skill level:** _Beginner_

Kaolin makes 3D deep learning easy, by providing all the _hard_/_tricky_ parts of coding up a 3D DL application. To get a feel for how easy training classifiers on 3D data has become, here's a quick demo.

In this tutorial, we will train a _pointcloud_ classifier, in about five lines of code!

For those who are new to pointclouds, here's how they look like.

<p align="center">
    <img src="../../assets/airplane_points.png">
</p>

We will use the `ModelNet10` dataset for the remainder of this tutorial. The remainder of this tutorial will be broken down into the following components.

- [Downloading ModelNet10](#downloading-modelnet10)
- [DataLoading](#dataloading)
- [Training the pointcloud classifier](#training-the-pointcloud-classifier)
- [Bells and whistles](#bells-and-whistles)

## Downloading ModelNet10

Note that the ModelNet10 dataset is provided ONLY for the convenience of academic research. Should you choose to download it, you must adhere to the original terms and copyright notice of the dataset. For convenience, we reproduce the original copyright from the dataset creators.

```
**Copyright**

All CAD models are downloaded from the Internet and the original authors hold the copyright of the CAD models. The label of the data was obtained by us via Amazon Mechanical Turk service and it is provided freely. This dataset is provided for the convenience of academic research only.
```

The ModelNet10 (10-class subset) dataset is available on the [Princeton ModelNet page](https://modelnet.cs.princeton.edu/). On this page, navigate to the ModelNet10 download link to obtain the dataset. We assume that it is unzipped and extracted to a location `MODELNET_DIRECTORY`.

## Warm-up

Before all the fun-stuff begins, let us import all necessary functions from `kaolin` and `torch`. A bit more on what the following modules do will become clear as we progress.

```
import torch
from torch.utils.data import DataLoader
import kaolin as kal
from kaolin import ClassificationEngine as Engine
from kaolin.datasets import ModelNet10 as ModelNet
from kaolin.models.PointNet import PointNetClassifier as PointNet
from kaolin.transforms import NormalizePointCloud as normpc
```

## Dataloading

Kaolin provides convenience functions to load popular 3D datasets (of course, ModelNet10). Assuming you have [installed Kaolin](../../README.md#installation-and-usage), fire up your favourite python interpreter, and execute the following commands.

```
norm = NormalizePointCloud()
```

This command defines a `transform` that takes in any pointcloud object and _normalizes_ it to be centered at the origin, and have a standard deviation of 1. Much like images, 3D data such as pointclouds need to be normalized for better classification performance.

```
train_loader = DataLoader(ModelNet('/path/to/ModelNet10', categories=['chair', 'sofa'],
                                   split='train', rep='pointcloud', transform=norm, device='cuda:0'),
                          batch_size=12, shuffle=True)
```

Phew, that was slightly long! But here's what it does. It creates a `DataLoader` object for the `ModelNet10` dataset. In particular, we are interested in loading only the `chair` and `sofa` categories. The `split='train'` argument indicates that we're loading the 'train' split. The `rep='pointcloud'` loads up meshes and converts them into pointclouds. The `transform=norm` applies a normalizing transform to each pointcloud. The other parameters are fairly easy to decipher.

Similarly, the test dataset can be loaded up as follows.

```
val_loader = DataLoader(ModelNet('/path/to/ModelNet10', categories=['chair', 'sofa'],
                                 split='test', rep='pointcloud', transform=norm, device='cuda:0'),
                        batch_size=12)
```

## Training the pointcloud classifier

Now that all of the data is ready, we can train our classifier using the `ClassificationEngine` class provided by Kaolin. The following line of code will train and validate a _PointNet_ classifier, which is probably the simplest of pointcloud neural architectures.

```
engine = ClassificationEngine(PointNet(num_classes=2), train_loader, val_loader, device='cuda:0')
engine.fit()
```

This should display a long trail of training/validation stats that go like this:
```
Epoch: 0, Train loss: 0.6302577257156372, Train accuracy: 0.6666666865348816
Epoch: 0, Train loss: 0.608104020357132, Train accuracy: 0.7083333432674408
Epoch: 0, Train loss: 0.5694317619005839, Train accuracy: 0.7222222288449606
Epoch: 0, Train loss: 0.5308908596634865, Train accuracy: 0.7708333432674408
Epoch: 0, Train loss: 0.49486334919929503, Train accuracy: 0.8166666746139526
Epoch: 0, Train loss: 0.46080070237318677, Train accuracy: 0.8472222288449606
Epoch: 0, Train loss: 0.42722116623606, Train accuracy: 0.8690476247242519
Epoch: 0, Train loss: 0.3970450200140476, Train accuracy: 0.8854166716337204
Epoch: 0, Train loss: 0.36996302836471134, Train accuracy: 0.898148152563307
Epoch: 0, Train loss: 0.3460669249296188, Train accuracy: 0.9083333373069763
Epoch: 0, Train loss: 0.3246546902439811, Train accuracy: 0.9166666702790693
...
...
...
Epoch: 9, Val loss: 0.001074398518653652, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0009598819953882614, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0010726014385909366, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0009777292708267023, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0009104261476598671, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0008428172893847938, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0007834221362697592, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0007336708978982643, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0006904241699885461, Val accuracy: 1.0
Epoch: 9, Val loss: 0.0006549106868025025, Val accuracy: 1.0
```

That's it, you've trained your first 3D classifier on pointcloud data using Kaolin!! Read through to find out more bells-and-whistles about the `ClassificationEngine` and how you can configure it.

The code is available in `pointcloud_classification_engine.py`.

For a more explicit example without the `ClassificationEngine` class, please see the code in `pointcloud_classification.py`


## Bells and whistles

The `ClassificationEngine` can be customized to suit your needs.

You can train on other categories by simply changing the `categories` argument passed to the `ModelNet10` dataset object. For example, you can add a `bed` class by running
```
dataset = ModelNet('/path/to/ModelNet10', categories=['chair', 'sofa', 'bed'],
                   split='train', rep='pointcloud', transform=norm, device='cuda:0')
```

You can also configure the parameters of the `PointNet` to your liking. For a more detailed explanation, refer to the documentation of the `PointNetClassifier` class.

Further, you can pass several parameters that configure the learning rate, optimizer, training duration, and more. A detailed description can be accessed from the documentation for the `ClassificationEngine` class.
