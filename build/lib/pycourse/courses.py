import numpy as np

class Course(object):

    def __init__(self,name,code=None,semester=None,year=None):

        self.name=name
        self.code=code
        self.semester=semester
        self.year=year

        self.categories=np.array([])
        self.weights=np.array([])
        self.nassessments=np.array([])
        self.ndrops=np.array([])
        self.nmisses=np.array([])

    def add_category(self,category,weight,nassessment,ndrops,nmisses):

        if len(self.categories) > 0:
            if np.in1d(category,self.categories):
                print('One or more categories already exist')
                return -1

        self.categories=np.append(self.categories,category)
        self.weights=np.append(self.weights,weight)
        self.nassessments=np.append(self.nassessments,nassessment)
        self.ndrop=np.append(self.ndrops,ndrop)
        self.nmiss=np.append(self.nmisses,nmiss)

    def add_categories(self,categories,weights,nassessments,ndrops,nmisses):
    
        #Check to make sure categories don't exist:
        for i in range(0,len(categories)):
            self.add_categor(categories[i],weights[i],nassessments[i],ndrops[i],nmisses[i])
        
    def load_gradebook(self,filename,fmt='moodle',classlist=True):
        pass
        
        
    def load_assessment(self):
        pass
        
    
        
