import numpy as np

class Assessment(object):

    def __init__(self,category,num,grades,due_date=None,post_date=None,optional=False):
        self.category=category
        self.num=num
        self.grades=np.array(grades)
        self.due_date=due_date
        self.post_date=post_date
        self.optional=optional

        for i in range(0,len(self.grades)):
            if self.grades[i]=='-':
                self.grades[i]=0.0
            else:
                self.grades[i]=float(self.grades[i])

        self.grades=self.grades.astype(float)