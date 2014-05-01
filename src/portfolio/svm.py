import numpy as np
from scipy.stats import norm
from sklearn.svm import SVR, SVC, LinearSVC
import MySQLdb
import numpy 
import math
import datetime
import time

def get_data(stock_tickr):
    db = MySQLdb.connect(host = "localhost",user="root", passwd="4991", db= "SW")
    cur = db.cursor()
    cur.execute("SELECT Close, Date FROM ORGANIZATION_STOCK_DATA WHERE STOCK_ID='%s'" % (stock_tickr,))
    print "SELECT Close, Date FROM ORGANIZATION_STOCK_DATA WHERE STOCK_ID='%s'" % ( stock_tickr,)
    results = cur.fetchall()
    return results
def svm(stock_tickr):
    data = get_data(stock_tickr)
    a = []
    b = []
    for i in xrange(len(data)):
        #x_10.append(time.mktime(data[i][1].timetuple()))
        #x_10.append((i - 242) * 86400)
        #x_10[i] - x_10[0]
        b.append(i + 1)
        a.append(data[i][0])

    a = np.array(a)

    w=[]
    for i in b:
    	l=[]
    	l.append(i)
    	w.append(l)

    b=np.array(w)
    print a[len(a) - 1]
    clf = SVC(kernel='linear', degree=1)
    print clf.fit(b, a)
    mean = clf.predict(len(a) - 1);
    sum = 0
    avg = 0
    for i in xrange(len(a) - 200, len(a)):
        sum += a[i]
    mov = sum / 200
    print 'mov', mov
    per = ((mean - mov) / mov) * 100
    print 'per', per[0]
    final = []
    final.append(mean[0])
    final.append(per[0])
    print final
    return final

svm('GOOGL')

