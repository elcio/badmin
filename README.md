# Web2py Badmin 

Badmin is an automatic admin interface for Web2py, built over Twitter Bootstrap.

## Setup

* simply install badmin on your app
* create an auth_group called "badmin"
* add membership on this group to the desired users (including you)
* access http://127.0.0.1:8000/yourapp/badmin

## Custom lists

You can add a filter to your lists and choose which columns to show, creating a global variable in your model, called badmin_tables, like this:


    badmin_tables={
      'auth_user':{
        'columns':['authorized','name','email','city','weekhours','workinplace','meetings'],
        'filters':['authorized','name','email','city','weekhours','workinplace','meetings'],
      },
      'job':{
        'columns':['project','name','time','start','open'],
        'filters':['name','time','open'],
      },
      'project':{
        'columns':['name',],
        'filters':['name'],
      },
      'page':{
        'columns':['title','slug','description','ordernum',],
        'filters':['title'],
      },
      'jobquestion':{
        'columns':['user','job','question','answer'],
        'filters':['question'],
      },
    }

You can also customize the menus, classifing tables. For doing this, include a new property, category, in badmin_tables, like this:

    badmin_tables={
      'auth_user':{
        'columns':['authorized','name','email','city','weekhours','workinplace','meetings'],
        'filters':['authorized','name','email','city','weekhours','workinplace','meetings'],
        'category':'main',
      },
      'job':{
        'columns':['project','name','time','start','open'],
        'filters':['name','time','open'],
        'category':'project',
      },
      'project':{
        'columns':['name',],
        'filters':['name'],
        'category':'project',
      },
      'page':{
        'columns':['title','slug','description','ordernum',],
        'filters':['title'],
        'category':'main',
      },
      'jobquestion':{
        'columns':['user','job','question','answer'],
        'filters':['question'],
        'category':'main',
      },
    }

Finally, you can choose tables to hide:

    badmin_exclude_tables=['auth_cas','auth_event','issue']

