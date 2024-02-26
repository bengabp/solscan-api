import pytesseract
import cv2 as cv
from PIL import Image
import pandas as pd
from pytesseract import Output
import numpy as np
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# You can further process 'rows_data' to convert it into a list of dictionaries with structured information.


def extract_table(img: np.ndarray):


    # Preprocess the image (convert to grayscale, apply thresholding, etc.)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 220, 255, cv.THRESH_BINARY)

    canny = cv.Canny(binary, 0, 225)
    contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img, contours, -1, (255, 255, 0), 2)

    rows = []
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # for contour in contours:
    #     x_values = []
    #     y_values = []
    #
    #     for point in contour:
    #         x, y = point[0]
    #         x_values.append(x)
    #         y_values.append(y)
    #
    #     avg_x = int(sum(x_values) / len(x_values))
    #     avg_y = int(sum(y_values) / len(y_values))
    #
    #     line_height = 18
    #     h, w, _ = img.shape
    #
    #     x1, y1 = 0, (avg_y - line_height // 2) - 15
    #     x2, y2 = w, avg_y + line_height // 2
    #
    #     cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 200), 1)
    #     img_roi = img_rgb[y1:y2, x1:x2]
    #     result = pytesseract.image_to_string(img_roi)
    #
    #     word_list = []
    #     for chunk in result.strip().split(" "):
    #         word_list.append(chunk)
    #         if chunk.startswith("$"):
    #             break
    #
    #     _month, _day, _time, _time_of_day, _type, _usd, _pbp, _pyth, _price = word_list
    #     current_date = datetime.today()
    #     timestamp = datetime.strptime(f"{_month} {_day} {current_date.year}, {_time} {_time_of_day}",
    #                                   "%b %d %Y, %I:%M:%S %p").timestamp()
    #
    #     rows.append({
    #         "timestamp": timestamp,
    #         "transactionType": _type,
    #         "usd": _usd,
    #         "pbp": _pbp,
    #         "pyth": _pyth,
    #         "price": _price
    #     })

    cv.imshow("gray", gray)
    cv.imshow("binary", binary)
    cv.imshow("canny", canny)
    cv.imshow("img", img)

    cv.waitKey(0)
    cv.destroyAllWindows()

    return rows


if __name__ == "__main__":
    img = cv.imread(r"C:\Users\bengabp\Documents\IT\UKTeam\SolanaScan\datasets\data_page2.png")
    rows = extract_table(img)
    print(rows)
