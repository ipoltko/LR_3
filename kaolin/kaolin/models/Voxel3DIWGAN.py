# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch
import torch.nn as nn
import torch.nn.functional as F


class Voxel3DIWGenerator(nn.Module):
    """TODO: Add docstring.

    https://arxiv.org/abs/1707.09557

    Input shape: B x 200
    Output shape: B x 32 x 32 x 32

    .. note::

        If you use this code, please cite the original paper in addition to Kaolin.
        
        .. code-block::

            @article{DBLP:journals/corr/SmithM17,
              author    = {Edward J. Smith and
                           David Meger},
              title     = {Improved Adversarial Systems for 3D Object Generation and Reconstruction},
              journal   = {CoRR},
              volume    = {abs/1707.09557},
              year      = {2017},
              url       = {http://arxiv.org/abs/1707.09557},
              archivePrefix = {arXiv},
              eprint    = {1707.09557},
              timestamp = {Mon, 13 Aug 2018 16:46:50 +0200},
              biburl    = {https://dblp.org/rec/bib/journals/corr/SmithM17},
              bibsource = {dblp computer science bibliography, https://dblp.org}
            }
    """

    def __init__(self):

        super(Voxel3DIWGenerator, self).__init__()

        self.linear = nn.Linear(200, 256 * 2 * 2 * 2)
        self.post_linear = torch.nn.Sequential(
            torch.nn.BatchNorm3d(256),
            torch.nn.ReLU()
        )

        self.layer1 = torch.nn.Sequential(
            torch.nn.ConvTranspose3d(256, 256, kernel_size=4, stride=2,
                                     padding=(1, 1, 1)),
            torch.nn.BatchNorm3d(256),
            torch.nn.ReLU()
        )
        self.layer2 = torch.nn.Sequential(
            torch.nn.ConvTranspose3d(256, 128, kernel_size=4, stride=2,
                                     padding=(1, 1, 1)),
            torch.nn.BatchNorm3d(128),
            torch.nn.ReLU()
        )
        self.layer3 = torch.nn.Sequential(
            torch.nn.ConvTranspose3d(128, 64, kernel_size=4, stride=2,
                                     padding=(1, 1, 1)),
            torch.nn.BatchNorm3d(64),
            torch.nn.ReLU()
        )
        self.layer4 = torch.nn.Sequential(
            torch.nn.ConvTranspose3d(64, 1, kernel_size=4, stride=2,
                                     padding=(1, 1, 1))
        )

    def forward(self, x):
        x = self.linear(x)
        x = x.view(-1, 256, 2, 2, 2)
        x = self.post_linear(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = x.squeeze(1)
        x = torch.tanh(x[:, :32, :32, :32])
        return x


class Voxel3DIWDiscriminator(nn.Module):
    """TODO: Add docstring.

    https://arxiv.org/abs/1707.09557

    Input shape: B x 32 x 32 x 32
    Output shape: B x 1
    """

    def __init__(self):

        super(Voxel3DIWDiscriminator, self).__init__()

        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv3d(1, 32, kernel_size=4, stride=2),
            torch.nn.LeakyReLU(.2)
        )
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv3d(32, 64, kernel_size=4, stride=2),
            torch.nn.LeakyReLU(.2)
        )
        self.layer3 = torch.nn.Sequential(
            torch.nn.Conv3d(64, 128, kernel_size=4, stride=2),
            torch.nn.LeakyReLU(.2)
        )
        self.layer4 = torch.nn.Sequential(
            torch.nn.Conv3d(128, 256, kernel_size=2, stride=2),
            torch.nn.LeakyReLU(.2)
        )
        self.layer5 = nn.Linear(256, 1)

    def forward(self, x):
        x = x.view(-1, 1, 32, 32, 32)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = x.view(x.shape[0], -1)
        x = self.layer5(x)
        return x
