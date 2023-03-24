import csv 
import itertools 
import math 
import random as ran 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as pat 
from matplotlib import animation, colors 
 

 
def main():
    data=30 
    result=[0]*data
    for z in range(data): 
        # 個数 
        num=20 
 
        x=[250+num*math.cos(math.radians((360/num)*i))for i in range(num)] 
        y=[250+num*math.cos(math.radians((360/num)*i))for i in range(num)] 
 
        velAngle= [(360/num)*i for i in range(num)] 
        vel=[ran.uniform(0, 3.5)for i in range(num)] 
 
        dx= [vel[i]*math.cos(math.radians(velAngle[i]))for i in range(num)] 
        dy= [vel[i]*math.sin(math.radians(velAngle[i]))for i in range(num)] 
 
        # リーダー 
        # ベクトル 
        dx[0]=3 
        dy[0]=5 
 
        kX=([0]*num) 
        kY=([0]*num) 
        test=500 
        # 描画領域 
        fig = plt.figure(figsize=(6, 6)) 
        plt.xlim([0, 500]), plt.ylim([0, 500]) 
        flag=0 
 
        ims=[] 
        for c in range(test): 
            # (結合)群れの中心に移動しようとする 
            #重心 
            aveX=sum(x)/num 
            aveY=sum(y)/num 
            # 各頂点と重心のきょり 
            ctrDirX=[aveX-x[i]for i in range(num)] 
            ctrDirY=[aveY-y[i]for i in range(num)] 
 
            # （整列）群れ全体の速度ベクトルに合わせるようにする 
            # (Vel)ベクトルの平均距離 
            # (Angle)なす角の平均 
            aveVel=sum(math.sqrt(dx[i]**2 + dy[i]**2)for i in range(num))/num 
            aveAngle=sum(math.degrees(math.atan2(dy[i],dx[i]))for i in range(num))/num 
            velX=aveVel*math.cos(math.radians(aveAngle)) 
            velY=aveVel*math.sin(math.radians(aveAngle)) 
 
            count=[0]*num 
            for i in range(1,num): 
                dis=math.sqrt((x[0]-x[i])**2+(y[0]-y[i])**2) 
                if dis<=50: 
                    count[i]=1 
            # リーダー 
            if c<=200: 
                x[0] += dx[0] 
                y[0] += dy[0] 
            else : 
                cc=0 
                count[0]=1 
                for i in range(num): 
                    if count[i]==1: 
                        cc+=1 
                if cc==num and flag==0: 
                    flag=1 
                    print("ステップ数:",end="") 
                    print(c) 
                    result[z]=c 
            # リーダー以外 
            # 二重ループ 
            for i in range(1, num): 
                if count[i]!=1: 
                    contX=([0]*num) 
                    contY=([0]*num) 
                    for j in range(i+1, num): 
                            dist=math.sqrt((x[j]-x[i])**2 + (y[j]-y[i])**2) 
                            # (分離) 
                            if 0<dist<15: 
                                contX[i]=(-1*(x[j]-x[i])) 
                                contY[i]=(-1*(y[j]-y[i])) 
                                t=float(math.sqrt(contX[i]**2 + contY[i]**2)) 
                                contX[i]/=t 
                                contY[i]/=t 
 
            for i in range(1, num): 
                if count[i]!=1: 
                    # パラメーター設定 
                    kX[i]=(1*ctrDirX[i]+1*velX+1.5*contX[i]) 
                    kY[i]=(1*ctrDirY[i]+1*velY+1.5*contY[i]) 
                    tVel=math.sqrt(kX[i]**2+kY[i]**2) 
                    if(tVel>2): 
                        kX[i]=2*kX[i]/tVel 
                        kY[i]=2*kY[i]/tVel 
                        dx[i] += (kX[i]-dx[i])*0.022
                        dy[i] += (kY[i]-dy[i])*0.022
                        x[i] += 0.15*c*dx[i] 
                        y[i] += 0.15*c*dy[i] 
 
            for i in range(num): 
                if count[i]!=1: 
                    if x[i] >= 500 or x[i] <= 0: 
                        dx[i] = -dx[i] 
                    if y[i] >= 500 or y[i] <= 0: 
                        dy[i]= -dy[i] 
            
            tmp1 = plt.scatter(x[1:], y[1:],c="black")
            tmp2 = plt.scatter(x[0], y[0],c="red") 
            ims.append([tmp1,tmp2]) 
            """
            im = plt.scatter(x, y,c="black")
            ims.append([im])
            """
        ani = animation.ArtistAnimation(fig, ims, interval=100, repeat_delay=100) 
        ani.save("./kenken/image"+str(z+1)+".gif",writer="pillow") 
        csv_file=open("./kenken/result"+str(z+1)+".csv","w",newline="") 
        writer=csv.writer(csv_file) 
        writer.writerow(["ループ数",str(result[z])+"回"]) 
    csv_file=open("./kenken/result.csv","w",newline="") 
    writer=csv.writer(csv_file) 
    writer.writerow(["num","ループ数"]) 
    for i in range(data): 
        writer.writerow([i+1,str(result[i])+"回"]) 
if __name__ == '__main__': 
    main()