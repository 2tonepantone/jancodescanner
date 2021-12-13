import cv2
from pyzbar import pyzbar
import numpy as np
import base64


def extract_barcode(uri):
    """Returns an extracted barcode from a provided image"""
    image = data_uri_to_cv2_img(uri)
    barcodes = pyzbar.decode(image)
    barcodeData = ''

    # loop over the detected barcodes
    for barcode in barcodes:
        # the barcode data is a bytes object we convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # print the barcode type and data to the terminal
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    return barcodeData


def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image
