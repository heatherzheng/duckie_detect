import numpy as np
import scipy.optimize as optimization
import matplotlib.pyplot as plt

def func(x, a, b):
    return a + b*x

def func1(x, a, b, c, d, f):
    return a + b*x + c*x + d*x + f*x

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
    with open("../data/data.txt") as f:
        content = f.readlines()
        for i in content:
            i = i.strip("\n")
            i = i.split()
            real_angle.append(int(i[0]))
            real_dist.append(int(i[1]))
            upperleft_x.append(int(i[2]))
            upperleft_y.append(int(i[3]))
            bottomright_x.append(int(i[4]))
            bottomright_y .append(int(i[5]))
            center_x.append((int(i[2])+int(i[4]))/2)
            center_y.append((int(i[3])+int(i[5]))/2)
            temp_box_x = int(i[4])-int(i[2])
            if(temp_box_x<5):
                print(str(i))
            temp_box_y = int(i[5])-int(i[3])
            box_x.append(temp_box_x)
            box_y.append(temp_box_y)
            box_min.append(min(temp_box_x,temp_box_y))
    a,_ = optimization.curve_fit(func,center_x,real_angle)
    b,_ = optimization.curve_fit(func,box_x,real_dist)
    print(a[0],a[1])
    print(b[0],b[1])
    result = []
    for i in center_x:
        result.append(func(i,a[0],a[1]))

    #plt.plot(center_y, center_x,real_dist, 'ro')
    #plt.xlabel("box_x_size")
    #plt.ylabel('distance')
    plt.xlabel("center_x_axis")
    plt.ylabel('angle')
    plt.plot(center_x, real_angle, 'ro')
    plt.plot(center_x, result, 'bo')
    plt.show()
    #optimization.curve_fit(func1, img_dist,img_angle,bot_w,bot_h,real_dist)

main()
