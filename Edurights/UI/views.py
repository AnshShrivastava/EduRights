from django.shortcuts import render,redirect
from .models import *
from rest_framework import views
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse


# Create your views here.

def home(request):
    data = Vlogs.objects.all()
    reviews = Review.objects.all()[:9]
    return render(request,'index.html',{'info': data, 'review': reviews})

def test(request):
    data = Vlogs.objects.all()

    return render(request,'home.html',{'info': data})

def leads(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        collegeemail = request.POST["collegeemail"]
        collegename = request.POST["collegename"]
        request = request.POST["request"]        
        lead = Leads(name=name,college=collegename,email=email,college_email=collegeemail,request=request)
        lead.save()
        status = "true"
        return redirect('thank')
    else:
        status = "false"
        return render(request,'contact-us.html', {'status': status})

def institutes(request):
    data = College.objects.all()
    return render(request,'institutes.html',{'info': data})

def vloggers(request):
    data = Vlogger.objects.all() 
    ad = Advertisement.objects.all()
    return render(request,'vloggers.html',{'info': data, 'ad': ad})
                  
def vloglist(request):
    data = Vlogs.objects.all() #SELECT * FROM VLOGS;

    return render(request,'vlogslist.html',{'info': data})

def newrequest(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        collegename = request.POST["collegename"]
        requests = request.POST['requests']
        filenew = request.FILES['filenew']
        fs = FileSystemStorage()
        filename = fs.save(filenew.name, filenew) 
        req = Requests(name=name,college=collegename,email=email,file=fs.url(filename),request=requests)
        req.save()
    return redirect('thank')


def about_us(request):
    ad = Advertisement.objects.all()
    return render(request,'about-us.html', {'ad': ad})

def vlogs(request):
    vlog_id = request.GET.get('vlog_id')
    v = Vlogs.objects.get(id=vlog_id)
    url = v.video
    url.replace("http:", "https:")
    ad = Advertisement.objects.all()
    return render(request,'postview.html',{'data':v, 'videourl': url, 'ad': ad})

def layout(request):
    return render(request,'layouts.html')

def college(request):
    college_id = request.GET.get('id')
    vlog = Vlogs.objects.filter(college_id=college_id) #SELECT * FROM VLOGS WHERE college_id = '12345';
    college = College.objects.get(id=college_id)
    ad = Advertisement.objects.all()
    return render(request,'college-layout.html',{'college':college, 'vlogs': vlog, 'ad': ad})

def thank(request):
    ad = Advertisement.objects.all()
    return render(request, 'thank.html', {'ad': ad})
 
 
def addreview(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        collegeemail = request.POST["collegeemail"]
        collegename = request.POST["collegename"]
        request = request.POST["request"]        
        lead = Leads(name=name,college=collegename,email=email,college_email=collegeemail,request=request)
        lead.save()
        status = "true"
        return redirect('thank')
    else:
        status = "false"
        return render(request,'add-review.html', {'status': status})
    
       
# class search(views.APIView):
#     model = Vlogs,Vlogger,College
#     serializer = VlogSerializer,VloggerSerializer,CollegeSerializer

#     def get(self,request):
#         srch = request.GET['search']
#         data1 = Vlogs.objects.filter(college_id__collegename__icontains=srch)
#         data2 = Vlogs.objects.filter(title__icontains=srch)
#         data = (data1 | data2).distinct()
#         return render(request,'searchresult.html', {'vlogs': data, 'query' : srch} )