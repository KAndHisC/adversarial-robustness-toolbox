# MIT License
#
# Copyright (C) The Adversarial Robustness Toolbox (ART) Authors 2018
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
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import unittest

from os.path import dirname, join
import numpy as np

import tensorflow as tf

tf.compat.v1.disable_eager_execution()
from tensorflow.keras.models import load_model

from art.attacks.extraction.functionally_equivalent_extraction import FunctionallyEquivalentExtraction
from art.estimators.classification.keras import KerasClassifier
from art.estimators.estimator import BaseEstimator, NeuralNetworkMixin
from art.estimators.classification.classifier import ClassifierMixin

from tests.utils import TestBase, master_seed
from tests.attacks.utils import backend_test_classifier_type_check_fail

logger = logging.getLogger(__name__)


@unittest.skipIf(
    tf.__version__[0] != "2" or (tf.__version__[0] == "1" and tf.__version__.split(".")[1] != "15"),
    reason="Skip unittests if not TensorFlow v2 or 1.15 because of pre-trained model.",
)
class TestFastGradientMethodImages(TestBase):
    @classmethod
    def setUpClass(cls):
        master_seed(seed=1234, set_tensorflow=True)
        super().setUpClass()

        cls.n_train = 100
        cls.n_test = 11
        cls.x_train_mnist = cls.x_train_mnist[0 : cls.n_train]
        cls.y_train_mnist = cls.y_train_mnist[0 : cls.n_train]
        cls.x_test_mnist = cls.x_test_mnist[0 : cls.n_test]
        cls.y_test_mnist = cls.y_test_mnist[0 : cls.n_test]

        model = load_model(
            join(*[dirname(dirname(dirname(__file__))), "utils", "data", "test_models",
                "model_test_functionally_equivalent_extraction.h5"])
        )

        np.random.seed(0)
        num_neurons = 16
        img_rows = 28
        img_cols = 28
        num_channels = 1

        x_train = cls.x_train_mnist.reshape(cls.n_train, img_rows, img_cols, num_channels)
        x_test = cls.x_test_mnist.reshape(cls.n_test, img_rows, img_cols, num_channels)

        x_train = x_train.reshape((x_train.shape[0], num_channels * img_rows * img_cols)).astype("float64")
        x_test = x_test.reshape((x_test.shape[0], num_channels * img_rows * img_cols)).astype("float64")

        mean = np.mean(x_train)
        std = np.std(x_train)

        x_test = (x_test - mean) / std

        classifier = KerasClassifier(model=model, use_logits=True, clip_values=(0, 1))

        cls.fee = FunctionallyEquivalentExtraction(classifier=classifier, num_neurons=num_neurons)
        cls.fee.extract(x_test[0:100])

    def setUp(self):
        master_seed(seed=1234, set_tensorflow=True)
        super().setUp()

    def test_critical_points(self):
        critical_points_expected_15 = np.array(
            [
                [
                    3.61953106e00,
                    9.77733178e-01,
                    3.03710564e00,
                    3.88522344e00,
                    -3.42297003e00,
                    -1.13835691e00,
                    -1.99857599e00,
                    -3.46220468e-01,
                    -3.59475588e00,
                    5.51705510e00,
                    -3.19797872e00,
                    -2.04326002e00,
                    1.05123266e00,
                    -4.06901743e00,
                    -1.20838338e00,
                    -2.89548673e00,
                    6.98455648e00,
                    2.85218553e00,
                    8.94698139e-02,
                    -2.37621231e00,
                    1.10785852e00,
                    2.23015480e00,
                    2.80221937e00,
                    -8.44071720e-01,
                    -4.29867814e00,
                    -1.89193948e00,
                    -2.02601143e00,
                    2.32254653e00,
                    5.46957626e00,
                    -1.09054547e00,
                    1.97730390e00,
                    7.13198416e00,
                    -3.48566995e00,
                    4.56309251e00,
                    -3.66508619e00,
                    2.45678983e-01,
                    1.18692621e00,
                    1.24711887e00,
                    -3.64649874e00,
                    -2.60243153e00,
                    -3.64646660e00,
                    -1.47897557e-01,
                    -4.22195494e-01,
                    1.06113047e01,
                    4.82448414e00,
                    -2.42173234e00,
                    1.11818199e-02,
                    4.65699866e00,
                    -1.49483467e00,
                    -4.83696263e-01,
                    -6.94802825e-01,
                    3.76123427e00,
                    -3.81138399e00,
                    -2.44772137e00,
                    1.80214210e00,
                    1.64008567e00,
                    9.98667003e-01,
                    -1.13632143e00,
                    3.14954375e00,
                    7.93954578e00,
                    9.08789028e-01,
                    -1.11114990e00,
                    2.12722866e00,
                    -3.82389751e00,
                    -2.73941016e00,
                    -2.74131238e-01,
                    -1.16791406e01,
                    -4.02691717e00,
                    -2.26112102e00,
                    -5.21371365e00,
                    -3.28863610e00,
                    -1.57028321e00,
                    -5.25291961e00,
                    -2.81473806e00,
                    -1.68024547e00,
                    -5.85965502e-01,
                    3.61981141e00,
                    9.23169673e-02,
                    -2.29606074e-01,
                    4.43114931e-01,
                    -2.80427895e-01,
                    -3.05502037e00,
                    1.91036227e-02,
                    -3.34978609e-01,
                    -3.84499306e00,
                    5.26390356e00,
                    5.38611250e00,
                    -2.63643293e00,
                    -2.00973074e00,
                    -2.36234227e00,
                    2.31791770e00,
                    -2.90647524e00,
                    -6.57321096e-01,
                    -2.36517907e00,
                    5.54615295e-01,
                    -6.27427313e00,
                    5.17139277e00,
                    -1.96714440e00,
                    3.59945621e-01,
                    -4.24878604e-01,
                    -1.08202458e00,
                    -4.80186427e00,
                    2.37278089e00,
                    -1.07572442e00,
                    -1.18075753e-01,
                    -1.17477993e00,
                    -2.93162165e00,
                    1.08992730e00,
                    5.54290231e00,
                    7.98407506e-01,
                    -3.66473517e00,
                    8.67953522e00,
                    -4.19382044e00,
                    -4.08782220e00,
                    9.82618000e00,
                    -7.69520713e-01,
                    -4.73994274e00,
                    -2.81408385e00,
                    2.04409418e00,
                    1.66265593e00,
                    -2.93741552e00,
                    5.99230900e00,
                    -1.73108306e00,
                    -3.28289962e00,
                    3.04322254e00,
                    5.02137877e00,
                    -3.61579148e00,
                    -3.60298823e00,
                    4.68144302e00,
                    -7.55810404e00,
                    -5.54235927e00,
                    4.30331267e00,
                    -8.89694006e-01,
                    -9.95076143e-01,
                    7.36865058e-01,
                    8.20305695e-02,
                    -4.47623746e00,
                    4.75655495e00,
                    5.55126730e00,
                    -2.94169700e-01,
                    -1.31565371e00,
                    9.54222010e00,
                    -9.08849702e-01,
                    -3.74910292e-01,
                    3.80123979e00,
                    6.66898337e00,
                    5.28420510e00,
                    1.10982206e-01,
                    -1.16276421e-01,
                    -5.82332350e00,
                    -1.28205374e00,
                    -1.55599314e00,
                    -4.66205671e00,
                    5.71610805e00,
                    -3.18101923e00,
                    -2.73180879e00,
                    2.55005165e00,
                    3.96954509e00,
                    7.24416286e-01,
                    1.02980621e01,
                    -7.88544755e-01,
                    2.93612566e00,
                    2.02170626e00,
                    5.67092866e00,
                    7.48089944e-01,
                    3.92145589e-01,
                    -4.68662954e00,
                    -5.93709701e-01,
                    6.64027217e00,
                    -1.27973863e00,
                    2.97883110e00,
                    1.27642013e00,
                    4.21654506e00,
                    -3.78209823e00,
                    8.09590708e00,
                    -4.29526503e00,
                    -2.22566713e00,
                    2.96030699e00,
                    6.98973613e-01,
                    3.24672410e00,
                    -2.28418990e00,
                    -1.66599664e00,
                    -5.96027162e-01,
                    3.88214888e00,
                    3.31149846e00,
                    1.49757160e00,
                    -3.66419049e00,
                    3.82181754e00,
                    1.38112419e-01,
                    6.94779206e00,
                    6.54329012e00,
                    -9.26489313e-01,
                    -1.62009512e00,
                    -4.52985187e00,
                    -3.53512243e-02,
                    -1.65790094e00,
                    2.17052203e00,
                    2.61034940e-01,
                    7.56353874e-01,
                    5.47853217e00,
                    -4.01821256e00,
                    1.44572322e00,
                    -4.79746586e-01,
                    3.47357980e00,
                    6.02979833e00,
                    -2.79622692e00,
                    1.69161006e00,
                    -4.23976729e-02,
                    -2.83040527e00,
                    8.38686737e-01,
                    2.03506626e00,
                    1.92358357e00,
                    1.44131202e-02,
                    -9.99430943e-02,
                    -5.40948077e00,
                    -1.80337181e00,
                    2.14607550e00,
                    3.85151903e00,
                    6.16199609e-01,
                    3.65155968e-01,
                    -6.86530386e-02,
                    4.37920573e-01,
                    1.64040341e00,
                    -6.59215215e00,
                    -1.73270323e00,
                    9.93275152e-01,
                    -3.73550020e00,
                    6.74519312e00,
                    3.12660362e-02,
                    5.84485063e00,
                    -4.49976578e00,
                    -4.02337192e00,
                    3.29641448e-01,
                    -6.11525876e00,
                    -3.19811199e-01,
                    1.15945105e00,
                    5.44615523e00,
                    6.57571553e-01,
                    -1.19802935e00,
                    -3.59314573e00,
                    6.02466561e00,
                    -3.47917071e00,
                    -4.20072539e00,
                    -4.51866361e00,
                    4.03811078e00,
                    -3.69489996e00,
                    -1.78012256e00,
                    1.61533135e00,
                    -1.61852848e00,
                    -4.10470488e00,
                    3.45463564e00,
                    3.56905786e00,
                    3.97554912e00,
                    2.66454239e00,
                    2.25804254e00,
                    -6.21473638e00,
                    5.76899253e00,
                    -2.08408059e-01,
                    7.83228855e-01,
                    4.94838720e00,
                    4.38791606e00,
                    1.12105376e00,
                    1.09827474e00,
                    -2.38398204e00,
                    -1.80753680e00,
                    -3.13452494e00,
                    -2.27719704e00,
                    -3.38822700e00,
                    -9.17931670e-01,
                    4.17912953e00,
                    1.27364259e01,
                    -2.03530245e00,
                    -3.29038740e00,
                    5.31179109e00,
                    -1.82267486e00,
                    -2.96119740e00,
                    1.31020764e00,
                    -4.94302867e00,
                    -1.16514227e00,
                    1.72064832e00,
                    2.72220374e-01,
                    2.50415711e00,
                    -4.29456275e-01,
                    1.59994399e00,
                    1.39253228e00,
                    2.22505196e00,
                    -5.05846429e00,
                    -4.35255236e00,
                    4.50001673e-01,
                    -4.27252846e00,
                    -2.87526989e-01,
                    3.17137548e00,
                    4.66601910e00,
                    -5.13815490e00,
                    -3.48299127e00,
                    2.41422025e00,
                    -1.46361301e00,
                    -6.49063866e-01,
                    1.92294782e00,
                    -3.47120162e00,
                    -2.86761934e00,
                    -1.45476737e00,
                    -4.17669035e00,
                    -4.01483069e00,
                    3.30219967e00,
                    -2.59101087e-01,
                    -4.75482758e00,
                    -2.24586949e00,
                    -5.68236958e00,
                    -3.01268930e00,
                    8.22969417e00,
                    7.26630125e-01,
                    1.71985527e00,
                    -9.85474778e-01,
                    9.69749700e-01,
                    2.67490406e00,
                    -4.33992693e00,
                    -4.07251552e-01,
                    6.08129826e00,
                    -3.20237632e00,
                    -2.92346407e00,
                    -2.01013404e00,
                    1.32121409e00,
                    1.15139410e00,
                    3.77379044e00,
                    1.63111624e00,
                    -3.99098443e-01,
                    7.15579205e00,
                    2.03479958e00,
                    -4.87601164e00,
                    1.05765834e01,
                    5.69732614e00,
                    1.18778294e-01,
                    2.86462296e-01,
                    2.49353875e00,
                    -6.36657921e-02,
                    1.08570479e00,
                    4.74854161e00,
                    -4.63241582e00,
                    -6.83954662e-01,
                    4.65345281e00,
                    1.33951496e00,
                    2.90639747e00,
                    -1.72986262e00,
                    -1.56536140e00,
                    -8.05650496e00,
                    -4.82346198e00,
                    3.39824919e-01,
                    3.78664395e00,
                    2.41632152e00,
                    -1.26309772e00,
                    -2.49517893e00,
                    2.20951730e00,
                    -3.85151265e-01,
                    4.81240175e00,
                    4.85709334e-02,
                    -7.60618498e00,
                    -5.42914323e00,
                    5.42941370e00,
                    -3.93630082e00,
                    3.67290378e00,
                    -1.04039267e00,
                    2.71366140e-01,
                    -1.81908310e-01,
                    4.73638654e00,
                    -5.89365669e-01,
                    -3.20289542e-01,
                    -6.35077950e00,
                    5.36441669e-01,
                    9.38127137e-01,
                    1.21089054e00,
                    4.44570135e00,
                    1.05628764e00,
                    9.13779419e-01,
                    6.46336488e00,
                    -5.53683667e00,
                    -1.13017499e00,
                    3.97816303e00,
                    3.43531407e00,
                    3.51956691e00,
                    1.54150627e00,
                    1.65980399e00,
                    4.09252687e00,
                    4.47248858e-01,
                    9.71886644e-01,
                    -1.03825118e00,
                    -2.35130810e-01,
                    -5.97346695e00,
                    4.64660911e00,
                    -3.43276914e-01,
                    7.65585441e00,
                    -5.17010009e-01,
                    1.28424404e00,
                    -6.57013775e-01,
                    -2.72570553e00,
                    3.09863582e00,
                    8.26999588e00,
                    1.08360782e00,
                    2.97499462e-01,
                    -5.28765957e-01,
                    -7.96130693e00,
                    -1.80771840e00,
                    1.74322693e00,
                    4.46006209e00,
                    1.96673988e00,
                    -1.26500012e00,
                    -2.62521339e-01,
                    4.43172806e00,
                    -8.59953375e-01,
                    -2.79203135e00,
                    3.97136669e00,
                    4.83725475e00,
                    -2.36000818e-01,
                    -2.54368931e00,
                    -6.09494471e00,
                    2.97887357e00,
                    -3.11669990e00,
                    -7.49438171e00,
                    7.68609007e00,
                    4.24065149e00,
                    -3.50205849e00,
                    -4.14267291e00,
                    1.29406661e00,
                    -3.29221719e00,
                    4.91285113e00,
                    2.49242470e00,
                    3.03079368e00,
                    -1.16511988e00,
                    1.75569959e-01,
                    3.69572816e00,
                    -2.23354575e00,
                    -1.08249093e00,
                    3.79457820e00,
                    2.46730808e00,
                    -5.62046536e00,
                    -1.63213742e00,
                    1.80517373e00,
                    -1.58217893e00,
                    7.70526692e00,
                    -1.45138939e00,
                    -1.02637577e00,
                    1.83421798e00,
                    1.20008006e00,
                    -3.70929508e-01,
                    -2.06747283e00,
                    1.05799974e00,
                    4.50025041e00,
                    8.99414047e-01,
                    -3.81032447e00,
                    6.64691827e00,
                    -6.68286008e00,
                    -5.33754112e00,
                    4.20039092e00,
                    1.15777816e00,
                    -1.79904165e00,
                    -2.25318912e00,
                    8.56072151e00,
                    -1.74587332e00,
                    2.27772815e00,
                    1.18619882e00,
                    1.17419760e00,
                    1.12252724e00,
                    2.41046828e00,
                    -1.27854741e00,
                    -1.63751443e00,
                    -4.36138109e00,
                    -3.99645147e00,
                    2.61707008e-01,
                    1.77727481e00,
                    2.58218034e00,
                    -3.34194564e00,
                    -5.45410857e00,
                    -1.10816013e01,
                    3.77134811e00,
                    -5.53653174e-01,
                    -7.50458024e-01,
                    1.83105453e00,
                    -6.35106143e00,
                    -2.32310964e-01,
                    8.36876665e00,
                    2.73772575e00,
                    2.42717722e00,
                    -7.06580844e00,
                    8.30491238e00,
                    -4.67310265e00,
                    4.82361105e00,
                    -6.71576571e00,
                    6.02101751e00,
                    6.24969448e00,
                    -2.98703859e00,
                    6.14207232e-01,
                    1.78015104e00,
                    -2.06596331e00,
                    -4.34009099e00,
                    -2.43064707e00,
                    2.03098762e00,
                    -9.89714067e-01,
                    -2.70977210e00,
                    2.74338316e00,
                    1.89889595e00,
                    -2.55656260e00,
                    -4.70778279e00,
                    3.13221251e00,
                    -2.32580294e00,
                    3.85278333e-02,
                    5.55167173e00,
                    3.21784728e-01,
                    -4.92260843e00,
                    -5.54069995e-01,
                    -2.40504807e00,
                    7.15357191e00,
                    -8.09982416e-01,
                    -5.25778915e-01,
                    -7.71322963e-01,
                    -4.04571082e-02,
                    -7.44434946e00,
                    -5.12893117e00,
                    -7.11996760e-01,
                    1.52709995e00,
                    1.20660824e00,
                    -3.94659988e00,
                    -6.15942263e00,
                    -3.24356676e00,
                    -2.71168115e00,
                    2.23742176e00,
                    -2.15833449e00,
                    3.28171007e00,
                    -9.01288903e-01,
                    -3.36544690e00,
                    -4.90099212e-01,
                    -5.28357599e00,
                    2.83366162e00,
                    -1.94060483e00,
                    -1.96470570e00,
                    -1.56417735e00,
                    -5.63317405e00,
                    -1.52587686e00,
                    -2.94973969e00,
                    -1.71309668e00,
                    -3.43045944e-01,
                    -2.89876104e00,
                    -2.06482721e00,
                    4.84964575e00,
                    1.41788617e00,
                    4.07125067e00,
                    9.04277262e-01,
                    4.09024059e00,
                    -5.57238878e00,
                    1.58954316e00,
                    -1.10885879e-01,
                    -2.21962753e00,
                    -3.10507445e00,
                    -4.85573938e00,
                    5.55346782e00,
                    -4.46137455e00,
                    6.53561699e00,
                    -4.18305953e00,
                    -3.33538699e00,
                    1.07412314e00,
                    -3.21736541e00,
                    4.22297199e00,
                    -1.33947330e00,
                    2.06426759e00,
                    -5.54850513e00,
                    2.50551073e00,
                    2.09512318e00,
                    -3.22334697e00,
                    1.08998132e01,
                    2.11009614e00,
                    9.43857355e00,
                    6.67997823e00,
                    -2.56444394e00,
                    -1.56702883e00,
                    -8.01844888e-01,
                    -6.53025150e00,
                    -3.07115943e00,
                    1.54471353e-01,
                    4.81876388e00,
                    -3.13769415e00,
                    4.56491640e00,
                    -6.82529587e00,
                    -2.94109962e00,
                    -2.92035453e00,
                    2.23157087e00,
                    1.22495482e00,
                    3.27356600e00,
                    2.78216232e00,
                    1.39149304e00,
                    1.12641226e00,
                    3.13438737e00,
                    -1.44455956e00,
                    3.45329504e00,
                    -7.25452537e00,
                    5.16350338e-01,
                    -1.52840925e00,
                    3.89239288e-01,
                    3.57665297e00,
                    4.23851729e-01,
                    2.51386164e00,
                    5.55541927e00,
                    -3.65730975e-02,
                    4.97351340e00,
                    -2.21492629e00,
                    2.06160783e-01,
                    -3.43932949e00,
                    3.46787764e00,
                    1.50062470e00,
                    -3.63420781e00,
                    7.16921221e-01,
                    3.67330490e00,
                    -1.89513701e00,
                    -4.99527599e00,
                    1.11835198e00,
                    -6.81027303e00,
                    2.85916379e00,
                    -1.23450647e00,
                    -1.60211378e00,
                    3.73671094e00,
                    -4.02548447e00,
                    6.06862004e00,
                    -1.19202728e00,
                    -2.41783262e00,
                    3.74904207e00,
                    2.45508616e00,
                    9.16190491e00,
                    -2.04793984e00,
                    -2.85129492e-01,
                    -4.08466337e00,
                    -1.34825047e00,
                    -2.80827325e00,
                    -2.43332648e00,
                    -6.90362325e00,
                    6.92712787e00,
                    -5.88185198e00,
                    -1.13563946e01,
                    -4.22056384e00,
                    -3.26737627e00,
                    -4.22009802e00,
                    5.09351493e00,
                    8.23654694e-01,
                    8.38630810e-03,
                    3.74246157e00,
                    2.14720496e00,
                    2.81112013e00,
                    -5.53460662e00,
                    -2.43520405e00,
                    3.62002815e00,
                    -9.93353240e00,
                    -5.95111730e00,
                    3.50146440e00,
                    -1.58161073e00,
                    1.32153944e00,
                    3.46545576e00,
                    -4.14140504e00,
                    1.80779810e00,
                    5.12518371e00,
                    5.06350579e-01,
                    -5.12143943e00,
                    3.05075730e00,
                    1.52664403e00,
                    1.17840650e00,
                    1.52245045e00,
                    -1.11987154e01,
                    3.52537880e00,
                    6.58677184e00,
                    1.04950075e00,
                    7.26431734e-01,
                    3.78884361e00,
                    -6.88274613e-01,
                    2.91277585e00,
                    -5.39988722e-01,
                    -4.86762086e00,
                    -5.85324299e00,
                    -4.79646945e00,
                    -5.12261654e00,
                    -3.76122380e00,
                    5.91361431e00,
                    3.95099716e00,
                    -1.00882397e00,
                    -1.12282264e00,
                    -1.53472669e-01,
                    -1.42612392e00,
                    1.01808498e00,
                    3.89284850e00,
                    -7.95528695e-01,
                    -1.52721085e00,
                    5.56588266e00,
                    -2.66966726e00,
                    1.07227282e00,
                    1.17704332e00,
                    2.19578871e-01,
                    -3.14188532e-01,
                    -3.56008185e00,
                    -1.10180252e00,
                    1.67156722e00,
                    1.65997958e00,
                    1.59415822e00,
                    -3.66572332e00,
                    -4.48543103e00,
                    2.70453532e00,
                    1.23141468e00,
                    -1.01656226e00,
                    4.45616246e00,
                    4.62624155e00,
                    1.06641760e01,
                    1.35086342e00,
                    -2.94979670e00,
                    -2.91476126e00,
                    -9.35116602e-01,
                    2.06360252e00,
                    -9.10136499e00,
                    5.81008956e00,
                    -1.62736303e00,
                    -1.25060209e00,
                    -2.87164090e00,
                    -5.45701288e-01,
                    -7.51629139e-01,
                    -9.38791436e-01,
                    2.34097570e00,
                    -2.84663470e00,
                    -3.87224043e00,
                    1.62309927e00,
                    5.67813073e-01,
                    3.81686799e-01,
                    2.51854400e00,
                    -4.86569414e00,
                    -4.26029143e00,
                    6.13481084e00,
                    -4.95681203e00,
                    -4.50729853e00,
                    2.67671425e00,
                    1.10979053e-01,
                    -9.80886696e-02,
                    -1.40850133e00,
                    2.61885371e00,
                    -2.60370423e00,
                    5.83765852e00,
                    -2.83363576e00,
                    -7.32202969e-01,
                    5.99369850e00,
                    -1.07059637e00,
                    7.54395772e00,
                    1.34653938e00,
                    5.18724237e00,
                    -7.20618474e00,
                    1.15357476e00,
                    -6.15439595e00,
                    4.00557024e00,
                    -6.54318747e00,
                    1.40767219e00,
                    -3.25250711e-01,
                    -6.16784426e00,
                    -5.85228332e00,
                    -2.92134516e-01,
                    6.75744660e00,
                    -3.20462659e-01,
                    4.23922397e00,
                    -9.29443606e-01,
                    3.45086639e00,
                    -8.67499798e00,
                    -2.01999643e00,
                    3.95956040e00,
                    8.79209638e-02,
                    -3.11761297e-01,
                    -9.54823660e-01,
                    3.36900880e00,
                    1.05584820e00,
                    1.90557798e-01,
                    4.35153735e00,
                    2.07445269e00,
                    3.28100342e-01,
                    6.04041984e00,
                    -1.15367544e00,
                    1.27468974e00,
                    -2.86660450e00,
                    -1.20727102e00,
                    6.11895125e00,
                    -2.82027924e00,
                    -6.04291722e00,
                    3.81097996e00,
                    9.10548304e-01,
                    8.94829367e-01,
                    4.36403895e-01,
                    -1.03365614e00,
                ]
            ]
        )
        np.testing.assert_array_almost_equal(self.fee.critical_points[15], critical_points_expected_15)

    def test_layer_0_biases(self):
        layer_0_biases_expected = np.array(
            [
                [3.52880724],
                [1.04879517],
                [1.50037751],
                [1.28102357],
                [-0.12998148],
                [1.31377369],
                [-0.37855184],
                [0.31751928],
                [-0.83950368],
                [1.00915159],
                [-0.22809063],
                [-0.09700302],
                [0.20176007],
                [-0.48283775],
                [0.15261177],
                [0.40842637],
            ]
        )
        np.testing.assert_array_almost_equal(self.fee.b_0, layer_0_biases_expected)

    def test_layer_1_biases(self):
        layer_1_biases_expected = np.array(
            [
                [0.3580238],
                [0.16528493],
                [-0.4548632],
                [-1.52886227],
                [0.23741153],
                [-1.2571574],
                [-0.75966823],
                [-1.02489274],
                [-0.48252173],
                [1.92286191],
            ]
        )
        np.testing.assert_array_almost_equal(self.fee.b_1, layer_1_biases_expected, decimal=4)

    def test_classifier_type_check_fail(self):
        backend_test_classifier_type_check_fail(
            FunctionallyEquivalentExtraction, [BaseEstimator, NeuralNetworkMixin, ClassifierMixin]
        )


if __name__ == "__main__":
    unittest.main()
