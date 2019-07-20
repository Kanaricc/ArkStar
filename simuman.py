import random

def rand_normal(l,r):
    opt=random.normalvariate(0.5,0.5/3)
    while opt<0 or opt>1:
        opt=random.normalvariate(0.5,0.5/3)
    
    return (int)(l+(r-l)*opt)

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