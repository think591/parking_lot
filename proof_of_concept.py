
##### 概念驗證 #####

# 使用 easyocr 模組的 Reader 類別
#* (parking_lot) pip install easyocr

import easyocr

reader = easyocr.Reader(["en"], gpu=False)   # 以 英文"en" 辨識

# 將 numpy 版本號調降的指令 ()
#* (parking_lot) pip install "numpy<2.0"

# 以 Reader 類別的 readtext() 方法辨識圖片中的文字
#* 預設參數下會回傳三組輸出：文字位置的四個 (x, y) 座標、文字、信心分數。
#* detail=0 參數僅回傳文字。不會回傳圖片座標和信心分數

img_path = "data/car_plate_1.jpg"
results = reader.readtext(img_path)
# results = reader.readtext("data/car_plate_1.jpg", detail=0)
print(results)


######################################################################################


# 可以利用文字位置的左上、右下這兩個座標點畫出方框
#* (parking_lot) pip install opencv-python
#* (parking_lot) conda install matplotlib
#* import cv2
#* cv2.rectangle(img, pt1, pt2, color, thickness) 取出 左上 和 右下 的座標點

import easyocr
import cv2
import matplotlib.pyplot as plt

reader = easyocr.Reader(["en"], gpu=False)
img_path = "data/car_plate_1.jpg"
results = reader.readtext(img_path)
print(results)
results[0][0]   # 取出座標點：先移除list[] 再移除tuple()
print(results[0][0])


x_points = []
y_points = []
for xi, yi in results[0][0]:
    x_points.append(int(xi))  #取整數，因為 cv2.rectangle 只接受整數
    y_points.append(int(yi))  #取整數，因為 cv2.rectangle 只接受整數
left_top = (min(x_points), min(y_points))
right_bottom = (max(x_points), max(y_points))
print(left_top)
print(right_bottom)

img = cv2.imread(img_path)
#* cv2.rectangle(img, pt1, pt2, color, thickness)
cv2.rectangle(img, left_top, right_bottom, (0, 255, 0), 5)  # RGB 紅綠藍 (0, 255, 0)
plt.imshow(img)
plt.show()


################################################################################################


# 紀錄進場時間

from datetime import datetime
from datetime import timezone
from datetime import timedelta

# results = reader.readtext("data/car_plate_1.jpg", detail=0)      # 車牌辨識後，紀錄進場時間
entry_time = datetime.now(timezone.utc) + timedelta(hours=8)       # 取得現在的時間。timezone.utc 格林威治時間


# 紀錄出場時間與計算停留時間

# results = reader.readtext("data/car_plate_1.jpg", detail=0)      # 車牌辨識後，紀錄出場時間
leaving_time = datetime.now(timezone.utc) + timedelta(hours=8)

time_elapsed = leaving_time - entry_time

print(entry_time)
print(leaving_time)
print(time_elapsed)
print(int(time_elapsed.total_seconds()))                          # 換算成秒數


################################################################################################


# 定義 parking_lot_ocr() 函數，設定圖片路徑和費率 

import easyocr
from datetime import datetime
from datetime import timezone
from datetime import timedelta

reader = easyocr.Reader(["en"], gpu=False)                              # 以 英文"en" 辨識

parked_vehicles = dict()                                                # 記錄停進來的 車和進場時間

def parking_lot_ocr(img_path: str, ntd_per_sec: int=1):                 # ntd_per_sec 費率
    results = reader.readtext(img_path, detail=0)
    entry_time = datetime.now(timezone.utc) + timedelta(hours=8)
    entry_time_str = entry_time.strftime("%Y-%m-%d %H:%M:%S")           # 轉換為文字格式，ISO 8601格式
    car_plate = results[0]
    if car_plate not in parked_vehicles.keys():                         # 辨識後，不在 parked_vehicles 中記錄為 “進場”
        parked_vehicles[car_plate] = entry_time
        print(f"Welcome to the parking lot {car_plate}!")               # x string 將車牌號碼寫入
        print(f"Your entry time is: {entry_time_str}.")
        print(f"Parking fee is NT${ntd_per_sec} per second.")
    else:                                                               # 辨識後，在 parked_vehicles 中記錄為 “出場”
        leaving_time = datetime.now(timezone.utc) + timedelta(hours=8)
        time_elapsed = leaving_time - parked_vehicles[car_plate]
        seconds_elapsed = int(time_elapsed.total_seconds())
        charge_amount = seconds_elapsed * ntd_per_sec
        print(f"Bye bye bye {car_plate}!")
        print(f"Your vehicle stayed {seconds_elapsed} seconds.")
        print(f"You will be charged NT${charge_amount:,}.")             # 千分位 逗號格式
        parked_vehicles.pop(car_plate, None)                            # 完成後，使用 pop 移除車牌圖片
        

parking_lot_ocr("data/car_plate_1.jpg")

print(parked_vehicles)

parking_lot_ocr("data/car_plate_1.jpg")

print(parked_vehicles)


################################################################################################

##### 成品 #####

# 建立一個上傳圖片與文字輸出的 gradio 介面

import gradio as gr

parked_vehicles = dict()

def parking_lot_ocr():
    pass

demo = gr.Interface(fn=parking_lot_ocr,
                    inputs=gr.Image(),
                    outputs="text",
                    title="小小停車場")
demo.launch()

################################################################################################

# 將 parking_lot_ocr() 函數完成

import gradio as gr
import easyocr
from datetime import datetime
from datetime import timezone
from datetime import timedelta

reader = easyocr.Reader(["en"], gpu=False)
parked_vehicles = dict()

def parking_lot_ocr(uploaded_img, ntd_per_sec: int=1):
    result = reader.readtext(uploaded_img, detail=0)
    entry_time = datetime.now(timezone.utc) + timedelta(hours=8)
    entry_time_str = entry_time.strftime("%Y-%m-%d %H:%M:%S")
    car_plate = result[0]
    if car_plate not in parked_vehicles.keys():
        parked_vehicles[car_plate] = entry_time
        return f"""Welcome to the parking lot {car_plate}!\n
                   Your entry time is: {entry_time_str}.\n
                   Parking fee is NT${ntd_per_sec} per second."""
    else:
        leaving_time = datetime.now(timezone.utc) + timedelta(hours=8)
        time_elapsed = leaving_time - parked_vehicles[car_plate]
        seconds_elapsed = int(time_elapsed.total_seconds())
        charge_amount = seconds_elapsed * ntd_per_sec
        parked_vehicles.pop(car_plate, None)
        return f"""Bye bye bye {car_plate}!\n
                   Your vehicle stayed {seconds_elapsed} seconds.\n
                   You will be charged NT${charge_amount:,}."""

demo = gr.Interface(fn=parking_lot_ocr,
                    inputs=gr.Image(),
                    outputs="text",
                    title="小小停車場")

demo.launch()


# 將 mkl toolkit 移除的指令
#* (parking_lot) conda install nomkl
