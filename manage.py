# myapp/models.py
from django.db import models

class Customer(models.Model):
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    tipe = models.CharField(max_length=50)
    checkin = models.DateField()
    checkout = models.DateField()
    jml = models.IntegerField()
    ket = models.TextField()
    status = models.CharField(max_length=50)

# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer

def home(request):
    return render(request, 'index.html')

def customertampildata(request):
    datapemesan = Customer.objects.all().order_by('-id')
    return render(request, 'admin.html', {'datapemesan': datapemesan})

def customerinsert(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        email = request.POST['email']
        phone = request.POST['phone']
        tipe = request.POST['tipe']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        jml = request.POST['jml']
        ket = request.POST['ket']
        status = 'Dalam Proses'  # Sesuaikan dengan logika Anda

        customer = Customer(nama=nama, email=email, phone=phone, tipe=tipe, checkin=checkin, checkout=checkout, jml=jml, ket=ket, status=status)
        customer.save()

        messages.success(request, 'Data Berhasil di kirim')
        return redirect('home')

def customerupdate(request):
    if request.method == 'POST':
        id = request.POST['id']
        nama = request.POST['nama']
        email = request.POST['email']
        phone = request.POST['phone']
        tipe = request.POST['tipe']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        jml = request.POST['jml']
        status = request.POST['status']

        customer = Customer.objects.get(id=id)
        customer.nama = nama
        customer.email = email
        customer.phone = phone
        customer.tipe = tipe
        customer.checkin = checkin
        customer.checkout = checkout
        customer.jml = jml
        customer.status = status
        customer.save()

        messages.success(request, 'Data Berhasil di Update')
        return redirect('customertampildata')

def customerhapus(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()

    messages.success(request, 'Data Berhasil di Hapus')
    return redirect('customertampildata')
