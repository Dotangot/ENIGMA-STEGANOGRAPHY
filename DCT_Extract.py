import cv2
import numpy as np
import ZigZag as zz
import Img_operation as img


# EXTRACT SECRET STRING OUT OF DCT COEFFICIENTS
def extract_encoded_data_from_DCT(dct_blocks):
    extracted_data = ""
    first_coeff = 0
    for current_dct_block in dct_blocks:
        for i in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[i])
            if curr_coeff > 1:
                curr_coeff = format(curr_coeff, '08b')
                extracted_data += curr_coeff[-1]
                first_coeff = 1
            # Enter $ to end of string, only after first char
            if len(extracted_data)%8==0 and first_coeff:
                if int(extracted_data[-8:], 2) == ord('$'):
                    return extracted_data[:-8]
    return extracted_data


def Dct_extract(stego_image):
    stego_image_f32 = np.float32(stego_image)
    stego_image_YCC = img.YCC_Image(cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb))

    # FORWARD DCT STAGE
    dct_blocks = [cv2.dct(block) for block in stego_image_YCC.channels[0]]  # Data encrypted in Luminance layer
    # QUANTIZATION STAGE
    dct_quants = [np.around(np.divide(item, img.quantmatrix)) for item in dct_blocks]
    # SORT DCT COEFFICIENTS BY FREQUENCY
    sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

    # DATA EXTRACTION STAGE
    recovered_data = extract_encoded_data_from_DCT(sorted_coefficients)

    secret = ""
    for i in range(0, len(recovered_data)-1, 8):
        # BINARY SEQUENCE TO CHAR + CONCAT TO STR
        secret += chr(int(recovered_data[i: i+8], 2))
    return secret
