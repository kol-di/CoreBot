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

# STATE_DICT_PATH = os.path.join(os.getcwd(), 'model_state_dict')


async def create_core_model(state_dict_path, rebuild=False):
    model = CoreModel()
    await model.init_(state_dict_path, rebuild=rebuild)
    return model


class CoreModel:
    _class_options = None
    _data_transform = None
    _device = None

    _instance = None

    model = None

    def __new__(cls, *args, **kwargs):
        print('new')
        if cls._instance is None:
            print('long new')
            instance = super().__new__(cls)
            cls._instance = instance
            cls._class_options = CLASS_OPTIONS
            cls._data_transform = DATA_TRANSFORM
            cls._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return cls._instance

    # def __init__(self, state_dict_path, rebuild=False):
    #     print('init')
    #     if self.__class__.model is None or rebuild:
    #         print('long init')
    #         self.__class__.model = self.create_pretrained_model(state_dict_path)

    async def init_(self, state_dict_path, rebuild):
        if self.__class__.model is None or rebuild:
            print('long init')
            self.__class__.model = await self.create_pretrained_model(state_dict_path)

    def __call__(self, img_filename):
        self.model.eval()

        img_name = img_filename.split('/')[-1]
        img = Image.open(f'playground/{img_name}')
        img_tensor = self._data_transform(img).unsqueeze(dim=0).to(self._device)

        with torch.no_grad():
            result = self.model(img_tensor).cpu().data.numpy().argmax()
        return self.img_class_(result)

    async def create_pretrained_model(self, state_dict_path):
        # Load the pretrained model from pytorch
        vgg16 = models.vgg16_bn(weights=models.VGG16_BN_Weights.DEFAULT)

        # Change model architecture for my needs
        num_features = vgg16.classifier[6].in_features
        features = list(vgg16.classifier.children())[:-1]  # Remove last layer
        features.extend([nn.Linear(num_features, len(self._class_options))])  # Add layer with 4 outputs
        vgg16.classifier = nn.Sequential(*features)  # Replace the model classifier

        # Load new weights after additional training
        vgg16.load_state_dict(torch.load(state_dict_path, map_location=self._device))
        vgg16 = vgg16.to(self._device)

        return vgg16

    def img_class_(self, label_idx=None):
        if label_idx is not None:
            if torch.is_tensor(label_idx):
                label_idx = label_idx.item()
            try:
                return self._class_options[label_idx]
            except KeyError:
                pass


# model1 = CoreModel(STATE_DICT_PATH)
# model2 = CoreModel(STATE_DICT_PATH)
# print(model1 == model2)
# print(model2('7498c829aec8669c19702e255513ab82.png'))
