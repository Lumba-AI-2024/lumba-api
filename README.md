## Cara clone dan menjalankan project
1. Clone project  
`git clone https://github.com/MKM-EAI/backend.git`  
2. Buat virtual environment  
`python virtualenv venv`  
3. Aktifkan virtual environment  
`source venv/bin/activate`  
4. Install library yang terdokumentasi di requirements.txt  
`pip install -r requirements.txt`  
5. Buat folder directory, default username, dan default workspace dengan path seperti berikut ini  
`backend/directory/default/default`  
6. Buat migrasi model ke database  
`python ./eai/manage.py makemigrations`  
`python ./eai/manage.py migrate`  
7. Jalankan server  
`python ./eai/manage.py runserver`  

## Jangan lupa dokumentasikan library sebelum push
`pip freeze > requirements.txt`
