import cv2
import matplotlib.pyplot as plt


def save_and_show(image, path):
    # Save image to path
    cv2.imwrite(path, image)
    # Show Encrypted image
    plt.figure()
    plt.imshow(image[:, :, ::-1])
    plt.title("Image Encrypted with your data")
    plt.axis("off")
    plt.show()
    return
