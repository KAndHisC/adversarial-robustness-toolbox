# MIT License
#
# Copyright (C) The Adversarial Robustness Toolbox (ART) Authors 2021
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
This module implements the TensorBoard support.
"""

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class SummaryWriter(ABC):
    def __init__(self, tensor_board: str):
        """
        Create summary writer.

        :param tensor_board:
        """
        from tensorboardX import SummaryWriter as SummaryWriterTbx

        if isinstance(tensor_board, str):
            self._summary_writer = SummaryWriterTbx(tensor_board)
        else:
            self._summary_writer = SummaryWriterTbx()

    @property
    def summary_writer(self):
        return self._summary_writer

    @abstractmethod
    def update(self, batch_id, global_step, grad=None, patch=None, estimator=None, x=None, y=None, **kwargs):
        """
        Update the summary writer.

        :param batch_id:
        :param global_step:
        :param grad:
        :param patch:
        :param estimator:
        :param x:
        :param y:
        """
        raise NotImplementedError


class SummaryWriterDefault(SummaryWriter):
    def __init__(
        self,
        tensor_board: str,
        ind_1: bool = False,
        ind_2: bool = False,
        ind_3: bool = False,
        ind_4: bool = False,
        ind_5: bool = False,
    ):
        super().__init__(tensor_board=tensor_board)

        self.ind_1 = ind_1
        self.ind_2 = ind_2
        self.ind_3 = ind_3
        self.ind_4 = ind_4
        self.ind_5 = ind_5

        self.losses = dict()

    def update(
        self,
        batch_id: int,
        global_step: int,
        grad: Optional[np.ndarray] = None,
        patch: Optional[np.ndarray] = None,
        estimator=None,
        x: Optional[np.ndarray] = None,
        y: Optional[np.ndarray] = None,
        **kwargs,
    ):
        """
        Update the summary writer.

        :param batch_id:
        :param global_step:
        :param grad:
        :param patch:
        :param estimator:
        :param x:
        :param y:
        """

        # Gradients
        if grad is not None:
            self.summary_writer.add_scalar(
                "gradients/norm-L1/batch-{}".format(batch_id),
                np.linalg.norm(grad.flatten(), ord=1),
                global_step=global_step,
            )
            self.summary_writer.add_scalar(
                "gradients/norm-L2/batch-{}".format(batch_id),
                np.linalg.norm(grad.flatten(), ord=2),
                global_step=global_step,
            )
            self.summary_writer.add_scalar(
                "gradients/norm-Linf/batch-{}".format(batch_id),
                np.linalg.norm(grad.flatten(), ord=np.inf),
                global_step=global_step,
            )

        # Patch
        if patch is not None:
            self.summary_writer.add_image(
                "patch",
                patch,
                global_step=global_step,
            )

        # Losses
        if estimator is not None and x is not None and y is not None:
            if hasattr(estimator, "compute_losses"):
                losses = estimator.compute_losses(x=x, y=y)

                for key, value in losses.items():
                    self.summary_writer.add_scalar(
                        "loss/{}/batch-{}".format(key, batch_id),
                        np.mean(value),
                        global_step=global_step,
                    )

        # Attack Failure Indicators
        if self.ind_1:
            from art.estimators.classification.classifier import ClassifierMixin

            if isinstance(estimator, ClassifierMixin):
                y_pred = estimator.predict(x)
                i_1 = np.argmax(y_pred, axis=1) == np.argmax(y, axis=1)
                self.summary_writer.add_scalars(
                    "Attack Failure Indicator 1 - Silent Success/batch-{}".format(batch_id),
                    {str(i): v for i, v in enumerate(i_1)},
                    global_step=global_step,
                )
            else:
                raise ValueError(
                    "Attack Failure Indicator 1 is only supported for classification, for the current "
                    "`estimator` set `ind_1=False`."
                )

        if self.ind_2:
            losses = estimator.compute_loss(x=x, y=y)

            if str(batch_id) not in self.losses:
                self.losses[str(batch_id)] = list()

            self.losses[str(batch_id)].append(losses)

            i_2 = np.ones_like(losses)

            if len(self.losses[str(batch_id)]) >= 3:

                delta_loss = self.losses[str(batch_id)][0] - self.losses[str(batch_id)][-1]
                delta_step = global_step

                from math import sqrt

                side_b = sqrt(2.0)

                for i_step in range(1, len(self.losses[str(batch_id)]) - 1):

                    side_a = np.sqrt(
                        np.square((self.losses[str(batch_id)][0] - self.losses[str(batch_id)][i_step]) / delta_loss)
                        + (i_step / delta_step) ** 2
                    )
                    side_c = np.sqrt(
                        np.square((self.losses[str(batch_id)][i_step] - self.losses[str(batch_id)][-1]) / delta_loss)
                        + ((delta_step - i_step) / delta_step) ** 2
                    )
                    cos_beta = -(side_b ** 2 - (side_a ** 2 + side_c ** 2)) / (2 * side_a * side_c)

                    i_2_step = 1 - np.abs(cos_beta)
                    i_2 = np.minimum(i_2, i_2_step)

                self.summary_writer.add_scalars(
                    "Attack Failure Indicator 2 - Break-point angle/batch-{}".format(batch_id),
                    {str(i): v for i, v in enumerate(i_2)},
                    global_step=global_step,
                )

        if self.ind_3:
            pass

        if self.ind_4:
            pass

        if self.ind_5:
            pass
