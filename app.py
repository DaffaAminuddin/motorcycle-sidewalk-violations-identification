from flask import Flask
from flask import render_template
from flask import Response
import cv2
import numpy as np
import torch
import time
import pandas as pd
from tracker import *
from with_attachments import *
import os

app = Flask(__name__)
cap=cv2.VideoCapture("https://mam.jogjaprov.go.id:1937/atcs-kota/Simpang_Pingit1.stream/chunklist_w386863109.m3u8")
# cap=cv2.VideoCapture("trotoar.mp4")
path='custom70-30.tflite'
#path='/usr/local/lib/python3.9/dist-packages/yolov5/yolov5s.pt'

model = torch.hub.load('C:\\Users\\Daffa\\AppData\\Roaming\\Python\\Python310\\site-packages\\yolov5', 'custom', path,source='local')

b=model.names[2] = 'car'

size=416
tracker=Tracker()
timeframe = time.time()
#frame_id = 0
p=0
count=0
counter=0

area=[(531,196),(485,181),(390,548),(503,588)] #cctvdemangan
area1=[(531,196),(485,181),(461,281),(524,295)]
area2=[(521,352),(451,325),(434,399),(517,416)]
area3=[(557,233),(529,227),(527,304),(571,311)]
polygon = np.array(area)
polygon1= np.array(area1)
polygon2= np.array(area2)
polygon3= np.array(area3)
#area=[(330,356),(140,287),(6,329),(247,471)] #gerdep
tracker=Tracker()
area_c=set()

def fillPolyTrans(img, points, color, opacity):
    """
    @param img: (mat) input image, where shape is drawn.
    @param points: list [tuples(int, int) these are the points custom shape,FillPoly
    @param color: (tuples (int, int, int)
    @param opacity:  it is transparency of image.
    @return: img(mat) image with rectangle draw.

    """
    list_to_np_array = np.array(points, dtype=np.int32)
    overlay = img.copy()  # coping the image
    cv2.fillPoly(overlay,[list_to_np_array], color )
    new_img = cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0)
    # print(points_list)
    img = new_img

    return img

def cek_pelanggar_bertambah(area_c):
    if len(area_c) > cek_pelanggar_bertambah.sebelum:
        print(f"Mengambil gambar pelanggar ke-{z}.")              
        cv2.imwrite('Foto pelanggar\pelanggar.png',img) #save foto saat terjadi pelanggaran pada file foto pelanggar
        print("Total waktu adalah " + str(waktu))
        #send_emails(email_list)
#         exec(open('/home/pi/skripsi/yolov5vehiclecount/with_attachments.py').read())
    else:
        print("Belum ditemui pelanggar kembali")
    cek_pelanggar_bertambah.sebelum = len(area_c)
    return cek_pelanggar_bertambah.sebelum
cek_pelanggar_bertambah.sebelum = 0

def generate():
    while True:
        ret,img=cap.read()
        #count += 1
        #frame_id += 1
        
        #if count % 4 != 0:
        #    continue
        img=cv2.resize(img,(600,600))
        
        #cv2.line(img,(79,cy1),(599,cy1),(0,255,0),2)
        results=model(img,size)
        a=results.pandas().xyxy[0]
        #print(a)
        list=[]
        for index,row in results.pandas().xyxy[0].iterrows():
            x1=int(row[0])
            y1=int(row[1])
            x2=int(row[2])
            y2=int(row[3])
            d=(row['class']) 
    #         print(row)
    #         cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
    #         if 'car' in d:
    #         if d==0: #//3==motor
            list.append([x1,y1,x2,y2])
                
        bbox_id=tracker.update(list)
        for bbox in bbox_id:
            x3,y3,x4,y4,id=bbox
            cx=int(x3+x4)//2 #titik center
            cy=int(y3+y4)//2
            results=cv2.pointPolygonTest(np.array(area1,np.int32),((cx,cy)),False)
            if results >=0:
                area_c.add(id)
                waktu_1 = time.time()
                cv2.circle(img,(cx,cy),3,(0,255,255),-1)
                cv2.rectangle(img,(x3,y3),(x4,y4),(0,0,255),1)
                print(id)
                z=len(area_c)
                #(waktu_motor_1)
           
            results_2=cv2.pointPolygonTest(np.array(area2,np.int32),((cx,cy)),False)
            if results_2 >=0:
                cv2.circle(img,(cx,cy),3,(0,255,255),-1)
                cv2.rectangle(img,(x3,y3),(x4,y4),(0,0,255),1)
                waktu_2 = time.time()
                waktu = waktu_2 - waktu_1
                if waktu >= 1.2:
                    cek_pelanggar_bertambah(area_c)
                #print(len(area_c))
                #print(cek_pelanggar_bertambah.sebelum)
            results_3=cv2.pointPolygonTest(np.array(area3,np.int32),((cx,cy)),False)
            if results_3 >=0:
                cv2.circle(img,(cx,cy),3,(0,255,255),-1)
                cv2.rectangle(img,(x3,y3),(x4,y4),(0,0,255),1)
                waktu_3 = time.time()
                waktu = waktu_3 - waktu_1
                if waktu >= 0.6:
                    cek_pelanggar_bertambah(area_c)
        img = fillPolyTrans(img=img, points=polygon, color=(120,200,255), opacity=.5)
        img = fillPolyTrans(img=img, points=polygon1, color=(120,0,255), opacity=.7)
        img = fillPolyTrans(img=img, points=polygon2, color=(120,200,0), opacity=.7)
        img = fillPolyTrans(img=img, points=polygon3, color=(100,0,25), opacity=.7)
        cv2.polylines(img,[np.array(area,np.int32)],True,(255,255,0),1)
        
        #count=(len(area_c)) #menghitung setiap motor yang masuk ke area
        #cv2.putText(img,str(count),(60,145),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),2)
            
        #fps
#         elapsed_time = time.time() - timeframe #fps
#         fps = frame_id / elapsed_time
#         cv2.putText(img, str(round(fps,2)), (10, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2) #FPS Value
#         cv2.putText(img, "FPS", (105, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2) #FPS Label
        #transparent
        suc, encode = cv2.imencode(".jpeg",img)
        img = encode.tobytes()
        
        yield(b'--img\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype= "multipart/x-mixed-replace; boundary=img")


if __name__ == "__main__":
    app.run(debug=True)

cap.release()