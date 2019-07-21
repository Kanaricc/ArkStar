import random
from logging import debug,info

normal_offset=0
def generate_normaloffset(offset=None):
    if offset==None:
        normal_offset=rand_normald(0.0,0.15)
    else:
        normal_offset=offset
    info(f"set normal_offset to {normal_offset}")


def rand_normald(l,r):
    opt=random.normalvariate(0.5+normal_offset,(1-0.5-normal_offset)/3)
    while opt<0 or opt>1:
        opt=random.normalvariate(0.5+normal_offset,(1-0.5-normal_offset)/3)
    
    return (l+(r-l)*opt)

def rand_normal(l,r):
    return (int)(rand_normald(l,r))
    

def rand(l,r):
    return random.randint(l,r)

def rand_pos(posl,posr=None,delta=5):
    res=posl
    if posr!=None:
        res[0]=rand_normal(posl[0],posr[0])
        res[1]=rand_normal(posl[1],posr[1])
    else:
        res[0]=rand_normal(posl[0]-delta,posl[0]+delta)
        res[1]=rand_normal(posl[1]+delta,posl[1]+delta)
    return res