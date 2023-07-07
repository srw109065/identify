# detect03.py
import torch
import numpy as np
import cv2
from time import strftime
import os
import dataPymysql
import time
import LINE
#LINE推播 KEY與 MSG
token = 'OLqCvEIQWMpN71IbNZndYaXzGFSZCGvrlCXUpyqCxkS'
#OLqCvEIQWMpN71IbNZndYaXzGFSZCGvrlCXUpyqCxkS 各人的key
#HiGPPsohxpsvDaGlbUyUEraTF9skJoqRnhWDSY6x9qY 專題群組的Key
message = ''


def det():
  model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt',force_reload=True)#custom 自己訓練
  # 設定信心門檻值
  model.conf = 0.7
  
  # 設定 IoU 門檻值
  model.iou = 0.3

  cap = cv2.VideoCapture(0)
  textgather = {"knife":"刀","fire":"火災"}
  start_time  = time.time()
  while cap.isOpened():
      current_time = time.time()
      elapsed_time = current_time - start_time
      success, frame = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        continue
      frame = cv2.resize(frame,(800,480))
      results = model(frame)
      print(elapsed_time)
      if len(results.pandas().xyxy[0]) > 0:#pandas 方法獲得的一個Pandas DataFrame 對象。
        #返回一個包含檢測結果的Pandas DataFrame 對象。通過 .xyxy 屬性，可以訪問檢測到的物體的信息，例如坐標、置信度和類別等。
          object_name = results.pandas().xyxy[0]['name'].tolist()[0]
          #results.pandas().xyxy[0]['name']返回的是一個包含物體名稱的Pandas Series 對象，而不是單個字符串。因此，如果要比較物體名稱
          #您需要使用 .item() 方法將其轉換為字符串
          #返回的Series對像不僅僅是一個元素，而是一個包含多個元素的倉庫。
          #您可以嘗試使用tolist()方法將Series對象轉換為Python列表，然後獲取列表中的第一個元素作為物體名稱。     

          if object_name in textgather:
            text = "危險, 危險，檢測到" + textgather.get(object_name)             

          
          if elapsed_time >= 10:    
            with open("output.txt", "w",newline='', encoding='utf-8') as file:
              file.write(text)       

            systime = strftime("%Y%m%d%H%M")#年月日時間
            imgname = os.path.join('images/',  object_name + '.' + systime + '.jpg')#拍照儲存
            filename = os.path.basename(imgname)
            cv2.imwrite(imgname, frame)
            dataPymysql.imageMysql(filename)
            LINE.lineNotifyMessage(token, imgname)
              
            start_time = current_time  

      cv2.imshow('YOLO COCO 03 mask detection', np.squeeze(results.render()))

      keyb = cv2.waitKey(1) & 0xFF
      #ESC結束
      if keyb == 27:  # 按下ESC键
          break
  cap.release()
  cv2.destroyAllWindows()
  
def main():
    det()
    
    
if __name__ == "__main__":
    main()

    
    
    