import numpy as np


def zigzag(input):
    h = 0
    v = 0
    vmin = 0
    hmin = 0
    vmax = input.shape[0]
    hmax = input.shape[1]
    i = 0
    output = np.zeros(( vmax * hmax))

    while (v < vmax) and (h < hmax):
        if ((h + v) % 2) == 0:
            if v == vmin:
                output[i] = input[v, h]
                if h == hmax:
                    v = v + 1
                else:
                    h = h + 1
                    i = i + 1
            elif (h == hmax-1 and v< vmax):
                output[i] = input[v, h]
                v = v + 1
                i = i + 1

            elif ((v > vmin) and (h < hmax -1 )):    # all other cases
                output[i] = input[v, h]
                v = v - 1
                h = h + 1
                i = i + 1

        else:
            if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
                output[i] = input[v, h]
                h = h + 1
                i = i + 1

            elif h == hmin:                  # if we got to the first column
                output[i] = input[v, h]

                if (v == vmax -1):
                    h = h + 1
                else:
                    v = v + 1

                i = i + 1

            elif ((v < vmax -1) and (h > hmin)):     # all other cases
                output[i] = input[v, h]
                v = v + 1
                h = h - 1
                i = i + 1

        if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
            output[i] = input[v, h]
            break
    return output


def inverse_zigzag(input, vmax, hmax):
    h = 0
    v = 0
    vmin = 0
    hmin = 0

    output = np.zeros((vmax, hmax))
    i = 0

    while ((v < vmax) and (h < hmax)):
        if ((h + v) % 2) == 0:                 # going up
            if v == vmin:
                output[v, h] = input[i]        # if we got to the first line

                if h == hmax:
                    v = v + 1
                else:
                    h = h + 1

                i = i + 1

            elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
                output[v, h] = input[i]
                v = v + 1
                i = i + 1

            elif ((v > vmin) and (h < hmax -1 )):    # all other cases
                output[v, h] = input[i]
                v = v - 1
                h = h + 1
                i = i + 1

        else:                                    # going down
            if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
                output[v, h] = input[i]
                h = h + 1
                i = i + 1

            elif h == hmin:                  # if we got to the first column
                output[v, h] = input[i]
                if (v == vmax -1):
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1

            elif((v < vmax -1) and (h > hmin)):     # all other cases
                output[v, h] = input[i]
                v = v + 1
                h = h - 1
                i = i + 1

        if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
            output[v, h] = input[i]
            break

    return output
# "ZigZag.py" location source: https://github.com/amzhang1/simple-JPEG-compression/blob/master/zigzag.py
