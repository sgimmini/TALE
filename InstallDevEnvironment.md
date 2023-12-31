## Install Python

# Install miniconda (Download from website)


# Update conda
conda update -n base -c defaults conda

# Create repository
conda create -n tale python==3.11

# Activate environment
conda activate tale

# Install the requirered Python packages
pip install -r requirements.txt

## Install VS Code

# Download Visual Studio Code (ask Google how to do)

# Update VS Code
Help > Check for Updates...

# Install the following extensions
Draw.io Integration
Python
Pylint
autopep8
Mypy Type Checker

# Set conda environment
open a python file (e.g. source/content.py)
click on bottom right tray, right of python
select tale conda environment


## Use git

# Start a new branch
checkout to... >dev
pull
branch > create branch from > dev  
    feature/[your feature name]

# Pull request
Commit your changes
Go to github.com > select your branch > Create pull request
Select destination of pull request to dev
Requets pull request

# Some else does code review
On github.com
Select pull requests > click on one of the pull requests
Files changed > Do your code review

# Delete branch
In VS Code
Branch > Delete branch ... > feature/[your feature name]


### Setting up

Using the TALE Project virtual environment only django should be necessary to install  
```
$ pip install Django==4.2.7  
```
Then you can run the server by   
```
$ python manage.py runserver  
````

It could be that you need to migrate. For this run 
```
$ python manage.py makemigrations  
$ python manage.py migrate 
```

