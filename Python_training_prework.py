# -*- coding: utf-8 -*-
"""
Spyder Editor
POS2CSV.py
This script file is extracting data
from a POS from a directory with one text file (ddmmyyyy.tsc) per day
into a csv file.
There are other files in the same directory with other endings with no value for this export.
Please adjust these variables as needed:
- data_dir  (path)
- data_file (filename)
- separator (for excel like ',' ';')
"""

"""
Clean all the variables of the session:
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')

import glob,os,sys,datetime,time

"""
Directory of the data and file name of the export and separator of the csv.
"""
data_dir  = 'C:/Users/Martin/Documents/_Martin/Python/POS2CSV/POS2CSVData/'
data_file = 'POS2CSV_Export.csv'
separator = ';'

"""
FUNCTION: Format a date from 'dd.mm.yyyy' to 'yyyy-mm-dd' (ISO external date):
"""
current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
current_date      = current_date_time[ 0:10]
current_time      = current_date_time[11:20]
def dateform1(date1="dd.mm.yyyy"):
    dateform1v1 = date1[6:10] + '-' + date1[3:5] + '-' + date1[0:2]
    return dateform1v1
"""
dateform1()
dateform1('dd.mm.yyyy')
dateform1('23.12.2015')
"""

"""
FUNCTION: suppress_stdout:
"""
from contextlib import contextmanager
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
"""
print("Now you see it")
with suppress_stdout():
    print("Now you don't")
"""

"""
Read all the records of all the filenames with '*.tsc' from the listed dir (data_dir)
and write them in an array:
"""
arrayall  = ['']
file_dir_extension = os.path.join(data_dir, '*.tsc')
for file_name in glob.glob(file_dir_extension):
    """  print file_name """
    with open(file_name) as f1:
        array1   = list(f1)
        arrayall = arrayall + array1

"""
Write a csv header and write it to a file (1. line)
"""
export1 =                               \
      'Extrakt_Dat'                     \
    + separator                         \
    + 'Extrakt_Zeit'                    \
    + separator                         \
    + 'Kassen_Dat'                      \
    + separator                         \
    + 'Kassen_Dat_YYYY'                 \
    + separator                         \
    + 'Kassen_Dat_MM'                   \
    + separator                         \
    + 'Kassen_Dat_MM_Nme'               \
    + separator                         \
    + 'Kassen_Dat_DD'                   \
    + separator                         \
    + 'Kassen_Dat_DD_Nme'               \
    + separator                         \
    + 'Kassen_Dat_Week_Of_Year'         \
    + separator                         \
    + 'Kassen_Dat_Week_of_Month'        \
    + separator                         \
    + 'Kassen_Nr'                       \
    + separator                         \
    + 'Tisch_Nr'                        \
    + separator                         \
    + 'Artikel_Nr'                      \
    + separator                         \
    + 'Artikel_Text'                    \
    + separator                         \
    + 'Artikel_Anz'                     \
    + separator                         \
    + 'Artikel_Preis'                   \
    + separator                         \
    + 'Artikel_Preis_Tot'               \
    + '\n'

""" print export1 """
f2 = open(data_dir + data_file, 'w')
f2.write(export1)
f2.close()

"""
Read all the records in the array, extract all the fields,
clean them and write (append) them in a csv formated file (from 2. line to the end)
"""
tischnr   = ' '
kassenr   = ' '
kassendat = ' '

for s in arrayall:

    if s[0:5]      == 'Tisch':
        tischnr    = s[ 7:-1] 
    elif s[0:5]    == 'Kasse':
        kassenr    = s[ 7:-1] 
    elif s[0:5]    == 'Datum':
        kassendat  = s[ 8:-1] 
        with suppress_stdout():
            kassendatISOstr = str( dateform1(kassendat) ) 
       
        kassendatISOdate = datetime.date(*(int(s) for s in kassendatISOstr.split('-')))        
        
    else:
        artikelnr  = s[ 0: 4] 
        artikeltxt = s[ 5:20] 
        artikelcnt = s[22:24] 
        artikelpr  = s[27:33] 
        artikelprt = s[34:-1] 

    if artikelnr.strip()   != '':

        export1 =                                \
          current_date                           \
        + separator                              \
        + current_time                           \
        + separator                              \
        + kassendatISOstr                        \
        + separator                              \
        + str(kassendatISOdate.year)             \
        + separator                              \
        + str(kassendatISOdate.month)            \
        + separator                              \
        + str(kassendatISOdate.month)            \
        + '_' + kassendatISOdate.strftime("%B")  \
        + separator                              \
        + str(kassendatISOdate.day)              \
        + separator                              \
        + str(kassendatISOdate.strftime("%w"))   \
        + '_' + kassendatISOdate.strftime("%A")  \
        + separator                              \
        + str(kassendatISOdate.isocalendar()[1]) \
        + separator                              \
        + str(kassendatISOdate.day / 7 + 1)      \
        + separator                              \
        + kassenr.strip()                        \
        + separator                              \
        + tischnr.strip()                        \
        + separator                              \
        + artikelnr.strip()                      \
        + separator                              \
        + artikeltxt.strip()                     \
        + separator                              \
        + artikelcnt.strip()                     \
        + separator                              \
        + artikelpr.strip()                      \
        + separator                              \
        + artikelprt.strip()                     \
        + separator                              \
        + '\n'

        """ print export1 """ 
        f2 = open(data_dir + data_file, 'a')
        f2.write(export1)
        f2.close()
        
