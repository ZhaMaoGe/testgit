# testgit
A easy django website with simple html appearance and simple backend. This website can crawl information from a specific website. The web site
is hard encoded in code, and the information is about tender.
# prerequests
* python2.7 or python3.6
* django 
* lxml 
* requests 
* json
* mysql-server
# code stucture
```
├── mysite
    ├── demo                          # Examples of pretrained models
        ├── migrations                
        ├── static                    #some css file
        ├── templates                 #front view template files, using bootstrap
        ├── upload                    #store the specific website
        ├── views.py                  #the logic code with front view files
        ├── verifycode.py             #generate a verify code
        ├── urls.py                   #url mapping
        ├── province.py               #crawl code
        ├── data_analysis.py          #analysis data
    ├── mysite                        # admin view
        ├── settings.py               #url mapping
    ├── templates                     # admin view template
    └── manage.py                     # Main file , using python mange.py runserver 0.0.0.0:8000 to see protype
└── README.md
```
# install step
1. add mysql user and password for the database connnection, setting is in mysite/settings.py
2. create a database
2. python manage.py migrate to create tables
3. add a user in mysql and login
