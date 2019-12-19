









# Thresholds and Alerts
Thresholds and Alerts Python scripts allows the user to analyze marketing 
data to pinpoint peaks and thresholds using linear regression and created 
an alert to notify the client of noteworthy change made by a competitor. 


## Installation 

### Install Python

Install [Python](https://www.python.org/downloads/) 64-Bit version 3.7 or earlier.

32-Bit version of Python has a restriction of 4 GB RAM usage. Because the 
analysis libraries are working with massive data sets, most of analysis are 
with over 5 GB of data, compiler generates an error. 

In order to run the given Python scripts, user need to use Python Integrated 
Development Environment (IDE). When installing Python, it comes with a 
default IDE. However, it is recommended to third party IDE such as PyCharm 
to run the scripts. The program was developed and tested in PyCharm. 


### Install pip
Use the package manager [pip](https://pip.pypa.io/en/stable/installing/) to install libraries. 


### NOTE
After installing Python and pip, we need to create an environment path for 
windows to run Python and pip. Path will help installing libraries through 
command line which is required to run the program.


Python:
Copy the downloaded Python folder. 
It is usually in this directory if installed with default settings: \
    C:\Users\%UserAccountName%\AppData\Local\Programs\Python

pip: 
Copy the downloaded pip folder. 
It is usually in this directory if installed with default settings: \
    C:\Users\%UserAccountName%\AppData\Local\Programs\Python\Scripts

These are example directory paths. Make sure to find the appropriate 
directory for your download.

```
Windows 10: 

1. Open System Properties (Keyboard shortcut win + pause)

2. Click Advanced system settings in the sidebar

3. Click Environment Variables...

4. Select Path in the System variables section

5. Click Edit

6. On the right sidebar, click new, copy the python directory and 
paste it into the opend textbar. 

7. On the right sidebar, click new, copy the pip directory and 
paste it into the opend textbar. 

8. Click ok on the current and all the following windows to 
complete setup and apply changes to the system properties.
```


### Python Libraries

Open command prompt in windows and input each of the given pip statement to 
install the libraries. 

* [matplotlib](https://pypi.org/project/matplotlib/)
```
    pip install matplotlib
```

* [numpy](https://pypi.org/project/numpy/)
```
    pip install numpy
```

* [pandas](https://pypi.org/project/pandas/)
```
    pip install pandas
```

* [python-dotenv](https://pypi.org/project/python-dotenv/)
```
    pip install python-dotenv
```

* [scikit-learn](https://pypi.org/project/scikit-learn/)
```
    pip install scikit-learn
```

* [secure-smtplib](https://pypi.org/project/secure-smtplib/)
```
    pip install secure-smtplib
```

* [setuptools](https://pypi.org/project/setuptools/)
```
    pip install setuptools
```

* [xlrd](https://pypi.org/project/xlrd/)
```
    pip install xlrd
```

* [mock](https://pypi.org/project/xlrd/)
```
    pip install mock
```




# Running clustering files

The clustering files will include:
totalrpdpplot, scatterpltrpdp, clusterrpdpKmean, clusterrpdpDBscan, cbcluster

## File structure

In Python, user can find the clustering files under
```bash
Python Scripts -> source -> plots
```

## File Directory

Make sure correct file directory is implemented in the .env file under
```bash
FCA_Competitive_Messaging_Dir
```

This will help locate the data files location used for the program to run.

## Installing packages

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
dependencies

```bash
pip install pandas
pip install matplotlib
pip install scikit-learn
pip install seaborn
```

## Usage

Recurring payment vs down payment of clustering is used to figure out which
brands have similar points on the same graph.











