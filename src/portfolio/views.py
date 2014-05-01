from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import messages

from .models import Stock 
from .forms import AddShareForm
#from .prediction import bayesian, svm

# Create your views here.

def home(request):
    return render_to_response("signup.html", locals(), context_instance = RequestContext(request))

def thankyou(request):
    print "Inside Thank You"
    return render_to_response("thankyou.html", locals(), context_instance = RequestContext(request))

def userpage(request):
    #Send data as Dictionary
    if request.user.is_authenticated():
        u = request.user
    dic = u.stock_set.all().order_by('stock_name')
    print dic
    #Calculate for each stock of his portfolio
    return render_to_response('userpage.html', {'dic': dic}, context_instance=RequestContext(request))

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
    print '%s Added to Portfolio' % s.stock_name
    dic = u.stock_set.all().order_by('stock_name')
    messages.success(request, 'Success! %s added to your portfolio' % s.stock_name)
    return render_to_response('portfolio.html', {'dic': dic}, context)

def removefromportfolio(request, user_id, stock_id):
    context = RequestContext(request)
    print 'user_id', user_id
    print 'stock_id', stock_id
    s = Stock.objects.get(id=stock_id)
    u = User.objects.get(id=user_id)
    u.stock_set.remove(s)
    print '%s Removed from Portfolio' % s.stock_name
    dic = u.stock_set.all().order_by('stock_name')
    messages.success(request, 'Success! %s removed from your portfolio' % s.stock_name)
    return render_to_response('portfolio.html', {'dic': dic}, context)

def predict(request, stock_id, period):
    context = RequestContext(request)
    print 'stock_id', stock_id
    s = Stock.objects.get(id=stock_id).stock_tickr.encode('utf-8')
    '''
    if period == 1 or 2:
        
    else:
        svm(s)
    '''
    return render_to_response('userpage.html', {'dic': dic}, context)

