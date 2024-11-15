from django.shortcuts import render,redirect
from app.models import user,student,teacher
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')
def studregister(request):
    if request.method=='POST':
        n=request.POST['fname']
        u=request.POST['uname']
        e=request.POST['email']
    
        pw=request.POST['password']
        cw=request.POST['cpassword']
        a=request.POST['age']
        g=request.POST['gender']
        img=request.FILES['image']
        us=user.objects.create_user(first_name=n, email= e,
        username=u,password=pw,usertype='student',approve=0,image=img)
        v =student.objects.create(studid=us,name=n,age=a,email=e,gender=g)
        v.save()
        
        return redirect(logins)
    else:
     return render(request,'studregister.html')


def logouts(request):
    logout(request) 
    return redirect(home)

def adminhome(request):
   return render(request,'adminhome.html')

def studenthome(request):
    return render(request,'studenthome.html')
def teacherhome(request):
   return render(request,'teacherhome.html')
def logins(request):
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['password']
        x=authenticate(request,username=u,password=p)
        if x is not None and x.is_superuser==1:
            login(request,x)
            request.session['id']=x.id
            
            return redirect(adminhome)
        elif x is not None and x.usertype=="student":
            if x.approve==1:
             login(request,x)
             request.session['id']=x.id
             return redirect(studenthome)
            
            else:
               return render(request, 'waiting.html')
            #    return HttpResponse("you cant enter into our website.you are in waiting list...")
        elif x is not None and x.usertype=="teacher":
        
            login(request,x)
            request.session['id']=x.id
            return redirect(teacherhome)
        
        else:
         messages.error(request, 'Invalid username or password.')
            
    
    return render(request,'login.html')


def addteacher(request):
    if request.method=="POST":
        
        n=request.POST['fname']
        u=request.POST['uname']
        e=request.POST['email']
        
        pw=request.POST['password']
        cw=request.POST['cpassword']
        a=request.POST['age']
        g=request.POST['gender']
        d=request.POST['department']
        x = user.objects.create_user(first_name=n, email= e,
        username=u,password=pw,usertype='teacher')
        v = teacher.objects.create(teachid=x,name=n,age=a,email=e,gender=g,department=d )
        v.save()
        
        return redirect(adminhome)
    else:
       return render(request,'addteacher.html')
def adminviewteacher(request):
   x=teacher.objects.all()
   return render(request,'adminviewteacher.html',{'data':x})

def adminviewstudent(request):
   x=student.objects.all()
   return render(request,'adminviewstudent.html',{'data':x})


def approve(request):
   x=student.objects.all()
   u=[i for i in x if not i.studid.approve]
   
   return render(request,'approve.html',{'data':u})
def approved(request,id):
    x=student.objects.get(id=id)#id in student table
    idd=x.studid_id # id in user table
    y=user.objects.get(id=idd)
    y.approve=1
    y.save()
    return redirect(approve)

def reject(request,id):
    x=student.objects.get(id=id)#id in student table
    idd=x.studid_id # id in user table
    y=user.objects.get(id=idd)
    y.delete()
    
    return redirect(approve)



def admindeleteteacher(request,id):
   x=user.objects.get(id=id)
   x.delete()
   return redirect(adminviewteacher)
def admineditteacher(request,id):
   x=teacher.objects.get(id=id)
   return render(request,'admineditteacher.html',{'data':x})

def admineditteacher2(request,id):
    if request.method=='POST':
        n=request.POST['name']
        u=request.POST['uname']
        e=request.POST['email']
        p=request.POST['password']
        d=request.POST['department'] 
        a=request.POST['age']
        
      
        x=teacher.objects.get(id=id)
        x.teachid.first_name=n
        x.teachid.username=u
        x.teachid.email=e
        x.teachid.password=p
        x.teachid.save()
        x.age=a
        x.name=n
        x.email=e
        x.department=d
        
        x.save()
       
        return redirect(adminviewteacher)
    else:
     return HttpResponse("invalid")
    


def admindeletestudent(request,id):
   x=user.objects.get(id=id)
   x.delete()
   return redirect(adminviewstudent)
def admineditstudent(request,id):
   x=student.objects.get(id=id)
   return render(request,'admineditstudent.html',{'data':x})



def admineditstudent2(request,id):
    if request.method=='POST':
        n=request.POST['name']
        u=request.POST['uname']
        e=request.POST['email']
        p=request.POST['password']
        
        a=request.POST['age']
        
      
        x=student.objects.get(id=id)
        x.studid.first_name=n
        x.studid.username=u
        x.studid.email=e
        x.studid.password=p
        x.studid.save()
        x.age=a
        x.name=n
        x.email=e
      
        
        x.save()
       
        return redirect(adminviewstudent)
    else:
     return HttpResponse("invalid")
    

def teachereditprofile(request):
   #username=request.user
   #x=user.objects.get(username=username)
   s=request.session['id']
   na=user.objects.get(id=s)#foreign key
   y=teacher.objects.get(teachid=na)
   #return HttpResponse(y)

 
   return render(request,'teachereditprofile.html',{'data1':na,'data2':y})
    

def teachereditprofile2(request,id):
    if request.method=='POST':
        n=request.POST['name']
        u=request.POST['uname']
        e=request.POST['email']
        p=request.POST['password']
        d=request.POST['department']
        a=request.POST['age']
        x=teacher.objects.get(id=id)
        x.teachid.first_name=n
        x.teachid.username=u
        x.teachid.email=e
        x.teachid.password=p
        x.teachid.save()
        x.age=a
        x.name=n
        x.email=e
        x.department=d
        x.save()
        return redirect(teacherhome)
    else:
     return HttpResponse("invalid")

def teacherviewstudent(request):
   x=student.objects.all()
   return render(request,'teacherviewstudent.html',{'data':x})


def studenteditprofile(request):
   #username=request.user
   #x=user.objects.get(username=username)
   s=request.session['id']
   na=user.objects.get(id=s)#foreign key
   y=student.objects.get(studid=na)
   #return HttpResponse(y)

 
   return render(request,'studenteditprofile.html',{'data1':na,'data2':y})



def studenteditprofile2(request,id):
    if request.method=='POST':
        n=request.POST['name']
        u=request.POST['uname']
        e=request.POST['email']
        p=request.POST['password']
        a=request.POST['age']
        x=student.objects.get(id=id)
        x.studid.first_name=n
        x.studid.username=u
        x.studid.email=e
        x.studid.password=p
        x.studid.save()
        x.age=a
        x.name=n
        x.email=e
        x.save()
        return redirect(studenthome)
    else:
     return HttpResponse("invalid")


def studentviewteacher(request):
   x=teacher.objects.all()
   return render(request,'studentviewteacher.html',{'data':x})



def deleteall(request):
   x=user.objects.all()
   x.delete()
   return HttpResponse("deleted")

