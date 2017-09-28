# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:27:24 2017

@author: mw352
"""

import random
import numpy as np

interval = np.loadtxt("D:\\tandon\\AI_for_game\\osu_project\\dataset\\interval.csv",delimiter=",",skiprows=0)


def check(p):
    if p[0] > 512 or p[0] < 0 or p[1] > 384 or p[1] < 0:
        return random_point()
    else:
        return p
    
def check_yn(p):
    if p[0] > 512 or p[0] < 0 or p[1] > 384 or p[1] < 0:
        return 0
    else:
        return 1

def pos_neg():
    obj = random.randint(0, 1)
    if obj == 0:
        return -1
    else:
        return 1

def random_next(p, level):
    nex = []
    if level == 1:
        offset1 = random.randint(30, 30)
        offset2 = random.randint(30, 30)
        nex = [p[0] + pos_neg() * offset1, p[1] + pos_neg() * offset2]
    elif level == 2:
        offset1 = random.randint(50, 60)
        offset2 = random.randint(50, 60)
        nex = [p[0] + pos_neg() * offset1, p[1] + pos_neg() * offset2]
    elif level == 3 or level == 4:
        offset1 = random.randint(60, 120)
        offset2 = random.randint(60, 120)
        nex = [p[0] + pos_neg() * offset1, p[1] + pos_neg() * offset2]
    elif level >=5 and level <= 8:
        offset1 = random.randint(100, 160)
        offset2 = random.randint(100, 160)
        nex = [p[0] + pos_neg() * offset1, p[1] + pos_neg() * offset2]
    else:
        nex = random_point()
        '''
    if check_yn(nex) == 0:
        return random_next(p, level)
    else:
        print('random_next:')
        print(nex)
        return nex;
        '''
    return check(nex)

def ad_hoc_possibility(t, pre, pre2):
    possibility = random.randint(0, 100)
    if possibility >= 0 and possibility < 10:
        return random_sym_point(pre, [256, 192])
    elif possibility >= 10 and possibility < 20:
        return random_sym_flat(pre, [0, 192])
    elif possibility >= 20 and possibility < 30:
        return random_sym_flat(pre, [256, 0])
    elif possibility >= 30 and possibility < 40:
        return random_repeat(pre)
    elif possibility >= 40 and possibility < 50:
        return random_repeat(pre)
    elif possibility >= 50 and possibility < 75:
        return consequent(pre, pre2)
    elif possibility >= 75 and possibility <= 100:
        return random_next(pre, t)
    
    
def generate_map_coordinate(a):
    map_c = []
    map_c.append(random_point())
    map_c.append(random_point())
    map_c.append(random_point())
    print(len(a))
    for i in range(3, len(a)):
        print('i - 1:')
        print(map_c[i - 1])
        next_p = ad_hoc_possibility(a[i], map_c[i-1], map_c[i-2])
        map_c.append(next_p)
        print('i:')
        print(map_c[i])
    return map_c
    
    
    

def random_point():
    x = random.randint(0, 512)
    y = random.randint(0, 384)
    return [x, y]

def random_sym_point(p, center):
    #print(p)
    x1 = p[0]
    x2 = p[1]
    y1 = center[0]
    y2 = center[1]
    sym1 = 2 * y1 - x1
    sym2 = 2 * y2 - x2
    sym = [sym1, sym2]
    print('random_sym_point:')
    print(check(sym))
    return check(sym)

def random_sym_flat(p, flat):
    #print(p)
    x1 = p[0]
    x2 = p[1]
    y1 = flat[0]
    y2 = flat[1]
    if y1 == 0:
        sym2 = 2 * y2 - x2
        print('random_sym_flat:')
        print(check([x1, sym2]))
        return check([x1, sym2])
    else:
        sym1 = 2 * y1 - x1
        print('random_sym_flat:')
        print(check([sym1, x2]))
        return check([sym1, x2])
    
def random_repeat(p):
    #print(p)
    x1 = p[0]
    x2 = p[1]
    offset1 = random.randint(-10, 10) 
    offset2 = random.randint(-10, 10) 
    print('random_repeat:')
    print(check([x1+offset1, x2+offset2]))
    return check([x1+offset1, x2+offset2])

def consequent(p1, p2):
    #print(p1)
    x1 = p1[0]
    x2 = p1[1]
    y1 = p2[0]
    y2 = p2[1]
    p = [x1+x1-y1, x2+x2-y2]
    print('consequent:')
    print(check(p))
    return check(p)


map_coordinate = generate_map_coordinate(interval)
print(len(map_coordinate))
np.savetxt('D:\\tandon\\AI_for_game\\osu_project\\dataset\\interval_coordinate.csv', map_coordinate, delimiter = ',')