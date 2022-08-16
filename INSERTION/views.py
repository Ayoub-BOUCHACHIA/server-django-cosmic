from django.shortcuts import redirect
from django.shortcuts import render
from .forms import FilesForm, LoginForm,FilesForm_for_pipline
import os
from django.contrib.auth import logout
from django.http import HttpResponse
# Create your views here.
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login
from .utils import *
from zipfile import ZipFile


def main(request):
    
    if request.user.is_authenticated:
        print("is authentificat")
        if request.method == 'POST':
            files_form = FilesForm(request.POST, request.FILES)
            if files_form.is_valid():
                from django.utils.datastructures import MultiValueDictKeyError
                
                platform_file = request.FILES['platform_file']
                
                try:
                    srs_file = files_form.cleaned_data["srs_file"]
                except MultiValueDictKeyError:
                    srs_file = None
                
                print(srs_file)
                fs = FileSystemStorage()
                
                
                filename_platform = fs.save("platform_file."+platform_file.name.split('.')[-1], platform_file)
                uploaded_platform_file_url = fs.url(filename_platform)
                print(uploaded_platform_file_url)
                
                message = insert_COSMIC_DATABASE(uploaded_platform_file_url[1:].replace('/',"\^").replace('^',''),srs_file)                
                
                delete_file(uploaded_platform_file_url[1:].replace('/',"\^").replace('^',''))
                
                
                return render(request,'INSERTION/home.html', context={
                    "message" : message
                })
                
                
        return render(request,'INSERTION/home.html')
    
    else:
        return redirect('/admin/login/?next=/admin/')
    


def generateDataset(request):
    
    # create a ZipFile object
    zipObj = ZipFile('dataset_cosmic.zip', 'w')
    # Add multiple files to the zip
    path_download_data_COSMIC_measurement = download_data_COSMIC_measurement()
    path_download_data_functional_user = download_data_functional_user()
    path_download_data_non_functional_requirement = download_data_non_functional_requirement()
    path_download_data_ambiguous_requirement = download_data_ambiguous_requirement()
    path_download_data_movements = download_data_movements()
    
    zipObj.write(path_download_data_COSMIC_measurement)
    zipObj.write(path_download_data_functional_user)
    zipObj.write(path_download_data_non_functional_requirement)
    zipObj.write(path_download_data_ambiguous_requirement)
    zipObj.write(path_download_data_movements)
    
    # close the Zip File
    zipObj.close()

    file_path = 'dataset_cosmic.zip'
    
    delete_file(path_download_data_COSMIC_measurement)
    delete_file(path_download_data_functional_user)
    delete_file(path_download_data_non_functional_requirement)
    delete_file(path_download_data_ambiguous_requirement)
    delete_file(path_download_data_movements)
    
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    delete_file(file_path)
    return response
    


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/insertion')
    else:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                print("checker auten ..")
                user = check_authentication(username=username,password=password)
                if user:
                    login(request, user)                    
                    return redirect('/insertion')
                
                else:
                    return render(request,'INSERTION/login.html', context={
                        "message" : "There is an error in the username or password"
                    })
                    
    return render(request,'INSERTION/login.html')

def logout_user(request):
    logout(request)
    return redirect("/")


def pipline(request):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            files_form = FilesForm_for_pipline(request.POST, request.FILES)
            if files_form.is_valid():
                srs_file = request.FILES["srs_file"]
                
                fs = FileSystemStorage()
                
                print("srs_file path : ",srs_file)
                
                filename_srs = fs.save("srs_file."+srs_file.name.split('.')[-1], srs_file)
                uploaded_srs_file_url = fs.url(filename_srs)
                print(uploaded_srs_file_url)
                
                data = pipline_COSMIC_measurement(uploaded_srs_file_url[1:].replace('/',"\^").replace('^',''))                
                 
                delete_file(uploaded_srs_file_url[1:].replace('/',"\^").replace('^',''))
                
                return render(request,'INSERTION/pipline.html', context={
                    "data" : data
                })
            
                """
                return render(request,'INSERTION/pipline.html', context={ 
                    "data" : {
                        "len_ambiguous" : len(data["ambiguous"]),
                        "len_unambiguous" : len(data["unambiguous"]),
                        "len_nfr" : len(data["nfr"]),
                        "len_fur" : len(data["fur"]),
                        "len_data_mouvements" : len(data["data_mouvements"]),
                        "ambiguous" : data["ambiguous"],
                        "unambiguous" : data["unambiguous"],
                        "nfr" : data["nfr"],
                        "fur" : data["fur"],
                        "data_mouvements" : data["data_mouvements"]
                    }
                })
                """    
                                
        return render(request,'INSERTION/pipline.html')
    
    else:
        return redirect('/admin/login/?next=/admin/')
    

