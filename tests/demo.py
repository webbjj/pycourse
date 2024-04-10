#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pycourse as pyc
import numpy as np
import matplotlib.pyplot as plt


# ### Setup
#Initialize your course. 
#These inputs aren't used at the moment, but would be used in the future
#when saving the Course object or outputting data
"""Course class

Parameters
----------
name : str
    Course Name
code : str
    Course Code (default: None)
semester : str
    Semester Name (default: None)
year : float
    Year course is being run (default: None)
"""
# In[2]:


course=pyc.Course(name='Test Class',code='NATS0000',semester='Winter',year='2024')

"""A grading scheme for a course

Parameters
----------
categories : str
    Array of category names
weights : int or float
    Array of category weights
ndrops : int or float
    Array of number of lowest assessments to drop (default: 0)
nmisses : int or float
    Array of number of missed assessments to drop (default: 0)
reweighting : str
    How should assessments in each category be reweighted if there is a drop, miss, or accomodation? (default: 'external')
    Can be a single string or array of strings for each category
    if 'internal':
        assessments within each category will be reweighted while the contribution
        of the category itself to the final grade won't change
    if 'external':
        All categories will be reweighted to account for a missing assessment within
        a given category
"""
# In[3]:


scheme=pyc.GradingScheme(['iClicker','Assignment','Project','Exam']
                      ,weights=[10,10,30,50],ndrops=[1,0,0,0],nmisses=[0,0,0,0],reweighting=['internal','internal','external','external'])

Will need to read in the gradebook manually for now. However in the future I would 
like to automate this process
# In[4]:


#Read in header of gradebook to find column number of each assessment
file=open('test_gradebook.csv','r')
header=file.readline().split(',')
for i,h in enumerate(header):
    print(i,h)
file.close()


# In[5]:


#Read in full gradebook
gradebook=np.loadtxt('test_gradebook.csv',skiprows=1,dtype=str,delimiter=',')

"""Add an array of students to the course

Parameters
----------
firstnames : str
    Student first names
lastnames : str
    Student last names
i_ds : int
    Student ID numbers
emails : str
    Student email addresses
"""
# In[6]:


#Add all of the students based on information in gradebook
course.add_students(gradebook[:,0],gradebook[:,1],gradebook[:,2],gradebook[:,3])

"""Add an assessment to the course

Parameters
----------
category : str
    Assessment category
num : int
    Assessment number within the category
grades : float
    Array of student grades
optional : bool
    Is assessment optional or not? (default: False)
"""
# In[7]:


#Based on information from the header, manually add each assessment
for i in range(7,23):
    nassess=1
    course.add_assessment('iClicker',nassess,gradebook[:,i].tolist())
    nassess+=1
    
for i in [24,25,26,27,28,32,29,30,31]:
    nassess=1
    course.add_assessment('Assignment',i,gradebook[:,i].tolist())
    nassess+=1
    
for i in [34,35,36]:
    nassess=1
    course.add_assessment('Project',i,gradebook[:,i].tolist())
    nassess+=1
    
for i in [38,39]:
    nassess=1
    course.add_assessment('Exam',i,gradebook[:,i].tolist())
    nassess+=1


# In[8]:


#Sanity check to confirm what the course categories are
course.cat


# In[9]:


#Sanity check to confirm which grade from the gradebook corresponds to what category
course.categories

"""Calculate final category grades and final grades

Parameters
----------
scheme : class
    Grading scheme for the course
return_weighting : bool
    If True, self.weights will be created with the weight of each assessment (default: False)
"""
# In[10]:


course.calc_grades(scheme,return_weighting=True)


# ### Analysis

# In[11]:


#Consider student1:
print('Student 1s grade in each assessment is: ',course.grades[0])
print('The default weighting scheme was: ',course.weights0)
print('The weightings used to calculate Student1s grade are: ',course.weights[0])

print('Student 1s final grade is :',course.final_grades[0])
print('Student 1s grades in each category are :',course.final_cat_grades[0])


# In[12]:


#Consider global properties
print('Average = ',np.mean(course.final_grades))
print('Median = ',np.median(course.final_grades))
print('STD = ',np.std(course.final_grades))


# In[13]:


#Plot final grade distribution

plt.hist(course.final_grades)
plt.xlabel('Final Grade (%)')
plt.ylabel('N')
plt.show()
plt.close()


# In[14]:


#Plot grade distribution in each category

for i in range(0,len(course.cat)):
    #Plot final grade distribution
    plt.hist(100.0*course.final_cat_grades[:,i]/scheme.weights[course.cat[i]])
    plt.xlabel('Final Grade (%)')
    plt.ylabel('N')
    plt.title(course.cat[i])
    plt.show()
    plt.close()


# ### Optimize Grades
If instead of one grading scheme, you have several, it is possible
to define many schemes and then optimize each student's grade. Each student's
individual weighting will be in course.weights if return_weighting=True
# In[15]:


scheme_1=pyc.GradingScheme(['iClicker','Assignment','Project','Exam']
                      ,weights=[10,10,30,50],ndrops=[1,0,0,0],nmisses=[0,0,0,0],reweighting=['internal','internal','external','external'])

scheme_2=pyc.GradingScheme(['iClicker','Assignment','Project','Exam']
                      ,weights=[10,10,20,40],ndrops=[0,0,0,0],nmisses=[1,1,1,1],reweighting=['internal','internal','external','external'])

scheme_3=pyc.GradingScheme(['iClicker','Assignment','Project','Exam']
                      ,weights=[20,20,20,20],ndrops=[1,1,0,0],nmisses=[0,0,0,0],reweighting=['internal','internal','external','external'])


# In[16]:


course.optimize_grades([scheme_1,scheme_2,scheme_3],return_weighting=True)


# In[17]:


#Consider student1:
print('Student 1s grade in each assessment is: ',course.grades[0])
print('The weightings used to calculate Student1s grade are: ',course.weights[0])

print('Student 1s final grade is :',course.final_grades[0])
print('Student 1s grades in each category are :',course.final_cat_grades[0])


# In[18]:


#Consider global properties
print('Average = ',np.mean(course.final_grades))
print('Median = ',np.median(course.final_grades))
print('STD = ',np.std(course.final_grades))


# In[19]:


#Plot final grade distribution

plt.hist(course.final_grades)
plt.xlabel('Final Grade (%)')
plt.ylabel('N')
plt.show()
plt.close()


# In[ ]:




