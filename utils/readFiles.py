import os
import re

path =  os.chdir('C://Users//503025052//Documents//GE//GE TestCases')
filenames = os.listdir(path)


for index,filename in enumerate(filenames):
    try:
        extension = os.path.splitext(filename)[1][1:]
        if(extension=='xlsx'):
            number =re.findall(r'\d+', str(filename))
            if(number[0]):
                taskName = filename.replace(number[0],'')
                taskName = taskName.replace(extension,'')
                taskName = taskName.replace('-','')
                taskName = taskName.replace('.','')
                taskName = taskName.replace('(QA)','')
                taskName = taskName.strip()
                
                numberJira = int(number[0])-3
                print(str(index)+'|'+str(taskName)+'|https://jira.verndale.com/browse/GEHC-'+str(numberJira))
        
    except IOError:
        print('Cant change %s' % (filename))

print("All Files have been updated")