from keras.models import load_model

# Метрики для модели
def dice_coef(y_true, y_pred):
    smooth = 1e-20
    y_true_f = y_true.flatten()
    intersection = (y_true_f * y_pred.flatten()).sum()
    return (2. * intersection + smooth) / (y_true_f.sum() + y_pred.flatten().sum() + smooth)

def dice_coef_loss(y_true, y_pred):
    return 1 - dice_coef(y_true, y_pred)

# Функция для загрузки модели
def load_model_unet():
    model = load_model(r'D:\projects\liver-segmentation-web-service\liver-segmentation-model\model\best_model.keras', 
                    custom_objects={'dice_coef': dice_coef, 'dice_coef_loss': dice_coef_loss})
    return model

