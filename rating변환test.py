import math
import matplotlib.pyplot as plt
score = {"1":1.0,"2":1.4,"3":1.8,"4":2.0,"5":2.4,"6":2.8,"7":3.2,"8":3.6,"9":4.0,"10":4.4,"11":4.8,"12":5.2,"13":5.6,"14":6.0,"15":6.4,"16":6.8,"17":7.2,"18":7.6,"19":8.0,"20":8.4,"21":8.8,"22":9.2,"23":9.6,"24":10.0,"25":10.4,"26":10.8,"27":11.2,"28":11.6,"29":12.0,"30":12.4,"31":12.8,"32":13.2,"33":13.6,"34":14.0,"35":14.4,"36":14.8,"37":15.2,"38":15.6,"39":16.0,"40":16.4,"41":16.8}
def r_cal(r):
    if r >= 2400:
        return int(800*math.log((r-1600)/800) + 2400)
    elif 400 <= r and r < 2400:
        return r
    else:
        return int(max(1,400/math.exp((400-r)/400)))
    
# print(r_cal(3000))

# x = 1800
# print(1/(1+math.pow(10,x/400)))

def rating_check(a, time_seconds):
    sum = a
    cur = (500+100*sum)*((15000)/(10000+time_seconds))
    global ans
    ans = 0
    
    print(r_cal(cur))
    return r_cal(cur)

print(rating_check(4.4,1000))
# x = []
# y = []
# for i in range(1,3600):
#     x.append(i)
# for i in x:
#     y.append(rating_check(5,i))

# plt.title("10분안에 푼 경우 랜디 점수 변화")
# plt.plot(x,y,'o')
# plt.show()



# print(rating_check(a,30))