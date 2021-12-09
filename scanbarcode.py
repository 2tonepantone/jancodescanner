import cv2
from pyzbar import pyzbar


def extract_barcode():
    """Returns an extracted barcode from a provided image"""
    fp = 'static/barcodeimages/product1.jpeg'
    image = cv2.imread(fp)
    barcodes = pyzbar.decode(image)
    decoded = barcodes[0]
    print(decoded)
    rect = decoded.rect
    print(rect)  # Rect(left=19, top=19, width=292, height=292)

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


if __name__ == '__main__':
    extract_barcode()



# def read_barcodes(frame):
#     global barcode_processed
#     barcode_processed = False
#     global barcode_info
#     barcode_info = ''
#     barcodes = pyzbar.decode(frame)
#     for barcode in barcodes:
#         x, y, w, h = barcode.rect

#         barcode_info = barcode.data.decode('utf-8')
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, barcode_info, (x + 6, y - 6),
#                     font, 2.0, (255, 255, 255), 1)

#         if (len(barcode_info) == 13):
#             barcode_processed = True
#     return frame


# def start_scan():
#     camera = cv2.VideoCapture(0)
#     try:
#         while True:
#             scanning, frame = camera.read()
#             frame = read_barcodes(frame)
#             # cv2.imshow('Barcode reader', read_barcodes(frame))
#             if cv2.waitKey(1) & barcode_processed:
#                 break
#     except cv2.error as e:
#         print(e)

#     camera.release()
#     cv2.destroyAllWindows()
#     return barcode_info
