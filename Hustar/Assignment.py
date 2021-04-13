import numpy

#######################################
def check_prime(num):
    for i in range(2, num):
        if (num % i == 0):
            return False
    return True
def problem01():
    a = 13
    b = 15
    if check_prime(a):
        print(str(a) + '는 소수입니다.')
    else:
        print(str(a) + '는 소수가 아닙니다.')
    if check_prime(b):
        print(str(b) + '는 소수입니다.')
    else:
        print(str(b) + '는 소수가 아닙니다.')
########################################


#######################################
def add_comma(val):
    val =  format(val, ',')
    return val

def problem02():
    comma_added_1234 = add_comma(1234)
    comma_added_12345678 = add_comma(12345678)
    comma_added_12 = add_comma(12)
    print(comma_added_1234) # '1,234'
    print(comma_added_12345678) # '12,345,678'
    print(comma_added_12) # '12'
#######################################


#######################################
def tokenize(trg, N=1):
    a = trg.split()
    d = []
    for i in range(len(a) - N + 1):
        b = a[i:i + N]
        c = (' ').join(b)
        d.append(c)
    return d
def problem03():
    a = "There was a farmer who had a dog ."
    print(tokenize(a))
    print(tokenize(a, 2))
#######################################




#######################################
def mean_and_var(*val):
    xlist = []
    ylist = []
    for x,y in val:
        xlist.append(x)
        ylist.append(y)
    xavg = sum(xlist)/len(xlist)
    yavg = sum(ylist)/len(ylist)
    xvar = numpy.var(xlist)
    yvar = numpy.var(ylist)
    xavg = sum(xlist)/len(xlist)
    yavg = sum(ylist)/len(ylist)
    m = xavg, yavg
    var = numpy.var(xlist), numpy.var(ylist)
    return m,var
def problem04():
    v1=(0, 1)
    v2=(0.5, 0.5)
    v3=(1, 0)
    m, var = mean_and_var(v1, v2, v3)
    print('평균: ', m)
    print('분산: ', var)
#######################################
