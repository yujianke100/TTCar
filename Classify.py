from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2 
import threading
import time
import os
import RPi.GPIO as GPIO


class Classify:
    cap_flag = 1
    cam_flag = 0
    num_index = 1
    i = 0

    cutTime = 0
    # outpinUp = 35
    # inpinUp = 37
    # outpinDown = 11
    # inpinDown = 13

    GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(outpinUp,GPIO.OUT,initial=GPIO.LOW)
    # GPIO.setup(inpinUp,GPIO.IN)
    # GPIO.setup(outpinDown,GPIO.OUT,initial=GPIO.LOW)
    # GPIO.setup(inpinDown,GPIO.IN)

    GPIO.setup(19, GPIO.IN)

    def get_trapezoid(self,X,Y):
        a1,a2 = 0.9,0.9
        trapezoid = np.ones((X,Y))
    
        for x in range(int(a1*X),X):
            for y in range (0,int(Y/2.0)):
                if (2.0/Y*y - (x-a1*X)/(X-a1*X)) < 0:
                    trapezoid[x][y] = 0


        for x in range(int(a2*X),X):
            for y in range (int(Y/2),Y):
                if (2.0/Y*(y-Y) + (x-a2*X)/(X-a2*X)) < 0:
                    trapezoid[x][y] = 0
        return trapezoid
        
    def obt(self):
        i = GPIO.input(19)
        if(i == 0):
            print("\nhave obt\n")
        return i

    def camera(self,id):
        try:
            self.cap = cv2.VideoCapture(id)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

            print("camera start!")
            while(self.cap.isOpened() and self.cap_flag == 1):
                ret ,frame = self.cap.read()
                if(self.cam_flag != 0):
                    print(self.cam_flag)
                if(self.cam_flag == 1):
                    if(self.cutTime < 6):
                        sName = 'D'
                    elif(self.cutTime < 12):
                        sName = 'C'
                    elif(self.cutTime < 18):
                        sName = 'B'
                    elif(self.cutTime < 24):
                        sName = 'A'
                    # cropImgup = frame[20:200,50:450]
                    # cropImgdown = frame[240:400,50:450]
                    # cv2.imwrite('./0.jpg',frame)
                    # cv2.imwrite('./1.jpg',frame[80:275,60:450])
                    # cv2.imwrite('./2.jpg',frame[310:420,108:450])
                    # cv2.imwrite('./1.jpg',frame[100:250,250:850])
                    # cv2.imwrite('./2.jpg',frame[350:550,350:800])
                    # cv2.imwrite('./all_' + str(self.i) +'.jpg',frame)
                    # cv2.imwrite('./up_' + str(self.i) +'.jpg',frame[80:275,60:450])
                    # cv2.imwrite('./down_' + str(self.i) +'.jpg',frame[310:420,108:450])
                    cv2.imwrite(sName + str(self.cutTime % 6) + str(2) +'.jpg',frame)
                    cv2.imwrite(sName + str(self.cutTime % 6) + str(0) +'.jpg',frame[230:310,500:800])
                    cv2.imwrite(sName + str(self.cutTime % 6) + str(1) +'.jpg',frame[380:490,550:750])
                    self.cutTime += 1
                    print("flag1 was clear")
                elif(self.cam_flag == 2):
                    print("cameraGet index:" + str(self.num_index))
                    # cv2.imwrite('./L'+str(self.num_index)+'.jpg',frame[0:300,0:210])
                    # cv2.imwrite('./M'+str(self.num_index)+'.jpg',frame[0:300,210:420])
                    # cv2.imwrite('./R'+str(self.num_index)+'.jpg',frame[0:300,420:630])
                    frame=np.rot90(frame)
                    frame=np.rot90(frame)
                    cv2.imwrite('./L'+str(self.num_index)+'.jpg',frame[250:400,450:600])
                    cv2.imwrite('./M'+str(self.num_index)+'.jpg',frame[250:400,600:750])
                    cv2.imwrite('./R'+str(self.num_index)+'.jpg',frame[250:400,750:900])
                    print("flag2 was clear")
                elif(self.cam_flag == 3):
                    # print("cameraGet index:" + str(self.num_index))
                    # cv2.imwrite('./L.jpg',frame[0:300,0:210])
                    # cv2.imwrite('./M.jpg',frame[0:300,210:420])
                    # cv2.imwrite('./R.jpg',frame[0:300,420:630])
                    # cv2.imwrite('./L.jpg',frame[150:400,0:210])
                    # cv2.imwrite('./M.jpg',frame[150:400,210:420])
                    # cv2.imwrite('./R.jpg',frame[150:400,420:630])
                    cv2.imwrite('./L'+str(self.num_index)+'.jpg',frame[250:400,450:600])
                    cv2.imwrite('./M'+str(self.num_index)+'.jpg',frame[250:400,600:750])
                    cv2.imwrite('./R'+str(self.num_index)+'.jpg',frame[250:400,750:900])
                    print("flag3 was clear")
                elif(self.cam_flag == 4):
                    if(self.cutTime < 6):
                        sName = 'D'
                    elif(self.cutTime < 12):
                        sName = 'C'
                    elif(self.cutTime < 18):
                        sName = 'B'
                    elif(self.cutTime < 24):
                        sName = 'A'
                    # cropImgup = frame[20:200,50:450]
                    # cropImgdown = frame[240:400,50:450]
                    # cv2.imwrite('./0.jpg',frame)
                    # cv2.imwrite('./1.jpg',frame[80:275,60:450])
                    # cv2.imwrite('./2.jpg',frame[310:420,108:450])
                    # cv2.imwrite('./1.jpg',frame[100:250,250:850])
                    # cv2.imwrite('./2.jpg',frame[350:550,350:800])
                    # cv2.imwrite('./all_' + str(self.i) +'.jpg',frame)
                    # cv2.imwrite('./up_' + str(self.i) +'.jpg',frame[80:275,60:450])
                    # cv2.imwrite('./down_' + str(self.i) +'.jpg',frame[310:420,108:450])
                    cv2.imwrite(sName + str(self.cutTime % 6) + str(2) +'.jpg',frame)
                    cv2.imwrite(sName + str(self.cutTime % 6) + str(0) +'.jpg',frame[230:290,700:850])
                    cv2.imwrite(sName + str(self.cutTime % 6) + str(1) +'.jpg',frame[380:420,700:800])
                    self.cutTime += 1
                    print("flag1 was clear")
                self.cam_flag = 0
            self.cap.release()
            print("camera was released")

        except Exception as e:
            self.cap.release()
            print("camera was released")
            GPIO.cleanup()
            print("GPIO was released")
            print(e)

    def threadcam(self,ip):
        self.cap_flag = 1
        self.cam_flag = 0
        self.num_index = 1
        self.i = 0
        try:
            camThread = threading.Thread(target=self.camera, args=(ip,))
            camThread.start()
        except:
            print ("camera threading start falsed!")

    def cut(self,mode):
        time.sleep(0.3)
        self.cam_flag = mode
        print("cam" + str(mode) + " start!")
        while(self.cam_flag != 0):
            pass
    def super_cut(self,mode):
        # time.sleep(0.5)
        self.cam_flag = mode
        print("cam" + str(mode) + " start!")
        # while(self.cam_flag != 0):
        #     pass
    def stop(self):
        self.cap_flag = 0

    def numUpdate(self,num_index):
        self.num_index = num_index

    def gpio_close(self):
        GPIO.cleanup()

    # def rec_yes_or_no_up(self):
    #     num = 0
    #     img = cv2.imread("./1.jpg")
    #     x, y = img.shape[0:2]
    #     img = cv2.resize(img, (int(y / 3), int(x / 3)))
    #     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    # #    cv2.namedWindow('canny demo')
    #     canny = cv2.Canny(gray, 35, 50)
    #     #cv2.imshow('Canny', canny)
    #     #cv2.createTrackbar('Min threshold','canny demo',lowThreshold, max_lowThreshold, CannyThreshold)
    #     I_array = np.array(canny)
    #     for i in range(I_array.shape[0]):
    #         for j in range(I_array.shape[1]):
    #             if I_array[i][j] > 0:
    #                 num = num + 1
    #     if num > 1000:
    #         return 1
    #     else:
    #         return 0

    # def rec_yes_or_no_down(self):
    #     num = 0
    #     img = cv2.imread("2.jpg")
    #     x, y = img.shape[0:2]
    #     img = cv2.resize(img, (int(y / 3), int(x / 3)))
    #     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #     #    cv2.namedWindow('canny demo')
    #     canny = cv2.Canny(gray, 35, 50)
    #     #cv2.imshow('Canny', canny)
    #     #cv2.createTrackbar('Min threshold','canny demo',lowThreshold, max_lowThreshold, CannyThreshold)
    #     I_array = np.array(canny)
    #     for i in range(I_array.shape[0]):
    #         for j in range(I_array.shape[1]):
    #             if I_array[i][j] > 0:
    #                 num = num + 1
    #     if num > 2000:
    #         return 1
    #     else:
    #         return 0

    # def rec_yes_or_no_up(self):
    #     img = cv2.imread("1.jpg")
    #     #img = cv2.blur(img,(img.shape[0],img.shape[1]))
    #     imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #     thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,17,2)
    #     thresh = np.multiply(thresh,self.get_trapezoid(img.shape[0],img.shape[1]))
    #     thresh = thresh.astype('uint8')
    #     binary, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    #     area = 0
    #     for i in range(0,len(contours),2):
    #         area += cv2.contourArea(contours[i])
    #     print("up" + str(area))
    #     if area > 1200:
    #         return 1
    #     else:
    #         return 0

    # def rec_yes_or_no_down(self):
    #     img = cv2.imread("2.jpg")
    #     #img = cv2.blur(img,(img.shape[0],img.shape[1]))
    #     imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #     thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,17,2)
    #     thresh = np.multiply(thresh,self.get_trapezoid(img.shape[0],img.shape[1]))
    #     thresh = thresh.astype('uint8')
    #     binary, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    #     area = 0
    #     for i in range(0,len(contours),2):
    #         area += cv2.contourArea(contours[i])
    #     print("down" + str(area))
    #     if area > 3000:
    #         return 1
    #     else:
    #         return 0

    # def rec_yes_or_no(self):
    #     upflag = 0
    #     downflag = 0
    #     GPIO.output(self.outpinUp,GPIO.HIGH)
    #     GPIO.output(self.outpinDown,GPIO.HIGH)
    #     time.sleep(0.000015)
    #     GPIO.output(self.outpinUp,GPIO.LOW)
    #     GPIO.output(self.outpinDown,GPIO.LOW)
    #     while 1:
    #         if(GPIO.input(self.inpinUp) and upflag == 0):
    #             upflag = 1
    #             tupu = time.time()
    #         if(GPIO.input(self.inpinDown) and downflag == 0):
    #             downflag = 1
    #             tdownu = time.time()
    #         if upflag == 1 and downflag == 1:
    #             break
    #     #发现高电平时开时计时
    #     while 1:
    #         if(not GPIO.input(self.inpinUp) and upflag == 1):
    #             upflag = 0
    #             tupd = time.time()
    #         if(not GPIO.input(self.inpinDown) and downflag == 1):
    #             downflag = 0
    #             tdownd = time.time()
    #         if upflag == 0 and downflag == 0:
    #             break
    #     #高电平结束停止计时
    #     #返回距离，单位为米
    #     return ((tupd-tupu)*340/2) < 0.3  ,((tdownd-tdownu)*340/2) < 0.3
    def rec_yes_or_no_up(self, my_pic):
        num = 0
        img = cv2.imread(my_pic)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    #    cv2.namedWindow('canny demo')
        canny = cv2.Canny(gray, 35, 50)
        #cv2.imshow('Canny', canny)
        #cv2.createTrackbar('Min threshold','canny demo',lowThreshold, max_lowThreshold, CannyThreshold)
        I_array = np.array(canny)
        for i in range(I_array.shape[0]):
            for j in range(I_array.shape[1]):
                if I_array[i][j] > 0:
                    num = num + 1
        print(my_pic + str(num))
        if num > 600:
            return 1
        else:
            return 0

    def rec_yes_or_no_down(self, my_pic):
        num = 0
        img = cv2.imread(my_pic)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #    cv2.namedWindow('canny demo')
        canny = cv2.Canny(gray, 35, 50)
        #cv2.imshow('Canny', canny)
        #cv2.createTrackbar('Min threshold','canny demo',lowThreshold, max_lowThreshold, CannyThreshold)
        I_array = np.array(canny)
        for i in range(I_array.shape[0]):
            for j in range(I_array.shape[1]):
                if I_array[i][j] > 0:
                    num = num + 1
        print(my_pic + str(num))
        if num > 900:
            return 1
        else:
            return 0


    def load_graph(self, model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)

        return graph
    def read_tensor_from_image_file(self, 
                            file_name,
                            input_height=224,
                            input_width=224,
                            input_mean=0,
                            input_std=255):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(
                file_reader, channels=3, name="png_reader")
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(
                tf.image.decode_gif(file_reader, name="gif_reader"))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
        else:
            image_reader = tf.image.decode_jpeg(
                file_reader, channels=3, name="jpeg_reader")
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result


    def load_labels(self, label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    def get_type(self, label):
        if(label == "fangkuai"):
            return "A"
        elif(label == "shuangwaiwai" or label == "wahaha" or label == "yangleduo"):
            return "B"
        elif(label == "xuehua" or label == "hongniu" ):
            return "C"
        elif(label == "wangqiu" or label == "mofang" or label == "telunsu" ):
            return "D"
        else:
            return "e"

    def classify_photos(self, file_name):

        label_file = "./output_labels.txt"
        t = []
        results = []
        top_k = []

        for i in range(3):
            t.append(self.read_tensor_from_image_file(file_name[i]))

        with tf.Session(graph=self.graph) as sess:
            for i in range(3):
                results.append(sess.run(self.output_operation.outputs[0], {
                    self.input_operation.outputs[0]: t[i]
                }))
        for i in range(3):
            results[i] = np.squeeze(results[i])
            top_k.append(results[i].argsort()[-5:][::-1])

        labels = self.load_labels(label_file)

        classify_num = 0
        type_of_photo = []
        for j in range(3):
            for i in top_k[j]:
                classify_num += 1
                if(results[j][i] > 0.5):
                    print(labels[i], results[j][i])
                    type_of_photo.append(self.get_type(labels[i]))
                    break
                elif(classify_num >= len(top_k[j])):
                    print("nothing was found!")
                    type_of_photo.append("none")
                    break
        return type_of_photo

    def classify_init(self):
        model_file = \
        "./output_graph.pb"
        label_file = "./output_labels.txt"
        input_height = 224
        input_width = 224
        input_mean = 0
        input_std = 255
        input_layer = "Placeholder"
        output_layer = "final_result"

        self.graph = self.load_graph(model_file)
        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        self.input_operation = self.graph.get_operation_by_name(input_name)
        self.output_operation = self.graph.get_operation_by_name(output_name)
    print("classify init complete")

    def redClean(self):
        GPIO.cleanup()
        print("red GPIO was released")

    def camrelease(self):
        self.cap.release()
