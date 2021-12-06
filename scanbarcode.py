import cv2
from pyzbar import pyzbar
from productscraper.management.commands.crawl import handle_scrape

def read_barcodes(frame):
    global barcode_processed
    barcode_processed = False
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect

        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6),
                    font, 2.0, (255, 255, 255), 1)

        if (bool(barcode_info)):
            handle_scrape(barcode_info)
            barcode_processed = True
    return frame


def main():
    camera = cv2.VideoCapture(0)
    try:
        while True:
            scanning, frame = camera.read()
            frame = read_barcodes(frame)
            # cv2.imshow('Barcode reader', read_barcodes(frame))
            if cv2.waitKey(1) & barcode_processed:
                break
    except cv2.error as e:
        print(e)

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
