#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pytesseract as terr
import os
import pymongo
import json
from re import *


# In[36]:


import glob
from PIL import Image

keyword_list = ['python','skill','mail','education','resume','cv','curriculum vitae','work','experience','computer',
                'data science','big data','date','dob','d.o.b','certification','certified','certificate','software','developer',
                'employment','university','technical','career','phone','strenghts','accomplish','language','professional']

# keyword list for computer science resume.

is_resume = 0
isnot_resume = 0


# In[37]:


print("Enter Resume File pathname")
for filepath in list(glob.iglob(input())):
        img = Image.open(filepath)
        text1 = terr.image_to_string(img)
        text = text1.lower()
        print(text)
        
        matched_keys = [i for i in keyword_list if i in text]
        matched = len(matched_keys)
        print(matched_keys)
        
        if matched > 3:
            is_resume += 1 
        else:
            isnot_resume += 1
            print(filepath)
            
        
        
print("classified as resume:", is_resume)
print("Not classified as resume:", isnot_resume)
        
    


# In[ ]:




