import pymysql
import pandas as pd
from PIL import Image
import io
import os

# 寫入照片
def imageMysql(img_name):
    # 指定資料夾路徑
    folder_path = "images/"

    # 使用 listdir 函數列出資料夾中的檔案名稱,返回該目錄中所有文件和子目錄的名稱列表。
    file_names = os.listdir(folder_path)

    # 連接數據庫
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="userpass")

    # 創建游標
    cursor = conn.cursor()
    
    sql = "INSERT INTO userdata (images) VALUES (%s)"
    
    
    # 設置目標大小
    target_size = (400, 200)
    
    # 逐一讀取照片並處理
    if img_name in file_names:
        # 組合檔案的完整路徑
        file_path = os.path.join(folder_path,img_name)
        image = Image.open(file_path)
    
        resized_image = image.resize(target_size,Image.Resampling.LANCZOS)#ANTIALIAS 讓縮放的圖更平滑
    
        # 在這裡對照片進行相應的處理
        # 將照片轉換為字節流
        stream = io.BytesIO()
        resized_image.save(stream, format='JPEG')
        image_bytes = stream.getvalue()

        # 插入照片數據   
        cursor.execute(sql, (image_bytes))
        print("照片資料已成功插入數據庫")
    # 提交
    conn.commit()

    # 關閉游標和數據庫連接
    cursor.close()
    conn.close()
        