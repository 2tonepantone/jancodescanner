import cv2
from pyzbar import pyzbar
import numpy as np
import base64


def extract_barcode(uri):
    """Returns an extracted barcode from a provided image"""
    image = data_uri_to_cv2_img(uri)
    barcodes = pyzbar.decode(image)
    decoded = barcodes[0]
    rect = decoded.rect
    # print(rect)  # Rect(left=19, top=19, width=292, height=292)

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    3, (0, 0, 255), 10)

        # print the barcode type and data to the terminal
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    # show the output image
    # cv2.imshow("Image", image)
    # cv2.imwrite('macbook_qr_rect.jpg', image)
    cv2.waitKey(1)
    return barcodeData


def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image
