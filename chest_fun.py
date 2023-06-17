from keras.models import load_model
import numpy as np
from PIL import Image
from keras import backend as K
import tensorflow as tf
from tensorflow import image

#path = '/home/lighthouse/resnet-OCT/resnet50-NIH/00000001_001.png'

def get_weighted_loss(pos_weights, neg_weights, epsilon=1e-7):
    """
    Return weighted loss function given negative weights and positive weights.

    Args:
      pos_weights (np.array): array of positive weights for each class, size (num_classes)
      neg_weights (np.array): array of negative weights for each class, size (num_classes)
    
    Returns:
      weighted_loss (function): weighted loss function
    """
    def weighted_loss(y_true, y_pred):
        """
        Return weighted loss value. 

        Args:
            y_true (Tensor): Tensor of true labels, size is (num_examples, num_classes)
            y_pred (Tensor): Tensor of predicted labels, size is (num_examples, num_classes)
        Returns:
            loss (Float): overall scalar loss summed across all classes
        """
        # initialize loss to zero
        loss = 0.0
        
        ### START CODE HERE (REPLACE INSTANCES OF 'None' with your code) ###

        for i in range(len(pos_weights)):
            # for each class, add average weighted loss for that class 
            loss += K.mean(-(pos_weights[i] *y_true[:,i] * K.log(y_pred[:,i] + epsilon) 
                             + neg_weights[i]* (1 - y_true[:,i]) * K.log( 1 - y_pred[:,i] + epsilon))) #complete this line
        return loss
    
        ### END CODE HERE ###
    return weighted_loss
    
def weighted_loss(y_true, y_pred):
        """
        Return weighted loss value. 

        Args:
            y_true (Tensor): Tensor of true labels, size is (num_examples, num_classes)
            y_pred (Tensor): Tensor of predicted labels, size is (num_examples, num_classes)
        Returns:
            loss (Float): overall scalar loss summed across all classes
        """
        # initialize loss to zero
        loss = 0.0
        
        ### START CODE HERE (REPLACE INSTANCES OF 'None' with your code) ###

        for i in range(len(pos_weights)):
            # for each class, add average weighted loss for that class 
            loss += K.mean(-(pos_weights[i] *y_true[:,i] * K.log(y_pred[:,i] + epsilon) 
                             + neg_weights[i]* (1 - y_true[:,i]) * K.log( 1 - y_pred[:,i] + epsilon))) #complete this line
        return loss


# img_path = 'resnet-OCT/resnet50-NIH/00000001_002.png'

def img_resize(img_path):
    print(img_path)
    img = Image.open(img_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = np.array(img)
    img = image.resize(img, [320,320])
    img = np.expand_dims(img, axis=0).astype('float32')
    return img/255

def chest_pre(path):
    module_path = 'resnet-OCT/resnet50-NIH/best_model_14.h5'
    label3 = ['Atelectasis', 'Effusion', 'Infiltration']
    label14 = ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion', 
                'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 
                'Mass', 'Nodule', 'Pleural_Thickening', 'Pneumothorax', 'Pneumonia']
    label14_cn =['肺不张','心脏扩大','肺实变','水肿','积液','肺气肿',
                '纤维化','疝气','浸润','肿块','结节','胸膜增厚','气胸','肺炎']
    i = img_resize(path)
    model = load_model(module_path, custom_objects={'weighted_loss': weighted_loss})
    m = model.predict(i, verbose=0)
    return  m[0]
