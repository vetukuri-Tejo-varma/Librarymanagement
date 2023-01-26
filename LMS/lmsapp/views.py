from django.shortcuts import render

# Create your views here.
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from lmsapp.models import Course, Book, Issue_book, Student


def login_fun(request):
    return render(request,"login.html",{'data':''})
def logread_fun(request):
    username=request.POST['txtname']
    password=request.POST['txtpassword']
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        if user.is_superuser:
            auth.login(request,user)
            request.session["student_name"] = user.username
            return redirect("admin_home")
        else:
            return render(request,"login.html", {'data': 'Invalid user name and password'})
    else:
        s1 = Student.objects.filter(Q(student_name=username) & Q(student_password=password)).exists()
        if s1:
            n1=request.session['Name'] = username
            print(n1)
            return render(request,"student_home.html",{'dict':n1})
        else:
                return render(request,'login.html',{'data':'Invalid username and password'})
def admin_signup(request):
        if request.method=="POST":
            user_name=request.POST['txtuser']
            user_password = request.POST['txtpswd']
            user_email = request.POST['txtmail']
            if User.objects.filter(Q(username=user_name) | Q(email=user_email)).exists():
                return render(request, "register.html", {'data': 'Username and email is already exists'})
            else:
                user = User.objects.create_superuser(username=user_name, email=user_email, password=user_password)
                user.save()
                return redirect('login')
        return render(request, "admin_signup.html")
def student_reg(request):
    course=Course.objects.all()
    s1=Student()
    if request.method=="POST":
        s1.student_name=request.POST['txtname']
        s1.student_phone = request.POST['txtphone']
        s1.student_semester = request.POST['txtsem']
        s1.student_password = request.POST['txtpswd']
        s1.student_course = Course.objects.get(course_name=request.POST['ddlcourse'])
        if Student.objects.filter(Q(student_name=s1.student_name) & Q(student_password=s1.student_password)).exists():
            return render(request, "student_signup.html",
                          {'data': 'Student name and student password is already exists'})
        s1.save()
        return redirect('login')
    return render(request, "student_signup.html", {'Course_Data': course})
def admin_home(request):
    n1 = request.session.get('student_name')
    return render(request,"admin_home.html",{'data':n1})
def student_home(request):
    n2 = request.session.get('Name')
    return render(request,"student_home.html",{'dict':n2})
def add_book(request):
    course=Course.objects.all()
    if request.method=="POST":
        b1=Book()
        b1.book_name=request.POST['txtbook']
        b1.author_name=request.POST['txtauthor']
        b1.course_id=Course.objects.get(course_name=request.POST['ddlcourse'])
        b1.save()
        return redirect("addbook")
    return render(request,"add_books.html",{'Course_Data':course})
def display_book(request):
    b1=Book.objects.all()
    return render(request,"display_books.html",{'data':b1})
def update_book(request, id):
        b1 = Book.objects.get(id=id)
        course = Course.objects.all()
        if request.method == 'POST':
            b1.Book_Name = request.POST['txtbook']
            b1.Author_Name = request.POST['txtauthor']
            b1.Course_ID = Course.objects.get(course_name=request.POST['ddlcourse'])
            b1.save()
            return redirect('display_book')
        return render(request, 'update_books.html', {'data': b1, 'Course_Data': course})

def delete_book(request,id):
    b1=Book.objects.get(id=id)
    b1.delete()
    return redirect("display_book")

def display_stud(request):
    s1=Student.objects.all()
    return render(request,"display_students.html",{'data':s1})

def update_stud(request,id):
    s1=Student.objects.get(id=id)
    course=Course.objects.all()
    if request.method=="POST":
        s1.Stud_Name=request.POST["txtname"]
        s1.Stud_Phone=request.POST["txtphone"]
        s1.Stud_Semester=request.POST["txtsem"]
        s1.Stud_Course=Course.objects.get(course_name = request.POST["ddlcourse"])
        s1.save()
        return redirect('display_student')
    return render(request,"update_students.html",{'data': s1, 'Course_Data': course})

def delete_student(request,id):
    s1=Student.objects.get(id=id)
    s1.delete()
    return redirect("display_student")


def assign_books(request):
    c1=Course.objects.all()
    return render(request,'assign_book.html',{'data':c1})
def readsemester(request):
    student_semester=request.POST['txtsem']
    student_course=Course.objects.get(course_name=request.POST['ddlcourse'])
    student=Student.objects.filter(Q(student_semester=student_semester) & Q(student_course=student_course))
    print(student)
    book=Book.objects.filter(Q(course_id=Course.objects.get(course_name=student_course)))
    return render(request,'assign_book.html',{'Students':student,'Books':book})

def readassignbook(request):
    ib=Issue_book()
    ib.student_name=Student.objects.get(student_name=request.POST['ddlSname'])
    ib.book_name=Book.objects.get(book_name=request.POST['ddlSbook'])
    ib.issue_date=request.POST['startDate']
    ib.end_date=request.POST['endDate']
    ib.save()
    return render(request,'assign_book.html')


def issued_book(request):
    ib=Issue_book.objects.all()
    return render(request,"issued_book.html",{'data':ib})

def issuebookupdate(request,id):
    ib=Issue_book.objects.get(id=id)
    if request.method=='POST':
        ib.Student_Name = Student.objects.get(student_name=request.POST['txtStudentName'])
        ib.Book_Name = Book.objects.get(book_name=request.POST['txtBookName'])
        ib.Issued_Date = request.POST['txtissuedDate']
        ib.Valid_Till = request.POST['txtvalidtill']
        ib.save()
        return redirect('issued_book')
    return render(request,'issuebookupdate.html',{'data':ib})

def issubookdelete(request,id):
    ib = issued_book.objects.get(id=id)
    ib.delete()
    return redirect('issued_book')

def studentissuedbook(request):
    ib=Issue_book.objects.filter(student_name=Student.objects.get(student_name=request.session['Name']))
    return render(request,'student_issued_book.html',{'data':ib})

def logout_fun(request):
    auth.logout(request)
    return redirect("/")
