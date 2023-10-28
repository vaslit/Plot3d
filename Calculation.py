import numpy as np
import cv2 as cv2
import matplotlib.pyplot as plt

def depthTest(imgL, imgR,numDisparities=16, blockSize=15):
    stereo = cv2.StereoSGBM_create(numDisparities=32, blockSize=15)
    disparity = stereo.compute(imgL, imgR)
    np.max
    imgs = [imgL, imgR, disparity]
    d_min = np.min(disparity)
    d_max = np.max(disparity)
    delta = d_max-d_min
    k = delta / 256
    return np.clip((disparity + d_min)/k,0,255).astype(np.uint8)
    titles = ['Левая перспектива', 'Правильная перспектива', 'Карта несоответствия']
    for i in range(3):
        plt.subplot(2, 2, i+1)
        plt.imshow(imgs[i], cmap='gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()
    