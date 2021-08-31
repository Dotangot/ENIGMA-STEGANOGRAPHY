'''
Ohad Mavdali & Dotan Gotshtein
DCT Image Steganography Project
'''

# External Libraries & Source Files
import cv2
import DCT_Embeding as embed
import DCT_Extract as extract
import Save_and_Show as ss

HIDDEN_IMAGE_FILEPATH = "images/hidden_img.jpg"


# Encrypt Stage
def Encrypt(text, filename):
    cover_image = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
    hidden_image = embed.Dct_embed(cover_image, text)
    # Save and Show Encrypted image
    ss.save_and_show(hidden_image, HIDDEN_IMAGE_FILEPATH)


# Decrypt Stage
def Extract(filename):
    stego_image = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
    secret = extract.Dct_extract(stego_image)
    # return secret message back to the user
    return secret
