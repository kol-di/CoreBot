from PIL import Image
import os

import torch
from torch import nn
from torchvision import models, transforms


CLASS_OPTIONS = {
    0: 'breakcore',
    1: 'draincore',
    2: 'glitchcore',
    3: 'weirdcore',
}

DATA_TRANSFORM = transforms.Compose([
    transforms.RandomResizedCrop(234),
    transforms.ToTensor(),
])

# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

STATE_DICT_PATH = os.path.join(os.getcwd(), 'model_state_dict')


# def create_pretrained_model(state_dict_path):
#     # Load the pretrained model from pytorch
#     vgg16 = models.vgg16_bn(weights=models.VGG16_BN_Weights.DEFAULT)
#
#     # Change model architecture for my needs
#     num_features = vgg16.classifier[6].in_features
#     features = list(vgg16.classifier.children())[:-1]  # Remove last layer
#     features.extend([nn.Linear(num_features, len(CLASS_OPTIONS))])  # Add layer with 4 outputs
#     vgg16.classifier = nn.Sequential(*features)  # Replace the model classifier
#
#     # Load new weights after additional training
#     vgg16.load_state_dict(torch.load(state_dict_path, map_location=DEVICE))
#     vgg16 = vgg16.to(DEVICE)
#
#     return vgg16


# def img_class(label_idx=None):
#     if label_idx is not None:
#         if torch.is_tensor(label_idx):
#             label_idx = label_idx.item()
#         try:
#             print(CLASS_OPTIONS[label_idx])
#         except KeyError:
#             pass
#
#
# def which_core_are_you(model, img_filename):
#     model.eval()
#
#     img_name = img_filename.split('/')[-1]
#     img = Image.open(f'playground/{img_name}')
#     img_tensor = DATA_TRANSFORM(img).unsqueeze(dim=0).to(DEVICE)
#
#     with torch.no_grad():
#         result = model(img_tensor).cpu().data.numpy().argmax()
#     return img_class(result)


# model = create_pretrained_model(STATE_DICT_PATH)
# which_core_are_you(model, '7498c829aec8669c19702e255513ab82.png')


class Model:
    _class_options = None
    _data_transforms = None
    _device = None
    _state_dict_path = None

    _instance = None

    model = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(instance, *args, **kwargs)
            cls._instance = instance
        return cls._instance

    def __init__(self, *args, **kwargs):
        self._class_options = CLASS_OPTIONS
        self._data_transforms = DATA_TRANSFORM
        self._state_dict_path = STATE_DICT_PATH
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.create_pretrained_model()

    def create_pretrained_model(self):
        # Load the pretrained model from pytorch
        vgg16 = models.vgg16_bn(weights=models.VGG16_BN_Weights.DEFAULT)

        # Change model architecture for my needs
        num_features = vgg16.classifier[6].in_features
        features = list(vgg16.classifier.children())[:-1]  # Remove last layer
        features.extend([nn.Linear(num_features, len(self._class_options))])  # Add layer with 4 outputs
        vgg16.classifier = nn.Sequential(*features)  # Replace the model classifier

        # Load new weights after additional training
        vgg16.load_state_dict(torch.load(self._state_dict_path, map_location=self._device))
        vgg16 = vgg16.to(self._device)

        return vgg16

    def img_class_(self, label_idx=None):
        if label_idx is not None:
            if torch.is_tensor(label_idx):
                label_idx = label_idx.item()
            try:
                print(self._class_options[label_idx])
            except KeyError:
                pass

    def which_core_are_you(self, img_filename):
        self.model.eval()

        img_name = img_filename.split('/')[-1]
        img = Image.open(f'playground/{img_name}')
        img_tensor = DATA_TRANSFORM(img).unsqueeze(dim=0).to(self._device)

        with torch.no_grad():
            result = self.model(img_tensor).cpu().data.numpy().argmax()
        return self.img_class_(result)

