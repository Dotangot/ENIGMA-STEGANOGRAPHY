import numpy as np

# Standard quantization table as defined by JPEG
quantmatrix = np.asarray([
                            [16, 11, 10, 16,  24, 40,   51,  61],
                            [12, 12, 14, 19,  26, 58,   60,  55],
                            [14, 13, 16, 24,  40, 57,   69,  56],
                            [14, 17, 22, 29,  51, 87,   80,  62],
                            [18, 22, 37, 56,  68, 109, 103,  77],
                            [24, 36, 55, 64,  81, 104, 113,  92],
                            [49, 64, 78, 87, 103, 121, 120, 101],
                            [72, 92, 95, 98, 112, 100, 103,  99]
                            ], dtype=np.float32)


# Image container class
class YCC_Image(object):
    def __init__(self, cover_image):
        self.height, self.width = cover_image.shape[:2]
        self.channels = [
                         split_8x8_blocks(cover_image[:, :, 0]),
                         split_8x8_blocks(cover_image[:, :, 1]),
                         split_8x8_blocks(cover_image[:, :, 2]),
                        ]


# Split image channel into 8x8 blocks
def split_8x8_blocks(image):
    blocks = []
    for vert_slice in np.vsplit(image, int(image.shape[0] / 8)):
        for horiz_slice in np.hsplit(vert_slice, int(image.shape[1] / 8)):
            blocks.append(horiz_slice)
    return blocks


# Combine 8x8 blocks into image channel
def combine_8x8_blocks(Nc, block_segments):
    image_rows = []
    temp = []
    for i in range(len(block_segments)):
        if i > 0 and not(i % int(Nc / 8)):
            image_rows.append(temp)
            temp = [block_segments[i]]
        else:
            temp.append(block_segments[i])
    image_rows.append(temp)
    return np.block(image_rows)


