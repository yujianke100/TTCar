import serial
import binascii
import time
import RPi.GPIO as GPIO

class SerialControl:
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(21, GPIO.IN)
    # GPIO.setup(3, GPIO.IN)

    # outpinUp = 35
    # inpinUp = 37
    # outpinDown = 11
    # inpinDown = 13

    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(outpinUp,GPIO.OUT,initial=GPIO.LOW)
    # GPIO.setup(inpinUp,GPIO.IN)
    # GPIO.setup(outpinDown,GPIO.OUT,initial=GPIO.LOW)
    # GPIO.setup(inpinDown,GPIO.IN)

    turnFlag = 1

    leftRightFlag = 1

    tn = 0
    bn = 0
    tf = 1
    bf = 1
    serialPort = "/dev/ttyACM0"  # 串口
    baudRate = 9600  # 波特率
    serialPort2 = "/dev/ttyS0"
    ser = serial.Serial(serialPort, baudRate, timeout=0.2)
    ser2 = serial.Serial(serialPort2, baudRate, timeout=0.5)
    print("UNO板：串口=%s ，波特率=%d" % (serialPort, baudRate))
    print("机械臂：串口=%s ，波特率=%d" % (serialPort2, baudRate))
    ser.write("h".encode())
    # ser.write("c".encode())
    # ser.flush()

    stopCmd = '55550207'
    stopCmd_list = []
    for i in stopCmd.split():
        stopCmd_list.append(binascii.a2b_hex(i))
    s = time.time()
    time.sleep(0.2)
    t02 = time.time() - s

    # s = time.time()
    # time.sleep(0.05)
    # t005 = time.time() - s

    s = time.time()
    time.sleep(0.8)
    t08 = time.time() - s

    s = time.time()
    time.sleep(0.7)
    t07 = time.time() - s

    # def rec_yes_or_no(self):
    #     try:
    #         upflag = 0
    #         downflag = 0
    #         GPIO.output(self.outpinUp,GPIO.HIGH)
    #         GPIO.output(self.outpinDown,GPIO.HIGH)
    #         time.sleep(0.000015)
    #         GPIO.output(self.outpinUp,GPIO.LOW)
    #         GPIO.output(self.outpinDown,GPIO.LOW)
    #         while 1:
    #             if(GPIO.input(self.inpinUp) and upflag == 0):
    #                 upflag = 1
    #                 tupu = time.time()
    #             if(GPIO.input(self.inpinDown) and downflag == 0):
    #                 downflag = 1
    #                 tdownu = time.time()
    #             if upflag == 1 and downflag == 1:
    #                 break
    #         #发现高电平时开时计时
    #         while 1:
    #             if(not GPIO.input(self.inpinUp) and upflag == 1):
    #                 upflag = 0
    #                 tupd = time.time()
    #             if(not GPIO.input(self.inpinDown) and downflag == 1):
    #                 downflag = 0
    #                 tdownd = time.time()
    #             if upflag == 0 and downflag == 0:
    #                 break
    #         return ((tupd-tupu)*340/2)  ,((tdownd-tdownu)*340/2)
    #     except:
    #         GPIO.cleanup()
    #         print("GPIO cleand")
    def car_togo(self):
        self.ser.write("h".encode())
        self.turnFlag = 1

    def car_toback(self):
        self.ser.write("t".encode())
        self.turnFlag = -1

    def jixiebi(self,choose):
        self.ser2.flush()
        self.ser2.writelines(self.stopCmd_list) 
        if(choose == 0):
            time.sleep(0.2)
        #a = '5555080301E80301E803'
            a = '55550506000100' #放
        elif(choose == 1):
            a = '55550506010100' #取左
        elif(choose == 2):
            a = '55550506020100' #取右
        elif(choose == 3):
            a = '55550506030100' #取中
        elif(choose == 4):
            a = '55550506040100' #特殊放上
        elif(choose == 5):
            a = '55550506050100' #特殊放下
        elif(choose == 6):
            a = '55550506060100' #看右
        elif(choose == 7):
            a = '55550506070100' #看仓库
        elif(choose == 8):
            a = '55550506080100' #看货架
        elif(choose == 9):
            a = '55550506090100' #看货架
        elif(choose == 10):
            a = '555505060A0100' #放下
        elif(choose == 11):
            a = '555505060B0100' #反看仓库
        elif(choose == 12):
            a = '55550207' #中断
        a_list = []
        for i in a.split():
            a_list.append(binascii.a2b_hex(i))
        time.sleep(0.1)
        self.ser2.writelines(a_list)
        if(choose == 0):
            self.car_togo()
            self.car_little()
            time.sleep(0.5)
            self.car_toback()
            self.car_little()
            time.sleep(0.5)
            self.car_little()
            time.sleep(0.5)
            self.car_togo()
            turnFlag = 1
            time.sleep(0.5)
        elif(choose == 4 or choose == 5):
            time.sleep(4)
        elif(choose == 6):
            time.sleep(2)

    def clear(self):
        self.ser.write("c".encode())
        self.ser.flush()

    def TopRedNum(self):
        if(int(GPIO.input(3)) == 0 and self.tf == 1):
            self.tn += 1
            self.tf = 0
            print("tn:" + str(self.tn))
        if(int(GPIO.input(3)) == 1 and self.tf == 0):
            self.tf = 1

    def TopFlag(self):
        n = self.tn
        self.tn = 0
        return n

    def getStop(self):
        data = 0
        while (1):
            data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
            # print(data)
            if(data == 1):
                return 1
            elif(data == 6):
                return 6
            elif(data == 5):
                return 5
            elif(data == 7):
                return 7
            elif(data == 4):
                return 4
    # def getStop(self):
    #     data = 0
    #     s = time.time()
    #     while (1):
    #         mt = time.time()
    #         if(mt - s) > self.t08:
    #             break
    #         data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #         # print(data)
    #         if(data == 1):
    #             return 1
    #         elif(data == 6):
    #             return 6
    #         elif(data == 5):
    #             return 5
    #     t = time.time()
    #     if (t - s) < self.t02:
    #         print("stop time too short")
    #         # self.ser.write("1".encode())
    #         data = 0
    #         while (1):
    #             mt = time.time()
    #             if(mt - s) > self.t08:
    #                 break
    #             data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #             # print(data)
    #             if(data == 1):
    #                 return 1
    #             elif(data == 6):
    #                 return 6
    #             elif(data == 5):
    #                 return 5
    #     return 0

    # def newgetStop(self):
    #     data = 0
    #     s = time.time()
    #     while (1):
    #         mt = time.time()
    #         if(mt - s) > self.t08:
    #             break
    #         data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #         if(data == 1):
    #             break
    #         elif(data == 6 or data == 5):
    #             return data
    #     t = time.time()
    #     if (t - s) < self.t02:
    #         print("stop time too short")
    #         # self.ser.write("1".encode())
    #         data = 0
    #         while (1):
    #             mt = time.time()
    #             if(mt - s) > self.t08:
    #                 break
    #             data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #             if(data == 1):
    #                 break
    #             elif(data == 6 or data == 5):
    #                 return data
    #     return data
    def newgetStop(self):
        data = 0
        while (1):
            data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
            if(data == 1):
                return 1
            elif(data == 6):
                return 6
            elif(data == 5):
                return 5
            elif(data == 7):
                return 7
            elif(data == 4):
                return 4

    # def largegetStop(self):
    #     s = time.time()
    #     data = 0
    #     while (1):
    #         data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #         if(data == 1):
    #             break
    #         elif(data == 6 or data == 5):
    #             return data
    #     t = time.time()
    #     if (t - s) < self.t02:
    #         print("stop time too short")
    #         # self.ser.write("1".encode())
    #         data = 0
    #         while (1):
    #             data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #             if(data == 1):
    #                 break
    #             elif(data == 6 or data == 5):
    #                 return data
    #     return data
    def largegetStop(self):
        data = 0
        while (1):
            data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
            if(data == 1):
                return 1
            elif(data == 6):
                return 6
            elif(data == 5):
                return 5
            elif(data == 7):
                return 7
            elif(data == 4):
                return 4
        
    def initgetStop(self):
        s = time.time()
        data = 0
        while (1):
            data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
            if(data == 1 or data == 8):
                return data
        t = time.time()
        if (t - s) < self.t02:
            print("stop time too short")
            # self.ser.write("1".encode())
            data = 0
            while (1):
                data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
                if(data == 1 or data == 8):
                    return data

    # def initgetStop(self):
    #     data = 0
    #     phflag = False
    #     ph1f = 1.0
    #     ph2f = 1.0
    #     s = time.time()
    #     while (1):
    #         mt = time.time()
    #         if(mt - s) > self.t07:
    #             break
    #         data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #         if(data == 1):
    #             break
    #         if(data == 9):
    #             phflag = True
    #         if(phflag):
    #             ph1, ph2 = self.rec_yes_or_no()
    #             if(ph1f > ph1):
    #                 ph1f = ph1
    #             if(ph2f > ph2):
    #                 ph2f = ph2
    #     t = time.time()
    #     if (t - s) < self.t02:
    #         print("stop time too short")
    #         # self.ser.write("s".encode())
    #         data = 0
    #         while (1):
    #             data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #             if(data == 1):
    #                 break
    #             if(data == 9):
    #                 phflag = True
    #             if(phflag):
    #                 ph1, ph2 = self.rec_yes_or_no()
    #                 if(ph1f > ph1):
    #                     ph1f = ph1
    #                 if(ph2f > ph2):
    #                     ph2f = ph2
    #             # if(data == 9):
    #             #     phflag = True
    #             # if(phflag):
    #             #     ph1, ph2 = self.rec_yes_or_no()
    #             #     if(ph1):
    #             #         print("ph1f true")
    #             #         ph1f = True
    #             #     if(ph2):
    #             #         print("ph2f true")
    #             #         ph2f = True
    #     return ph1f < 0.3, ph2f < 0.3
    def getState(self):
        data = 0
        data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
        if(data == 8):
            return 1
        elif(data == 9):
            return 0
        else:
            return -1

    def car_go(self):
        print("car_go")
        self.car_togo()
        self.ser.write("7".encode())
        e = self.getStop()
        # time.sleep(0.25)
        # if(e == 6):
        #     print("too go and back")
        #     time.sleep(1)
        #     self.car_back()
        #     print(e)
        # elif(e == 5):
        #     print("extra go")
        #     self.car_go()
            # time.sleep(1)
            # self.car_back()

    def car_old_go(self):
        self.car_togo()
        self.ser.write("1".encode())
        self.getStop()

    def after_fast_go(self):
        self.car_togo()
        self.ser.write("8".encode())
        self.getStop()

    def after_fast_back(self):
        self.car_toback()
        self.ser.write("8".encode())
        self.getStop()

    def car_back(self):
        print("car back")
        self.car_toback()
        self.ser.write("7".encode())
        e = self.getStop()
        # time.sleep(0.25)
        # print(e)
        # if(e == 6):
        #     time.sleep(1)
        #     print("too back and go")
        #     self.car_go()
        # elif(e == 5):
        #     print("extra back")
        #     self.car_back()
            # time.sleep(1)
            # self.car_go()
        # self.car_togo()

    def car_start_back(self):
        print("car back")
        self.car_toback()
        self.ser.write("9".encode())
        self.getStop()

    def car_old_back(self):
        print("car back")
        self.car_toback()
        self.ser.write("1".encode())
        self.getStop()
        self.car_togo()

    # def car_init_back(self):
    #     print("car back")
    #     self.car_toback()
    #     self.ser.write("u".encode())
    #     ph1, ph2 = self.initgetStop()
    #     self.car_togo()
    #     return ph1, ph2

    def car_init_left(self):
        # time.sleep(0.3)
        # self.car_togo()
        self.leftRightFlag = 1
        self.ser.write("2".encode())
        e = self.getStop()
        print(e)
        time.sleep(0.3)
        if(e == 7):
            self.ser.write("3".encode())
            self.getStop()
            if(self.turnFlag == 1):
                time.sleep(0.25)
                self.car_toback()
                time.sleep(0.25)
                self.ser.write("7".encode())
                self.getStop()
                time.sleep(0.25)
                self.car_togo()
                time.sleep(0.25)
                self.ser.write("7".encode())
                self.getStop()
            else:
                time.sleep(0.25)
                self.car_togo()
                time.sleep(0.25)
                self.ser.write("7".encode())
                self.getStop()
                time.sleep(0.25)
                self.car_toback()
                time.sleep(0.25)
                self.ser.write("7".encode())
                self.getStop()
            time.sleep(0.25)
            self.car_left()


    def car_init_right(self):
        # time.sleep(0.3)
        # self.car_togo()
        self.leftRightFlag = -1
        self.ser.write("3".encode())
        e = self.getStop()
        time.sleep(0.3)
        if(e == 7):
            self.ser.write("2".encode())
            self.getStop()
            if(self.turnFlag == 1):
                time.sleep(0.25)
                self.car_toback()
                time.sleep(0.25)
                self.ser.write("7".encode())
                self.getStop()
                time.sleep(0.25)
                self.car_togo()
                time.sleep(0.25)
                self.ser.write("7".encode())
                self.getStop()
            else:
                time.sleep(0.25)
                self.car_togo()
                time.sleep(0.25)
                self.ser.write("7".encode())
                self.getStop()
                time.sleep(0.25)
                self.car_toback()
                time.sleep(0.25)
                self.ser.write("7".encode())
                self.getStop()
            time.sleep(0.25)
            self.car_right()

    def car_left(self):
        # self.car_togo()
        time.sleep(0.3)
        self.car_init_left()

    def car_right(self):
        # self.car_togo()
        time.sleep(0.3)
        self.car_init_right()

    def car_return(self):
        time.sleep(0.5)
        self.car_togo()
        self.ser.write("3".encode())
        self.getStop()
        self.ser.write("3".encode())
        self.getStop()

    def car_little(self):
        self.ser.write("l".encode())
        self.getStop()

    def car_low_little(self):
        self.ser.write("L".encode())
        self.getStop()

    def car_fast_little(self):
        self.ser.write("L".encode())
        self.getStop()

    # def car_toline(self):
    #     print("in toline")
    #     self.ser.write("0".encode())
    #     data = 0
    #     s = time.time()
    #     while (1):
    #         data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #         if(data == 1):
    #             print("out of stop")
    #             break
    #     t = time.time()
    #     if (t - s) < self.t02:
    #         print(" toline stop time too short")
    #         self.ser.write("0".encode())
    #         data = 0
    #         while (1):
    #             data = int.from_bytes(self.ser.read(), byteorder='little', signed=True)
    #             if(data == 1):
    #                 print("out of stop")
    #                 break
    def before_toline(self):
        self.ser.write("z".encode())
        e = self.getStop()
        if(e == 4):
            if(self.leftRightFlag == 1):
                self.car_right()
                self.car_go()
                time.sleep(0.5)
                self.car_back()
                time.sleep(0.5)
                self.car_left()
            elif(self.leftRightFlag == -1):
                self.car_left()
                self.car_go()
                time.sleep(0.5)
                self.car_back()
                time.sleep(0.5)
                self.car_right()

    def car_toline(self):
        self.car_togo()
        self.ser.write("0".encode())
        self.getStop()

    def car_middle(self):
        self.ser.write("4".encode())
        self.getStop()
    def car_fast_middle(self):
        self.ser.write("m".encode())
        self.getStop()

    def car_special_back(self):
        self.car_toback()
        self.ser.write("7".encode())
        self.getStop()

    def Catch_things(self,num):
        self.before_toline()
        # if(self.getState() == 0):
        #     print("update")
        #     self.car_togo()
        #     self.car_toline()
        #     self.car_little()
        #     self.car_little()
        #     self.car_little()
        #     time.sleep(0.5)
        #     self.car_back()
        time.sleep(0.3)
        self.jixiebi(num)
        time.sleep(0.5)
        self.car_togo()
        time.sleep(0.3)
        # self.car_togo()
        # self.car_little()
        # self.car_little()
        # self.car_little()
        # self.car_little()
        self.car_toline()
        if(num == 1):
            self.car_little()
            self.car_low_little()
            time.sleep(1.2)
            # self.car_toback()
            # self.car_toback()
        elif(num == 2):
            self.car_little()
            time.sleep(0.2)
            self.car_low_little()
            time.sleep(1)
            # self.car_toback()
            # self.car_little()
            # self.car_little()
        else:
            # self.car_little()
            time.sleep(0.3)
            self.car_low_little()
            time.sleep(0.7)
            self.car_little()
            time.sleep(0.2)
            # self.car_toback()
            # self.car_little()
            # self.car_little()
            # self.car_little()
        # self.car_little()
        # self.car_little()
        # self.car_little()
        # self.car_little()
        self.car_special_back()
        # self.car_toback()

    def special_Catchthings(self, num):
        self.before_toline()
        self.car_toline()
        self.car_little()
        self.car_little()
        time.sleep(0.2)
        self.car_special_back()
        self.car_togo()
        self.Catch_things(num)

    def lowbi(self):
        self.jixiebi(10)
        # self.car_fast_middle()
        # self.car_fast_middle()
        time.sleep(1.5)
        self.car_toback()
        # self.car_little()
        # self.car_little()
        self.car_little()
        time.sleep(1.5)
        self.car_togo()
        # self.car_toback()
        # self.car_little()
        # self.car_little()
        # self.car_little()
        # time.sleep()
        # self.car_little()
        # self.car_little()
        # self.jixiebi(5)
        # self.jixiebi(6)
        # self.car_back()

    def fast_go(self,num):
        self.car_togo()
        # self.ser.write("9".encode())
        # time.sleep(0.3)
        if(num == 2):
            self.ser.write("A".encode())
        elif(num == 3):
            self.ser.write("B".encode())
        elif(num == 4):
            self.ser.write("C".encode())
        elif(num == 5):
            self.ser.write("D".encode())
        elif(num == 6):
            self.ser.write("E".encode())
        elif(num == 7):
            self.ser.write("F".encode())
        e = self.largegetStop()
        # if(e == 6):
        #     print("too go and back")
        #     time.sleep(1)
        #     self.car_back()
        # elif(e == 5):
        #     print("extra go")
        #     self.car_go()
        # self.ser.write("f".encode())
        # self.newgetStop()
        # self.after_fast_go()
        # self.ser.write("8".encode())
        # self.getStop()
        # 
        # time.sleep(0.2)


    def fast_back(self,num):
        self.car_toback()
        # self.ser.write("9".encode())
        # time.sleep(0.3)
        if(num == 2):
            self.ser.write("A".encode())
        elif(num == 3):
            self.ser.write("B".encode())
        elif(num == 4):
            self.ser.write("C".encode())
        elif(num == 5):
            self.ser.write("D".encode())
        elif(num == 6):
            self.ser.write("E".encode())
        elif(num == 7):
            self.ser.write("F".encode())
        e = self.largegetStop()
        # if(e == 6):
        #     time.sleep(1)
        #     print("too back and go")
        #     self.car_go()
        # elif(e == 5):
        #     print("extra back")
        #     self.car_back()
        # self.car_toback()
        # self.ser.write("f".encode())
        # self.newgetStop()
        # self.after_fast_back()
        # self.ser.write("8".encode())
        # self.getStop()
        # time.sleep(0.2)

    # def fast_back_init(self,num):
    #     # self.car_toback()
    #     # self.ser.write("1".encode())
    #     # time.sleep(0.3)
    #     # for i in range(num):
    #     #     self.ser.write("f".encode())
    #     #     self.getStop()
    #     # self.car_togo()
    #     self.car_old_back()
    #     for i in range(num - 1):
    #         s = time.time()
    #         # self.car_toback()
    #         self.ser.write("f".encode())
    #         self.newgetStop()
    def fast_go_init(self):
        self.ser.write("G".encode())

    def fast_go_init2(self):
        self.car_togo()
    
    def fast_go_init_info(self):
        return self.initgetStop()
        
    # def car_super_back(self):
    #     self.car_toback()
    #     self.ser.write("s".encode())
    #     ph1, ph2 = self.initgetStop()
    #     self.car_togo()
    #     return ph1 , ph2
    print("SerialControl init complete")

    # def soundClean(self):
    #     GPIO.cleanup()
    #     print("SerialControl GPIO was released")