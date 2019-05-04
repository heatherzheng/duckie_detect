import numpy as np
import scipy.optimize as optimization
import matplotlib.pyplot as plt
import math
def func(x, a, b):
    return a + b*x

def func1(x, a, b, c):
    return a + b*x + c*x*x

def main():

    bot_w = 5
    bot_h = 3.8
    upperleft_x = []
    upperleft_y = []
    bottomright_x = []
    bottomright_y = []
    real_dist = []
    real_angle = []
    center_x = []
    center_y = []
    box_x = []
    box_y = []
    box_min = []
    with open("../data/data_yolo.txt") as f:
        content = f.readlines()
        for i in content:
            i = i.strip("\n")
            i = i.split()
            y = float(i[0])
            x = float(i[1])
            dist = math.sqrt(x**2 + y**2)
            if x==0:
                angle = 0
            else:
                angle = (90 - math.degrees(math.atan(abs(y)/abs(x)))) * (-math.copysign(1, x))
            print(angle,dist)
            real_angle.append(angle)
            real_dist.append(dist)


            upperleft_x.append(float(i[2]))
            upperleft_y.append(float(i[3]))
            bottomright_x.append(float(i[4]) + float(i[2]))
            bottomright_y.append(float(i[5]) + float(i[3]))
            center_x.append(float(i[2])+float(i[4])/2)
            center_y.append(float(i[3])+float(i[5])/2)
            temp_box_x = float(i[4])
            temp_box_y = float(i[5])
            box_x.append(temp_box_x)
            box_y.append(temp_box_y)
            box_min.append(min(temp_box_x,temp_box_y))
    a,_ = optimization.curve_fit(func,center_x,real_angle)
    b,_ = optimization.curve_fit(func,box_x,real_dist)
    b2,_ = optimization.curve_fit(func1,box_x,real_dist)
    print(a[0],a[1])
    print(b[0],b[1])
    print(b2[0],b2[1],b2[2])
    result = []
    '''
    for i in box_x:
        result.append(func(i,b[0],b[1]))
    '''
    for i in box_x:
        result.append(func1(i,b2[0],b2[1],b2[2]))
    #plt.plot(center_y, center_x,real_dist, 'ro')
    plt.xlabel("box_x_size")
    plt.ylabel('distance')
    #plt.xlabel("center_x_axis")
    #plt.ylabel('angle')
    plt.plot(box_x, real_dist, 'ro')
    plt.plot(box_x, result, 'bo')
    plt.show()
    #optimization.curve_fit(func1, img_dist,img_angle,bot_w,bot_h,real_dist)

main()
