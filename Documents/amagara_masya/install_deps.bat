@echo off
echo Installing dependencies...

cd backend
call venv\Scripts\activate.bat

echo Installing Pillow first...
python -m pip install --upgrade pip
python -m pip install Pillow==11.2.1

echo Installing Django and core packages...
python -m pip install Django==4.2.10
python -m pip install djangorestframework==3.14.0
python -m pip install djangorestframework-simplejwt==5.3.1
python -m pip install django-cors-headers==4.3.1
python -m pip install django-filter==23.5

echo Installing phone number packages...
python -m pip install django-phonenumber-field==7.1.0
python -m pip install phonenumbers==8.13.22

echo Installing other dependencies...
python -m pip install python-dotenv==1.0.1
python -m pip install django-storages==1.14.2
python -m pip install boto3==1.28.62
python -m pip install django-allauth==0.57.0
python -m pip install django-crispy-forms==2.0
python -m pip install crispy-bootstrap5==2023.10
python -m pip install django-environ==0.11.2
python -m pip install django-import-export==3.3.0
python -m pip install django-report-builder==6.4.2

echo Dependencies installed successfully!
pause 