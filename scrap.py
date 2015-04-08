# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:30:07 2015

@author: pol delgado martin
"""
import os
import shutil
import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

try:
    shutil.rmtree('report')
except:
    pass
os.makedirs('report')
os.chdir('report')

document='<table border="1" style="border-collapse:collapse">'
Users={
    #Put users here
}


"""
pwd=Users.items()[0][1]
user=Users.items()[0][0]
"""
for user,pwd in Users.iteritems():
    browser=RoboBrowser(history=True)
    browser.open('https://www.aqmetrix.com', verify=False)

    form=browser.get_forms().pop()
    form['nombre'].value=user
    form['passwd'].value=pwd
    browser.submit_form(form, verify=False)
    
    table=BeautifulSoup(browser.session.get('https://www.aqmetrix.com/aqx/diary/infodisp/get_infodisp_incidencias.php').content)
   
    j=0
    for row in table.select('table tbody tr'):
        document=document+'<tr>'        
        for data in row.select('td'):
            if data.select('a') == []:
                document=document+data.prettify()
            else:
                for i in data.select('a'):
                    if 'PNG' in i.attrs['href']:
                        document=document+'<td>'
                        r = browser.session.get(i.attrs['href'], stream=True)
                        name=str(user)+str(j)+'.PNG'
                        i.attrs['href']=name
                        if r.status_code == 200:
                            with open(name, 'wb') as f:
                                r.raw.decode_content = True
                                shutil.copyfileobj(r.raw, f)
                            document=document+'<img src="'+name+'" height="50%">'   
                            document=document+'</td>'
                    if 'TXT' in i.attrs['href']:
                        document=document+'<td>'
                        r = browser.session.get(i['href'])
                        text=r.text
                        ip=re.findall('(?<=IP PUBLICA :\s)[0-9.]+',text)[0]
                        document=document+ip
                        document=document+'</td>'
             
        document=document+'</tr>'        
        j=j+1
        
document=document+'</table>'
with open('index.html','w') as f:
    f.write(document)

    
