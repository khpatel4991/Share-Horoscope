import MySQLdb
import numpy 
import math
import datetime
import time

def get_data(stock_tickr):
	db = MySQLdb.connect(host = "localhost",user="root", passwd="4991", db= "SW")
	cur = db.cursor()
	cur.execute("SELECT Close, Date FROM ORGANIZATION_STOCK_DATA WHERE STOCK_ID='%s'" % (stock_tickr,))
	results = cur.fetchall()
	return results

def bayesian(stock_tickr):	
    data = get_data(stock_tickr)
	#data[0] Price
	#data[1] Time
    x_10 =[]
    t_data = []
    for i in xrange(len(data) - 10, len(data)):
        #x_10.append(time.mktime(data[i][1].timetuple()))
        #x_10.append((i - 242) * 86400)
        #x_10[i] - x_10[0]
        x_10.append(i - 241)
        t_data.append(data[i][0])
    t=[]
    t.append(t_data)
    t_data = t

#t_data = [1196.32, 1197.04, 1196.99, 1195.8, 1193.58, 1197.75, 1196.16, 1195.37, 1195.1, 1194.86]
#input data set
#t_data=[[1196.32, 1197.04, 1196.99, 1195.8, 1193.58, 1197.75, 1196.16, 1195.37, 1195.1, 1194.86]]
# actual value that we are trying to predict[]

#t_actual=[1193.54]
    #t_data=stockvalues
    # initiating variable for our calculation purpose
    N = 10
    M = 6

    rel_err_dr=0

    #for i in range(len(t_actual)):
     #   rel_err_dr=rel_err_dr+t_actual[i]
        
    x=x_10[len(x_10) - 1] + 1

    for k in range(1):
        
    # creating empty arrays/matrices

        t = numpy.zeros((N,1),float)
        phi = numpy.zeros((M,1),float)
        phi_sum = numpy.zeros((M,1),float)
        phi_sum_t = numpy.zeros((M,1),float)

        for i in range(M):
            phi[i][0]=math.pow(x,i)

        for i in range(N):
           t[i][0]=t_data[k][i]
            
        for j in range(N):
            for i in range(M):
                phi_sum[i][0]=phi_sum[i][0]+math.pow(x_10[j],i)
                phi_sum_t[i][0]=phi_sum_t[i][0]+t[j][0]*math.pow(x_10[j],i)

    # Calculation of variance / standard deviation
        S=numpy.linalg.inv(0.005*numpy.identity(M)+11.1*numpy.dot(phi_sum,phi.T))

        var=numpy.dot((phi.T),numpy.dot(S,phi))
        var=var+1/11.1

    # Calculating the mean
        mean=11.1*numpy.dot(phi.T,numpy.dot(S,phi_sum_t))
       #error_n=0
        #error_n=error_n+math.fabs(t_actual[k]-mean)

        #abs_error=0
        #abs_error = abs_error + error_n
        mean = mean[0][0]
        print 'mean', mean

    t = t_data[0]
    t_data = t
    sum = 0
    avg = 0
    for i in t_data:
        sum += i
    mov = sum / len(t_data)
    print 'mov', mov
    per = ((mean - mov) / mov) * 100
    print 'per', per
    final = []
    final.append(mean)
    final.append(per)
    print final
    return final
