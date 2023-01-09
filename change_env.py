import math
import re

path_ = 'hopper.xml'


def change(path, name, new_v):
    with open(path, 'r') as file:
        xml = file.read()
        new = re.sub(r'' + name + r'=".*"', name + '="' + new_v + '"', xml)
        file.close()
        with open(path, 'w') as f:
            f.write(new)
            f.flush()
            f.close()


def rang(from_, to, n):
    i = from_
    rang_list = []
    while i <= to:
        rang_list.append(i)
        i += (to - from_) / (n - 1)
    return rang_list



def cal_grav_vector(ang, v):
    x = 0
    y = v * math.sin(math.radians(ang))
    z = v * math.cos(math.radians(ang))
    return str(x) + ' ' + str(y) + ' ' + str(z)


def all_change_run(path: str, name: str, rang_ang: list, rang_v: list):
    for i in rang_ang:
        for j in rang_v:
            vector = cal_grav_vector(i, j)
            change(path, name, vector)
            print(vector)
            # TODO run PGMORL here !! (with different gravity vectors)

            # TODO run PGMORL here !!
            


grav_ang = rang(-5., 5., 3.)  # only in y-z plane
grav_v = rang(-9.81 * 1.1, -9.81 * 0.9, 3.)
all_change_run(path_, 'gravity', grav_ang, grav_v)
