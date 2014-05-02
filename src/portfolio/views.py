from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import messages

from .models import Stock 
from .forms import AddShareForm
from .ystockquote import get_price

import MySQLdb
import numpy 
import math
import datetime
import random
import operator as op

import time
import datetime
from scipy.stats import norm
from sklearn.svm import SVR, SVC, LinearSVC
from chartit import DataPool, Chart

# Create your views here.

def home(request):
    return render_to_response("signup.html", locals(), context_instance = RequestContext(request))

def thankyou(request):
    return render_to_response("thankyou.html", locals(), context_instance = RequestContext(request))

def userpage(request):
    #Send data as Dictionary
    if request.user.is_authenticated():
        u = request.user
    lis = u.stock_set.all().order_by('stock_name')
    r = right_side(u)
    dicy = []
    dic = []
    dicy.append(lis)
    dicy.append(dic)
    dicy.append(r)
    print 'Normal UserPage', dicy
    #Calculate for each stock of his portfolio
    return render_to_response('userpage.html', {'dicy': dicy}, context_instance=RequestContext(request))

def graph(request):
    if request.user.is_authenticated():
        u = request.user
    context = RequestContext(request)
    lis = u.stock_set.all().order_by('stock_name')
    dicy=lis
    return render_to_response('graph.html', {'dicy': dicy}, context_instance=RequestContext(request))    

def aboutus(request):
    return render_to_response("aboutus.html", locals(), context_instance = RequestContext(request))

def portfolio(request):
    
    if request.user.is_authenticated():
    # Do something for logged-in users.
        u = request.user
        dic = u.stock_set.all()
    else:
    # Do something for anonymous users.
        dic = {}
    return render_to_response('portfolio.html', {'dic': dic}, context_instance=RequestContext(request))

def suggestion(request):
    context = RequestContext(request)
    search_text = ''
    print search_text
    if request.method == 'POST':
        search_text = request.POST['search_text']
        print search_text
    suggs = get_category_list(8, search_text)
    return render_to_response('suggestion.html', {'suggs': suggs }, context)

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Stock.objects.filter(stock_name__istartswith=starts_with)
    else:
        cat_list = Stock.objects.all()

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list

def addtoportfolio(request, user_id, stock_id):
    context = RequestContext(request)
    print 'user_id', user_id
    print 'stock_id', stock_id
    s = Stock.objects.get(id=stock_id)
    u = User.objects.get(id=user_id)
    s.users.add(u)
    r = right_side(u)
    print '%s Added to Portfolio' % s.stock_name
    dic = u.stock_set.all().order_by('stock_name')
    print dic
    d = []
    dicy = []
    dicy.append(dic)
    dicy.append(d)
    dicy.append(r)
    messages.success(request, 'Success! %s added to your portfolio' % s.stock_name)
    return render_to_response('userpage.html', {'dicy': dicy}, context)

def removefromportfolio(request, user_id, stock_id):
    context = RequestContext(request)
    print 'user_id', user_id
    print 'stock_id', stock_id
    s = Stock.objects.get(id=stock_id)
    u = User.objects.get(id=user_id)
    u.stock_set.remove(s)
    r = right_side(u)
    print '%s Removed from Portfolio' % s.stock_name
    dic = u.stock_set.all().order_by('stock_name')
    d = []
    dicy = []
    dicy.append(dic)
    dicy.append(d)
    dicy.append(r)
    messages.success(request, 'Success! %s removed from your portfolio' % s.stock_name)
    return render_to_response('userpage.html', {'dicy': dicy}, context)

def predict(request, stock_id, period):
    context = RequestContext(request)
    period = int(period)
    s = Stock.objects.get(id=stock_id).stock_tickr.encode('utf-8')
    s_name = Stock.objects.get(id=stock_id).stock_name.encode('utf-8')
    dic = []
    dic.append(s_name)
    if period == 2:
        dic.append(bayesian(s))
        dic.append('Short Term Prediction is ')
    else:
        dic.append(svm(s))
        dic.append('Long Term Prediction is ')
    u = request.user
    lis = u.stock_set.all()
    r = right_side(u)
    dicy = []
    dicy.append(lis)
    dicy.append(dic)
    dicy.append(r)
    return render_to_response('userpage.html', {'dicy': dicy}, context)

def get_data(stock_tickr):
    db = MySQLdb.connect(host = "localhost",user="root", passwd="4991", db= "SW")
    cur = db.cursor()
    cur.execute("SELECT Close, Date FROM ORGANIZATION_STOCK_DATA WHERE STOCK_ID='%s' ORDER BY Date" % (stock_tickr,))
    results = cur.fetchall()
    return results

def bayesian(stock_tickr):
    data = get_data(stock_tickr)
    x_10 =[]
    t_data = []
    for i in xrange(len(data) - 10, len(data)):
        t_data.append(data[i][0])
    for i in xrange(1, 11):
        x_10.append(i)
    t=[]
    t.append(t_data)
    t_data = t
    N = 10
    M = 6

    rel_err_dr=0

    x=x_10[len(x_10) - 1] + 1

    for k in range(1):
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
    mean = round(mean, 3)
    per = round(per, 3)
    final.append(mean)
    final.append(per)
    return final

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

    a = numpy.array(a)

    w=[]
    for i in b:
        l=[]
        l.append(i)
        w.append(l)

    b=numpy.array(w)
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
    return final

def current(request, stock_id):

    context = RequestContext(request)
    u = request.user
    r = right_side(u)
    lis = u.stock_set.all()
    s = Stock.objects.get(id=stock_id).stock_tickr.encode('utf-8')
    s_name = Stock.objects.get(id=stock_id).stock_name.encode('utf-8')
    dic = float(get_price(s))
    d = []
    d.append(s_name)
    d.append(dic)
    dicy = []
    dicy.append(lis)
    dicy.append(d)
    dicy.append(r)
    return render_to_response('userpage.html', {'dicy': dicy}, context)

def history(request, stock_id):
    context = RequestContext(request)
    u = request.user
    lis = u.stock_set.all()
    s = Stock.objects.get(id=stock_id).stock_tickr.encode('utf-8')
    s_name = Stock.objects.get(id=stock_id).stock_name.encode('utf-8')
    data = get_historical_data(s) #tuple
    dicy = []
    dicy.append(data)
    dicy.append(s_name)
    #data.append(d)
    return render_to_response('historicaldata.html', {'dicy': dicy}, context)


def get_historical_data(stock_tickr):
    db = MySQLdb.connect(host = "localhost",user="root", passwd="4991", db= "SW")
    cur = db.cursor()
    cur.execute("SELECT * FROM ORGANIZATION_STOCK_DATA WHERE STOCK_ID='%s' ORDER BY Date" % (stock_tickr,))
    results = cur.fetchall()
    return results

def plot(request, stock_id, time_p):
    context = RequestContext(request)
    start_time = int(time.mktime(datetime.datetime(2011, 1, 1).timetuple()) * 1000)
    s = Stock.objects.get(id=stock_id).stock_tickr.encode('utf-8')
    s_name = Stock.objects.get(id=stock_id).stock_name.encode('utf-8')
    y = get_plot_data(s, time_p)
    xdata = []
    ydata = []
    for i in xrange(len(y)):
        xdata.append(y[i][1])
        ydata.append(y[i][0])
    zipped = zip(xdata, ydata)
    create_js(zipped)
    return render_to_response('Zooming.html',{'s':s_name},context)

def get_plot_data(stock_tickr, timeperiod):
    db = MySQLdb.connect(host = "localhost",user="root", passwd="4991", db= "SW")
    cur = db.cursor()
    #cur.execute("SELECT Close, Date FROM ORGANIZATION_STOCK_DATA WHERE  DATE > DATE_SUB( '2013-12-31', INTERVAL %s DAY ) AND STOCK_ID='%s' ORDER BY Date" % (timeperiod,stock_tickr))
    cur.execute("SELECT Close, Date FROM ORGANIZATION_STOCK_DATA WHERE STOCK_ID = '%s' ORDER BY Date" % (stock_tickr,))
    #print "SELECT Close, Date FROM ORGANIZATION_STOCK_DATA WHERE STOCK_ID = '%s' ORDER BY Date" % (stock_tickr,)
    results = cur.fetchall()
    #print results
    return results

def create_js(data):

    f = open('/home/khpatel4991/Documents/sharehoroscope/static/static/js/zoomingData.js', 'w')
    f.write('zoomingData = [')
    for i in xrange(len(data) - 1):
        f.write('{ arg: new Date(%s, %s, %s), y1: %s},' % (data[i][0].timetuple()[0], data[i][0].timetuple()[1] - 1, data[i][0].timetuple()[2], data[i][1]))
    i = len(data) - 1
    f.write('{ arg: new Date(%s, %s, %s), y1: %s}];' % (data[i][0].timetuple()[0], data[i][0].timetuple()[1] - 1, data[i][0].timetuple()[2], data[len(data) - 1][1]))

def right_side(u):
    lis = u.stock_set.all()
    a = {}
    for i in xrange(lis.count()):
        a[lis[i].stock_name.encode('utf-8')] = (bayesian(lis[i].stock_tickr))[1]
    sorted_a = sorted(a.iteritems(), key=op.itemgetter(1))
    a = sorted_a
    final = []
    if(len(a) >= 4):
        final.append(a[len(a) - 1])
        final.append(a[len(a) - 2])
        final.append(a[1])
        final.append(a[0])
        
        
    return final
