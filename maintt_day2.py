import time
ss = time.time()

import threading
import cv2 
from SerialControl import SerialControl
from Classify import Classify
from CarData import CarData
import Obt
import copy

key = 0

my_index = 1

classify = Classify()

scontrol = SerialControl()
classify.classify_init()
# toobad = [[[]]*83 for _ in range(83)]


Car = CarData(19,0,7,1)
classify.threadcam(0)
inf = 9999
sum_num = 0

A_num = 3
B_num = 3
C_num = 3
D_num = 3

get_things = [23,41,56,38]
A_pos = [0,1,2,3,4,5]
B_pos = [9,18,28,34,39,44]
C_pos = [72,73,74,75,76,77]
D_pos = [35,40,45,51,61,68]

things_up_down = {0:[0,0],1:[0,0],2:[0,0],3:[0,0],4:[0,0],5:[0,0],9:[0,0],18:[0,0],28:[0,0],34:[0,0],39:[0,0],44:[0,0],72:[0,0],73:[0,0],74:[0,0],75:[0,0],76:[0,0],77:[0,0],35:[0,0],40:[0,0],45:[0,0],51:[0,0],61:[0,0],68:[0,0]}

A_pos_up2 = [5,4,3,2,1,0]
B_pos_up2 = [44,39,34,28,18,9]
C_pos_up2 = [72,73,74,75,76,77]
D_pos_up2 = [35,40,45,51,61,68]

obt = -2
down_to = {0:10,1:11,2:12,3:13,4:14,5:15,9:8,28:27,34:33,44:43,72:64,74:65,75:66,77:67,35:36,45:46,51:52,68:69,40:78,61:79,73:80,76:81,39:82,18:83}
cst = 1

real_graph = [[68,69,70,71,72,73,74,75,76,77],
              [61,79,62,63,64,80,65,66,81,67],
              [51,52,53,54,55,56,57,58,59,60],
              [45,46,47,-1,-1,-1,-1,48,49,50],
              [40,78,41,-1,-1,-1,-1,42,43,44],
              [35,36,37,-1,-1,-1,-1,38,82,39],
              [29,30,31,-1,-1,-1,-1,32,33,34],
              [19,20,21,22,23,24,25,26,27,28],
              [10,11,12,13,14,15,16,17,83,18],
              [0, 1, 2, 3, 4, 5, 6, 7, 8,9]]



A = []
B = []
C = []
D = []
scontrol.clear()

print("before things_classify")

def update():
    for key in things_up_down:
        if things_up_down[key][0]==1 and things_up_down[key][1]==1:
            if key in A_pos:
                A_pos.remove(key)
            elif key in B_pos:
                B_pos.remove(key)
            elif key in C_pos:
                C_pos.remove(key)
            elif key in D_pos:
                D_pos.remove(key)



def things_classify(num_index):
    path = ['./L'+str(num_index)+'.jpg', './M'+str(num_index)+'.jpg', './R'+str(num_index)+'.jpg']
    num1, num2, num3 = classify.classify_photos(path)
    print(num1)
    print(num2)
    print(num3)
    if num_index == 1:
        A.append(num1)
        A.append(num2)
        A.append(num3)
    elif num_index == 2:
        B.append(num1)
        B.append(num2)
        B.append(num3)
    elif num_index == 3:
        C.append(num1)
        C.append(num2)
        C.append(num3)
    elif num_index == 4:
        D.append(num1)
        D.append(num2)
        D.append(num3)
print("before mydirection_old")

def storage_rec(pic_path_up,pic_path_down):
    print(pic_path_up)
    print(pic_path_down)
    print("1111111111111111111111")
    ph1 = classify.rec_yes_or_no_up(pic_path_up)
    ph2 = classify.rec_yes_or_no_down(pic_path_down)
    index = int(pic_path_up[1])
    if pic_path_up[0] == 'B':
        if ph1:
            things_up_down[B_pos_up2[index]][0] = 1
        if ph2:
            things_up_down[B_pos_up2[index]][1] = 1
    elif pic_path_up[0] == 'C':
        if ph1:
            things_up_down[C_pos_up2[index]][0] = 1
        if ph2:
            things_up_down[C_pos_up2[index]][1] = 1
    elif pic_path_up[0] == 'D':
        if ph1:
            things_up_down[D_pos_up2[index]][0] = 1
        if ph2:
            things_up_down[D_pos_up2[index]][1] = 1



def mydirection_old(src,path):
    print("mydirection_old")
    index = 0
    direction = []
    for i in range(len(real_graph)):  
        for j in range(len(real_graph[i])):  
            if real_graph[i][j] == src:
                Car.x = i
                Car.y = j
                break
    # 上0下3左2右1
    while index!=len(path):
        if (Car.y+1) < 10 and real_graph[Car.x][Car.y+1] == path[index]:
            direction.append(1)
            Car.y = Car.y + 1
        elif (Car.x+1) < 10 and real_graph[Car.x+1][Car.y] == path[index]:
            direction.append(3)
            Car.x = Car.x + 1
        elif (Car.y-1) >= 0 and real_graph[Car.x][Car.y-1] == path[index]:
            direction.append(2)
            Car.y = Car.y - 1
        elif (Car.x-1) >= 0 and real_graph[Car.x-1][Car.y] == path[index]:
            direction.append(0)
            Car.x = Car.x - 1
        index = index + 1
    Car.Id = path[len(path)-1]
    return direction
print("before jg_l")
def jg_l(a,b):
    print("jg_l")
    if (a == 2 and b == 0) or (a == 0 and b == 1) or (a == 1 and b == 3) or (a == 3 and b == 2):
        return 1
    else:
        return 0

print("before mydirection")
def mydirection(src,path):
    print("mydirection")
    index = 0
    direction = []
    for i in range(len(real_graph)):  
        for j in range(len(real_graph[i])):  
            if real_graph[i][j] == src:
                Car.x = i
                Car.y = j
                break
    #上0下3左2右1
    while index!=len(path):
        if (Car.y+1) < 10 and real_graph[Car.x][Car.y+1] == path[index]:
            direction.append(1)
            Car.y = Car.y + 1
        elif (Car.x+1) < 10 and real_graph[Car.x+1][Car.y] == path[index]:
            direction.append(3)
            Car.x = Car.x + 1
        elif (Car.y-1) >= 0 and real_graph[Car.x][Car.y-1] == path[index]:
            direction.append(2)
            Car.y = Car.y - 1
        elif (Car.x-1) >= 0 and real_graph[Car.x-1][Car.y] == path[index]:
            direction.append(0)
            Car.x = Car.x - 1
        index = index + 1
    Car.Id = path[len(path)-1]
    real_direction = []
    for val in range(len(direction)):
        if(direction[val] == Car.state):
            real_direction.append(0)
        elif((direction[val] + Car.state) == 3):
            real_direction.append(3)
        elif(jg_l(direction[val],Car.state) == 1):
            real_direction.append(2)
            real_direction.append(0)
            Car.state = direction[val]
        else:
            real_direction.append(1)
            real_direction.append(0)
            Car.state = direction[val]
    return real_direction
print("before py_to_arduino")
def py_to_arduino(direction):
    print("direction : ")
    print(direction)
    val = 0
    forward_time = 0
    back_time = 0
    while(val < len(direction)):
        if(direction[val] == 0):
            #forward(1)
            #            scontrol.car_go()
            forward_time = val + 1
            while(forward_time < len(direction)):
                if(direction[forward_time] == 0):
                    forward_time += 1
                else:
                    break
            if(forward_time == val + 1):
                scontrol.car_go()
            else:
                scontrol.fast_go(forward_time - val)
                val = forward_time - 1
                        

        elif(direction[val] == 3):
            #back(1)
#            scontrol.car_back()
            back_time = val + 1
            while(back_time < len(direction)):
                if(direction[back_time] == 3):
                    back_time += 1
                else:
                    break
            if(back_time == val + 1):
                scontrol.car_back()
            else:
                # print('加速后*' + str(back_time - val))
                scontrol.fast_back(back_time - val)
                val = back_time - 1
                
                

        elif(direction[val] == 2):
            #turn_left
            #forward(1)
            scontrol.car_left()
            # print('左 ')

        else:
            #turn_right
            #forward(1)       
            scontrol.car_right()
            # print('右 ')
        val = val + 1

print("before py_to_arduino_r")
def py_to_arduino_r(direction):
    print("direction : ")
    print(direction)
    val = 0
    forward_time = 0
    back_time = 0
    while(val < len(direction)):
        if(direction[val] == 3):
            #forward(1)
            #            scontrol.car_go()
            forward_time = val + 1
            while(forward_time < len(direction)):
                if(direction[forward_time] == 3):
                    forward_time += 1
                else:
                    break
            if(forward_time == val + 1):
                scontrol.car_go()
            else:
                # print('加速前*' + str(forward_time - val))
                scontrol.fast_go(forward_time - val)
                val = forward_time - 1
    
        
        elif(direction[val] == 0):
            #back(1)
            #            scontrol.car_back()
            back_time = val + 1
            while(back_time < len(direction)):
                if(direction[back_time] == 0):
                    back_time += 1
                else:
                    break
            if(back_time == val + 1):
                scontrol.car_back()
            else:
                # print('加速后*' + str(back_time - val))
                scontrol.fast_back(back_time - val)
                val = back_time - 1
        
        
        
        elif(direction[val] == 2):
            #turn_left
            #forward(1)
            scontrol.car_left()

        else:
            #turn_right
            #forward(1)
            scontrol.car_right()

        val = val + 1

            


print("before make_right")
def make_right(direction):
    print("make_right")
    if((direction + Car.state) == 3):
        #180
        scontrol.car_return()
        Car.state = direction
    elif(jg_l(direction,Car.state) == 1):
        #turn_left
        scontrol.car_left()
        Car.state = direction
    elif(Car.state != direction):
        #turn_right
        scontrol.car_right()
        Car.state = direction
print("before Cinit")




def Cinit():
    print("cinit")
    global cst,obt
    val = 0
    num_index = 1
    store_index = 0
    classify_threads = []
    store_threads = []
    scontrol.car_fast_middle()
    scontrol.car_left()
    D_box = [1,2,3,4,5,6]
    C_box = [7,8,9,10,11,12]
    B_box = [13,14,15,16,17,18]
    A_box = [19,20,21,22,23,24]
    while(val < 25):
        if(val==0):
            scontrol.car_go()
            scontrol.car_go()
        if(val in D_box):
            if cst == 1:
                if classify.obt() == 0:
                    print("have zhangaiwu")
                    obt = down_to[D_pos_up2[val-1]]
                    cst = 0
                    for i in range(len(real_graph)):
                        for j in range(len(real_graph[i])):
                            if real_graph[i][j] == obt:
                                real_graph[i][j] = -1
            ms = time.time()
            time.sleep(0.2)
            classify.cut(1)
            print(time.time() - ms)
            ms = time.time()
            pic_path_up = 'D' + str(val-1) + '0.jpg'
            pic_path_down = 'D' + str(val-1) + '1.jpg'
            t = threading.Thread(target=storage_rec,args=(pic_path_up,pic_path_down))
            store_threads.append(t)
            store_threads[store_index].start()
            store_index += 1
            print(time.time() - ms)

            if val == 6:
                scontrol.car_init_right()
                scontrol.fast_go(4)
            else:
                scontrol.car_go()
                
        if(val in C_box):
            if cst == 1:
                if classify.obt() == 0:
                    obt = down_to[C_pos_up2[val-7]]
                    cst = 0
                    for i in range(len(real_graph)):
                        for j in range(len(real_graph[i])):
                            if real_graph[i][j] == obt:
                                real_graph[i][j] = -1
            time.sleep(0.2)
            classify.cut(1)
            pic_path_up = 'C' + str(val-7) + '0.jpg'
            pic_path_down = 'C' + str(val-7) + '1.jpg'
            t = threading.Thread(target=storage_rec,args=(pic_path_up,pic_path_down))
            store_threads.append(t)
            store_threads[store_index].start()
            store_index += 1
            if val == 12:
                scontrol.car_init_right()
                scontrol.fast_go(4)
            else:
                scontrol.car_go()
   

        if(val in B_box):
            if cst == 1:
                if classify.obt() == 0:
                    obt = down_to[B_pos_up2[val-13]]
                    cst = 0
                    for i in range(len(real_graph)):
                        for j in range(len(real_graph[i])):
                            if real_graph[i][j] == obt:
                                real_graph[i][j] = -1
            time.sleep(0.2)
            classify.cut(1)
            pic_path_up = 'B' + str(val-13) + '0.jpg'
            pic_path_down = 'B' + str(val-13) + '1.jpg'
            t = threading.Thread(target=storage_rec,args=(pic_path_up,pic_path_down))
            store_threads.append(t)
            store_threads[store_index].start()
            store_index += 1
            if val == 18:
                scontrol.fast_back(2)
                scontrol.car_init_left()
                scontrol.fast_back(5)
            else:
                scontrol.car_go()
        val = val + 1
    
    print("#######")
    print(things_up_down)
    print("#######")
    classify.redClean()
    classify_threads = []
    while num_index <=4:
        classify.numUpdate(num_index)
        time.sleep(0.5)
        classify.cut(3)
        t = threading.Thread(target=things_classify,args=(num_index,))
        classify_threads.append(t)
        classify_threads[num_index-1].start()
        scontrol.fast_go(3)
        scontrol.car_right()
        scontrol.fast_go(2)
        num_index += 1

if __name__ == '__main__':
    cmd = input("\npress enter to start!")
    scontrol.jixiebi(9)
    tt = time.time()
    print("main init time:" + str(tt-ss))
    Cinit()
    print("obt-----" + str(obt))
    if obt == 78:
        special_id = 40
    elif obt == 79:
        special_id = 61
    elif obt == 80:
        special_id = 73
    elif obt == 81:
        special_id = 76
    elif obt == 82:
        special_id = 39
    elif obt == 83:
        special_id = 18
    toobad = copy.deepcopy(Obt.obt_p(obt))
    Car.Id = 23
    Car.state = 1
    print("stop safe")
    update()
    print("update safe")
    A_index = [0,1,2]
    B_index = [0,1,2]
    C_index = [0,1,2]
    D_index = [0,1,2]
    shortest=[]
    while((A_num != 0) or (B_num != 0) or (C_num != 0) or (D_num != 0)):
        # path=Car.dijkstra(graph_list,Car.Id,get_things)
        print("into while")
        short = inf
        for i in get_things:
            if len(toobad[Car.Id][i]) < short:
                short = len(toobad[Car.Id][i])
                shortest = toobad[Car.Id][i]
        if shortest:
            path = shortest[1:]
        else:
            path = shortest
        short = inf


        print(path)
        if path:
            direction = mydirection(Car.Id,path)
            py_to_arduino(direction)
       

        print(Car.Id)
        if Car.Id == 23:
            while('none' in A):
                make_right(1)
                A.clear()
                classify.cut(3)
                things_classify(1)
            make_right(0)
            index_flag = 0
            for index in A_index:
                if A[index] == 'A':
                    the_num = index
                    target = A[index]
                    index_flag = 1
                    break
                elif A[index] == 'B' or A[index] == 'D':
                    the_num = index
                    target = A[index]
                    index_flag = 1
            if index_flag == 0:
                target = 'C'
                the_num = A_index[-1]
                A_index.remove(the_num)
            else:
                A_index.remove(the_num)
            
            if(target in ["A","B","C","D"]):
                scontrol.Catch_things(the_num+1)
            A_num = A_num - 1
            if (A_num == 0 and 23 in get_things):
                get_things.remove(23)

        elif Car.Id == 41:
            while('none' in D):
                make_right(3)
                D.clear()
                classify.cut(3)
                things_classify(4)
            make_right(1)
            index_flag = 0
            for index in D_index:
                if D[index] == 'D':
                    the_num = index
                    target = D[index]
                    index_flag = 1
                    break
                elif D[index] == 'A' or D[index] == 'C':
                    the_num = index
                    target = D[index]
                    index_flag = 1
            if index_flag == 0:
                target = 'B'
                the_num = D_index[-1]
                D_index.remove(the_num)
            else:
                D_index.remove(the_num)
            
            if(target in ["A","B","C","D"]):
                scontrol.Catch_things(the_num+1)
            D_num = D_num - 1
            if (D_num == 0 and 41 in get_things):
                get_things.remove(41)

        elif Car.Id == 38:
            while('none' in B):
                make_right(0)
                B.clear()
                classify.cut(3)
                things_classify(2)
            make_right(2)
            index_flag = 0
            for index in B_index:
                if B[index] == 'B':
                    the_num = index
                    target = B[index]
                    index_flag = 1
                    break
                elif B[index] == 'A' or B[index] == 'C':
                    the_num = index
                    target = B[index]
                    index_flag = 1
            if index_flag == 0:
                target = 'D'
                the_num = B_index[-1]
                B_index.remove(the_num)
            else:
                B_index.remove(the_num)
            if(target in ["A","B","C","D"]):
                scontrol.Catch_things(the_num+1)
            B_num = B_num - 1
            if (B_num == 0 and 38 in get_things):
                get_things.remove(38)
            
        elif Car.Id == 56:
            while('none' in C):
                make_right(2)
                C.clear()
                classify.cut(3)
                things_classify(3)
            make_right(3)
            index_flag = 0
            for index in C_index:
                if C[index] == 'C':
                    the_num = index
                    target = C[index]
                    index_flag = 1
                    break
                elif C[index] == 'D' or C[index] == 'B':
                    the_num = index
                    target = C[index]
                    index_flag = 1
            if index_flag == 0:
                target = 'A'
                the_num = C_index[-1]
                C_index.remove(the_num)
            else:
                C_index.remove(the_num)
            if(target in ["A","B","C","D"]):
                scontrol.Catch_things(the_num+1)
            C_num = C_num - 1
            if (C_num == 0 and 56 in get_things):
                get_things.remove(56)


        if target == 'A':
            # path = Car.dijkstra(graph_list,Car.Id,A_pos)
            print(things_up_down)
            print("##############")
            print(Car.Id)
            print("A_pos : ")
            print(A_pos)
            print(short)
            if A_pos:
                for i in A_pos:
                    if len(toobad[Car.Id][i]) < short:
                        short = len(toobad[Car.Id][i])
                        shortest = toobad[Car.Id][i]
                if shortest:
                    path = shortest[1:]
            else:
                print("A_pos has no place")
                # 释放机械臂
                continue

            short=inf
            print(path)
            Car.state = 3 - Car.state
            direction = mydirection(Car.Id,path)
            py_to_arduino_r(direction)
            Car.state = 3 - Car.state
            make_right(0)
            if things_up_down[Car.Id][0] == 0:
                scontrol.jixiebi(0)
                things_up_down[Car.Id][0] = 1
            else:
                scontrol.lowbi()
                things_up_down[Car.Id][1] = 1
            if Car.Id == special_id:
                time.sleep(1)
         


        elif target == 'B':
            # path = Car.dijkstra(graph_list,Car.Id,B_pos)
            print("CarId：")
            print(Car.Id)
            print(toobad[Car.Id][39])
            if B_pos:
                for i in B_pos:
                    if len(toobad[Car.Id][i]) < short:
                        short = len(toobad[Car.Id][i])
                        shortest = toobad[Car.Id][i]
                print("CarId：")
                print(Car.Id)
                print("shortest:")
                print(shortest)
                if shortest:
                    path = shortest[1:]
            else:
                print("B_pos has no place")
                # 释放机械臂
                continue
            short=inf
            print("path:")
            print(path)
            Car.state = 3 - Car.state
            direction = mydirection(Car.Id,path)
            py_to_arduino_r(direction)
            Car.state = 3 - Car.state
            make_right(2)
            if things_up_down[Car.Id][0] == 0:
                scontrol.jixiebi(0)
                things_up_down[Car.Id][0] = 1
            else:
                scontrol.lowbi()
                things_up_down[Car.Id][1] = 1
            if Car.Id == special_id:
                time.sleep(1)
           
        elif target == 'C':
            # path = Car.dijkstra(graph_list,Car.Id,C_pos)
            if C_pos:
         
                for i in C_pos:
                    if len(toobad[Car.Id][i]) < short:
                        short = len(toobad[Car.Id][i])
                        shortest = toobad[Car.Id][i]
                if shortest:
                    path = shortest[1:]
            else:

                print("C_pos has no place")
                # 释放机械臂
                continue
            short=inf
            print(path)
            Car.state = 3 - Car.state
            direction = mydirection(Car.Id,path)
            py_to_arduino_r(direction)
            Car.state = 3 - Car.state
            make_right(3)
            if things_up_down[Car.Id][0] == 0:
                scontrol.jixiebi(0)
                things_up_down[Car.Id][0] = 1
            else:
                scontrol.lowbi()
                things_up_down[Car.Id][1] = 1
            if Car.Id == special_id:
                time.sleep(1)
           
        elif target == 'D':
            # path = Car.dijkstra(graph_list,Car.Id,D_pos)
            if D_pos:
                for i in D_pos:
                    if len(toobad[Car.Id][i]) < short:
                        short = len(toobad[Car.Id][i])
                        shortest = toobad[Car.Id][i]
                if shortest:
                    path = shortest[1:]
            else:
                print("D_pos has no place")
                # 释放机械臂
                continue
            short=inf
            print(path)
            Car.state = 3 - Car.state
            direction = mydirection(Car.Id,path)
            py_to_arduino_r(direction)
            Car.state = 3 - Car.state
            make_right(1)
            if things_up_down[Car.Id][0] == 0:
                scontrol.jixiebi(0)
                things_up_down[Car.Id][0] = 1
            else:
                scontrol.lowbi()
                things_up_down[Car.Id][1] = 1
            if Car.Id == special_id:
                time.sleep(1)
            
        update()
    mt = time.time()
    print("total time:" + str(mt - tt))
    classify.stop()
    classify.camrelease()
    print(things_up_down)
    # except Exception as e:
    #     classify.redClean()
    #     classify.stop()
    #     classify.camrelease()
    #     print(e)


    # try:
    #     work()
    # except Exception as e:
    #     classify.redClean()
    #     classify.stop()
    #     classify.camrelease()
    #     print(e)
