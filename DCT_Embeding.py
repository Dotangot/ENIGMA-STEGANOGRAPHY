import cv2
import numpy as np
import ZigZag as zz
import Img_operation as img

NUM_LAYERS = 3  # IMAGE HAS 3 LAYERS: RGB


# EMBED SECRET STRING IN DCT COEFFICIENTS
def embed_encoded_data_into_DCT(secret_bin_data, sorted_coeffs):
    data_complete = False
    index = 0
    # FLAG THE END OF SECRET WITH '$'
    secret_bin_data += format(ord('$'), '08b')
    encoded_data_len = len(secret_bin_data)+8
    converted_blocks = []
    # ITERATE COEFF BLOCKS
    for current_dct_block in sorted_coeffs:
        for i in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[i])
            # CHANGE ONLY COEFFs GREATER THAN 1
            if (curr_coeff > 1):
                # SET NUM IN RANGE 255 AND TURN TO BIN
                curr_coeff = format(np.uint8(current_dct_block[i]), '08b')
                # REPLACE 1LSB OF COEFF WITH 1MSB OF SECRET
                if index+1 <= encoded_data_len:
                    curr_coeff = curr_coeff[:-1]
                    curr_coeff += secret_bin_data[index: index+1]
                    index += 1
                else:
                    data_complete = True; break
                # REPLACE CONVERTED COEFFICIENTS
                current_dct_block[i] = np.float32(int(curr_coeff, 2))
        converted_blocks.append(current_dct_block)

    if not(data_complete):
        raise ValueError("Data didn't fully embed into cover image!")
    return converted_blocks

def Dct_embed(image, text_to_hide):
    height, width = image.shape[:2]
    # FORCE IMAGE DIMENSIONS TO BE 8x8 COMPLIANT
    while height % 8: height += 1  # Rows
    while width % 8: width += 1  # Cols
    valid_dim = (width, height)
    padded_image = cv2.resize(image, valid_dim)
    cover_image_f32 = np.float32(padded_image)
    # SPLIT TO 8X8 BLOCKS AND TURN TO YCrCb
    cover_image_YCC = img.YCC_Image(cv2.cvtColor(cover_image_f32, cv2.COLOR_BGR2YCrCb))
    # PLACEHOLDER FOR HOLDING STEGO IMAGE DATA
    stego_image = np.empty_like(cover_image_f32)

    for chan_index in range(NUM_LAYERS):
        # FORWARD DCT STAGE
        dct_blocks = [cv2.dct(block) for block in cover_image_YCC.channels[chan_index]]
        # QUANTIZATION STAGE
        dct_quants = [np.around(np.divide(item, img.quantmatrix)) for item in dct_blocks]
        # SORT DCT COEFFICIENTS BY FREQUENCY
        sorted_coeffs = [zz.zigzag(block) for block in dct_quants]

        # EMBED DATA IN LUMINANCE LAYER
        if chan_index == 0:
            # DATA INSERTION STAGE
            secret_bin_data = ""
            for char in text_to_hide.encode('ascii'):
                secret_bin_data += format(char, '08b')
            # DATA ENCRYPTION STAGE
            embedded_dct_blocks = embed_encoded_data_into_DCT(secret_bin_data, sorted_coeffs)
            # REVERSE ZIGZAG
            desorted_coefficients = [zz.inverse_zigzag(block, vmax=8, hmax=8) for block in embedded_dct_blocks]
        else:
            # REVERSE ZIGZAG TO CHROMA CHANNELS
            desorted_coefficients = [zz.inverse_zigzag(block, vmax=8, hmax=8) for block in sorted_coeffs]

        # DEQUANTIZATION STAGE
        dct_dequants = [np.multiply(data, img.quantmatrix) for data in desorted_coefficients]
        # Inverse DCT Stage
        idct_blocks = [cv2.idct(block) for block in dct_dequants]

        # REBUILD FULL IMAGE CHANNEL
        stego_image[:, :, chan_index] = np.asarray(img.combine_8x8_blocks(cover_image_YCC.width, idct_blocks))

    # YCrCb TO BGR
    stego_image_BGR = cv2.cvtColor(stego_image, cv2.COLOR_YCR_CB2BGR)
    # Clamp Pixel Values to [0 - 255]
    final_stego_image = np.uint8(np.clip(stego_image_BGR, 0, 255))
    return final_stego_image


