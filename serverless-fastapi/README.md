

python -m venv venv
=======

py -m venv venv

source venv/Scripts/activate





# 버전

pip 버전 : pip install --upgrade pip

버전 저장: pip freeze > requirements.txt: 각 package 버전을 저장한다.

버전 다운: pip install -r requirements.txt







> 빌드  순서

1. site-packages zip 저장

​	cd venv/lib/site-packages   

​	zip -r9 ../../../function.zip .



2. app 파일 funciton.zip파일에 끼워넣기

   cd ../../../

   zip -g ./function.zip -r app



3.  S3에 function.zip파일 넣기



> 실행
>
> VSCODE
> uvicorn app.main:app
