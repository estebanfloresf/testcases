from openpyxl import load_workbook
#import the pandas library and aliasing as pd and numpy as np
import pandas as pd
import numpy as np
import os 


class createTestCase():
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        
        self.wb = load_workbook(self.dir_path+'\\inputTC.xlsx')
        self.ws = self.wb['Sheet1']
     
        self.commonWords = ["note:","notes:","important note:","onclick/ontap","consists of:"]
        self.changeWords = [
            {"from": "will be", "to": "is"},
            {"from": "will wrap", "to": "wraps"},
            {"from": "will not be", "to": "is not"},
            {"from": "will dissapear", "to": "dissapears"},
            {"from": "will have", "to": "has"},
            {"from": "will move up", "to": "moves up"},
            {"from": "will fall back", "to": "fallbacks"},
            {"from": "will never be", "to": "is never"},
            {"from": "if", "to": "when"}

        ]
        self.verifyLst= []
        self.expectedLst= []
        #   # Transform the ws into a panda dataframe
        self.df = pd.DataFrame(self.ws.values)
        # # replace None values with NA and drop them
        self.df = self.df.replace(to_replace='None', value=np.nan).dropna()
        
        
        header = self.df.iloc[0]
        self.df = self.df[1:]
        self.df = self.df.rename(columns = header)
        self.df = self.df.reset_index(drop=True)
        self.dfList = self.df[header].values
   

    def __main__(self):
      self.createVfyLst(self.dfList)
      self.createExpLst(self.dfList)
      self.df.to_csv(self.dir_path+'\\resultsTC.csv',encoding='utf-8', index=False)
      
      

    def createVfyLst(self,dfList):
        try:       
            for req in dfList:
                band =0 
                req = str(req[0]).lower()        
                reqToLst  = req.split(' ')
                for word in reqToLst:
                    if(word in self.commonWords):
                        band =1
                        break
                if(band==0):
                    self.verifyLst.append("Verify "+req)
                else:
                    self.verifyLst.append(req.capitalize())
                
            # Find the name of the column by index
            replaceClmn = self.df.columns[0] 
            # Drop that column
            self.df.drop(replaceClmn, axis = 1, inplace = True)
            # Put whatever series you want in its place
            self.df[replaceClmn] = self.verifyLst
        except ValueError:
            print("There was a problem")


    def createExpLst(self,dfList):
        
        try:
            for req in dfList:          
                req = str(req[0]).lower()
                for wordrplc in self.changeWords:
                    if(wordrplc['from'] in req):
                        req = req.replace(wordrplc['from'],wordrplc['to'] )
                        break

                self.expectedLst.append(str(req).capitalize())                    
            
            self.df['Expected'] = self.expectedLst
            # Adding columns wth -1 value for the excel testcase format
            browserList = [-1] * len(self.expectedLst)
            browserListNoApply = ['---'] * len(self.expectedLst)
            self.df['windowsIE'] = browserList
            self.df['windowsCH'] = browserList
            self.df['windowsFF'] = browserList
            self.df['macSF'] = browserListNoApply
            self.df['macCH'] = browserListNoApply
            self.df['macFF'] = browserListNoApply
            
            print("CSV file generated with success")
        except ValueError:
            print("There was a problem")
     
        
       


if __name__ == "__main__":
    app = createTestCase()
    app.__main__()





        
