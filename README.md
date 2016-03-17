# taj-exchange


#Setting Up MySQL Access to remote host
1. From cPanel interface, go to Remote MySQL and add your host ip. Wildcards using '%' are allowed.
2. From your local machine, use the command 'mysql -u 'username' -p -h 'remote host'' to connect to the databae.
    - currently host is web.engr.illinois.edu


## Getting Started


1. Get virtualenv
2. Update python to 2.7.x (if necessary)
3. Install pip for python 2.7.x
4. Install django


##Getting Virtualenv

	1. Download and extract the virtualenv python module
```
	$ curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-15.0.0.tar.gz
	$ tar xvfz virtualenv-15.0.0.tar.gz
	$ cd virtualenv-15.0.0
```
	2. Now we create a virtual environemnt 'myVE'
```
	$ python virtualenv.py ~/myVE
```
This creates a directory ~/myVE and sets up a virtual environment


##Updating python 	

Because we do not have root permissions on this server,
we must compile Python 2.7.x into our virtual environment.

1. Download the Python 2.7.x source code
======================================
	$ curl -O https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
	$ tar -zxvf Python-2.7.11.tgz 
======================================
2. We must now activate our virtual environment so that Python 2.7.11 
can be installed into ~/myVE/bin and ~/myVE/lib as opposed to the system
======================================	
	$ source ~/myVE/bin/activate
	(myVE) $ cd Python-2.7.11/
======================================
3. Now we must compile and install Python 2.7.11	
======================================	
	(myVE) $ ./configure
	(myVE) $ make altinstall prefix=~/myVE/ exec-prefix=~/myVE
======================================
These commands ensure that the python installation is placed into the 
virtual environment

4. Now that python is installed, we want to alias the python shell command to use Python 2.7.x
add to ~/.bashrc:

	alias python="~/myVE/bin/Python2.7"

And then we must tell our shell to use this upadated .bashrc file:

======================================
	(myVE) $ source ~/.bashrc
======================================

##Install pip for python 2.7.x

The version of pip that is installed with virtualenv is dependent
on the Python version you are using. To install pip2.7 we must do the following:

1. Navigate to the ~/myVE/bin directory
2. Activate the virtualenvironment:
======================================
	$ source activate
======================================
3. Compiling and installing Python should result in a file easy_install 
Within the ~/myVE/bin directory. Ensure easy_install uses the correct version of Python:
======================================
	(myVE) $ easy_install --version
======================================
You should see something like:
======================================
	setuptools 20.3 from ~/myVE/lib/python2.7/site-packages/setuptools-20.3-py2.7.egg (Python 2.7)
======================================
4. If there is a file within the current directory called pip, rename it to something else otherwise the new version of pip will not be installed.
======================================	
	(myVE) $ mv pip old.pip
======================================
4. Now we install pip for Python 2.7.11:
======================================	
	(myVE) $ easy_install pip
======================================
Once this installation is complete you can ensure you have the proper version by:
======================================
	(myVE) $ pip --version 
======================================
You should see something like:
======================================
	pip 8.1.0 ~/myVE/lib/python2.7/site-packages/pip-8.1.0-py2.7.egg (python 2.7)
======================================

##Install Django

Now that we have pip that runs on python 2.7, installing dependencies (such as Django) is as easy as:
======================================
	(myVE) $ pip install django
======================================
To test that django has been installed do:
======================================
	(myVE) $ python -c "import django; print django.__path__;"
======================================
Which should print the directory django is installed in.

Congratulation! You have setup the TAJ Exchange environment
