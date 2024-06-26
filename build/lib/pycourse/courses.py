import numpy as np
from .assessments import Assessment
from .accomodations import Accomodation

class Course(object):

    def __init__(self,name,code=None,semester=None,year=None):
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


        self.name=name
        self.code=code
        self.semester=semester
        self.year=year
        self.nstudent=0

        self.firstnames=np.array([])
        self.lastnames=np.array([])
        self.i_ds=np.array([])
        self.emails=np.array([])


        self.assessments=np.array([])
        self.categories=np.array([])
        self.cat=np.array([]) 
        self.ncat=np.array([])

        self.nums=np.array([])
        self.accomodations=np.array([])

        self.all_grades=np.array([])

    
    def add_student(self,firstname,lastname,i_d,email):

        """Add a student do the course

        Parameters
        ----------
        firstname : str
            Student's first name
        lastname : str
            Student's last name
        i_d : int
            Student's ID number
        email : str
            Student's email address
        """

        self.firstnames=np.append(self.firstnames,firstname)
        self.lastnames=np.append(self.lastnames,lastname)
        self.i_ds=np.append(self.i_ds,i_d)
        self.emails=np.append( self.emails,email)

        self.accomodations=np.append(self.accomodations,Accomodation(firstname,lastname,i_d,email))


        return 1


    def add_students(self,firstnames,lastnames,i_ds,emails):
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
        for i in range(0,len(firstnames)):
            add_return=self.add_student(firstnames[i],lastnames[i],i_ds[i],emails[i])

        return add_return

    def add_assessment(self,category,num,grades,optional=False):
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
        self.assessments=np.append(self.assessments,Assessment(category,num,grades,optional))
        self.categories=np.append(self.categories,category)
        self.nums=np.append(self.nums,num)

        self.all_grades=np.append(self.all_grades,self.assessments[-1].grades)
        self.grades=self.all_grades.reshape(len(self.assessments),len(grades)).T

        self._update_categories(category)

    def _update_categories(self,category):

        print('UP DEBUG: ',category,self.cat)

        if category not in self.cat:
            self.cat=np.append(self.cat,category)
            self.ncat=np.append(self.ncat,1)
        elif category in self.cat:
            arg=np.argwhere(self.cat==category).flatten()
            self.ncat[arg]+=1

        self.ncats=dict(zip(self.cat, self.ncat))

    def add_accomodation(self,firstname=None,lastname=None,i_d=None,email=None,category=None,num=None,ndrops=None,nmisses=None):
        """Add an accomodation for a select student

        Parameters
        ----------
        firstname : str
            strudents first name (default : None)
        lastname : str
            strudents lastname (default : None)
        i_d : int
            strudents i_d (default : None)
        email : str
            strudents email address (default : None)
        category : str
            category that accomodation is to be applied (default: None)
        num : int
            assessment number within category that accomodation is to be appled (default: None)
        ndrops : int
            number of lowest assessments within category to be dropped for accomodated student
        nmisses : int
            number of missed assessments within category to be dropped for accomodated student
        """

        student_arg = self._student_search(firstname,lastname,i_d,email)

        if student_arg>=0:
            self.accomodations[student_arg].add_accomodation(category,num,ndrops,nmisses)
        else:
            print('Accomodation not added')

    def calc_grades(self,scheme,return_weighting=False):
        """Calculate final category grades and final grades

        Parameters
        ----------
        scheme : class
            Grading scheme for the course
        return_weighting : bool
            If True, self.weights will be created with the weight of each assessment (default: False)
        """

        #setup default weights
        self.weights0=np.zeros(len(self.assessments))
        self.final_grades=np.zeros(len(self.firstnames))
        self.final_cat_grades=np.zeros([len(self.firstnames),len(self.ncats)])
        self.keepers=np.ones([len(self.firstnames),len(self.assessments)])

        if return_weighting:
            self.weights=np.zeros([len(self.firstnames),len(self.assessments)])

        for i in range(0,len(self.assessments)):
            cat=self.assessments[i].category
            self.weights0[i]=scheme.weights[cat]/self.ncats[cat]

        #Account for optional assessments, allowed misses, and reweighting schemes
        for i in range(0,len(self.firstnames)):
            if return_weighting:
                self.final_grades[i],self.final_cat_grades[i],self.keepers[i],self.weights[i]=self._calc_student_grade(self.grades[i],scheme,weights0=self.weights0,accomodation=self.accomodations[i],return_weighting=return_weighting)
            else:
                self.final_grades[i],self.final_cat_grades[i],self.keepers[i]=self._calc_student_grade(self.grades[i],scheme,weights0=self.weights0,accomodation=self.accomodations[i],return_weighting=return_weighting)

    def optimize_grades(self,schemes,return_weighting=False):
        """Calculate final category grades and final grades using the scheme that maximizes grade

        Parameters
        ----------
        schemes : class
            Grading schemes for the course
        """

        #setup default weights
        self.weights0=np.zeros([len(self.firstnames),len(self.assessments)])
        self.final_grades=np.zeros(len(self.firstnames))
        self.final_cat_grades=np.zeros([len(self.firstnames),len(self.ncats)])
        self.keepers=np.ones([len(self.firstnames),len(self.assessments)])

        if return_weighting:
            self.weights=np.zeros([len(self.firstnames),len(self.assessments)])
            weights=np.zeros([len(self.firstnames),len(self.assessments)])

        for scheme in schemes:

            weights0=np.zeros(len(self.assessments))
            final_grades=np.zeros(len(self.firstnames))
            final_cat_grades=np.zeros([len(self.firstnames),len(self.ncats)])
            keepers=np.ones([len(self.firstnames),len(self.assessments)])

            for i in range(0,len(self.assessments)):
                cat=self.assessments[i].category
                weights0[i]=scheme.weights[cat]/self.ncats[cat]

            #Account for optional assessments, allowed misses, and reweighting schemes
            for i in range(0,len(self.firstnames)):
                if return_weighting:
                    final_grades[i],final_cat_grades[i],keepers[i],weights[i]=self._calc_student_grade(self.grades[i],scheme,weights0=weights0,accomodation=self.accomodations[i],return_weighting=return_weighting)
                else:
                    final_grades[i],final_cat_grades[i],keepers[i]=self._calc_student_grade(self.grades[i],scheme,weights0=weights0,accomodation=self.accomodations[i],return_weighting=return_weighting)

            optgrade=final_grades>self.final_grades

            self.final_grades[optgrade]=final_grades[optgrade]
            self.final_cat_grades[optgrade]=final_cat_grades[optgrade]
            self.keepers[optgrade]=keepers[optgrade]
            if return_weighting:
                self.weights[optgrade]=weights[optgrade]


    def _calc_student_grade(self,grades,scheme,weights0=None,accomodation=None,return_weighting=False):

            npass=dict(zip(self.ncats.keys(),np.zeros(len(self.ncats))))
            keepers=np.ones(len(grades),dtype=bool)
            final_cat_grade=np.zeros(len(self.ncats))

            if weights0 is None:
                weights0=np.zeros(len(self.assessments))

                for i in range(0,len(self.assessments)):
                    cat=self.assessments[i].category
                    weights0[i]=scheme.weights[cat]/self.ncats[cat]

            #Set allowed misses, drops and optional assignments to non-keepers
            for j in range(0,len(self.assessments)):

                cat=self.assessments[j].category
                num=self.assessments[j].num

                if accomodation is not None:

                    print('DEBUG0':,cat,num,accomodation.categories,accomodation.nums)

                    if cat in accomodation.categories and num in accomodation.nums:
                        keepers[j]=False
                    elif cat in accomodation.nmisses.keys():
                        nmiss_extra=accomodation.nmisses[cat]
                    else:
                        nmiss_extra=0

                if self.assessments[j].optional and grades[j]==0 and keepers[j]:
                    keepers[j]=False
                elif not self.assessments[j].optional and grades[j]==0 and npass[cat] < (scheme.nmisses[cat]+nmiss_extra) and keepers[j]:
                    print('DEBUG: ',npass[cat],scheme.nmisses[cat],nmiss_extra)
                    npass[cat]+=1
                    keepers[j]=False


            for j in range(0,len(self.ncats)):
                cat=self.cat[j]
                ndrop=scheme.ndrops[cat]

                if accomodation is not None:
                    if cat in accomodation.ndrops.keys():
                        ndrop+=accomodation.ndrops[cat]

                if ndrop>0:

                    cat=scheme.categories[j]
                    catmatcharg=np.argwhere((self.categories==cat)*keepers).flatten()
                    minsortargs=np.argsort(grades)

                    ndropmatch=0
                    for minarg in minsortargs:
                        if minarg in catmatcharg:
                            keepers[minarg]=False
                            ndropmatch+=1
                        if ndropmatch==ndrop:
                            break


            #Find new weights           
            weights=np.zeros(len(self.assessments))

            for j in range(0,len(self.ncats)):

                cat=scheme.categories[j]

                catmatchcount=(self.categories==cat)*keepers

                if scheme.reweighting[cat]=='internal':
                    totweight0=scheme.weights[cat]
                    totweights=np.sum(weights0[catmatchcount])
                    weights[catmatchcount]=weights0[catmatchcount]*totweight0/totweights

                    #Sanity Check
                    diff = abs(np.sum(weights[catmatchcount]) - scheme.weights[cat])
                    if diff > 0.001:
                        print('GRADE SUM ERROR',j,final_cat_grade,np.sum(final_cat_grade),totweight0,totweights,diff)                    

                elif scheme.reweighting[cat]=='external':
                    weights[catmatchcount]=weights0[catmatchcount]

            #Scale keeper weights
            if np.sum(weights)<100.0:
                weights*=100.0/np.sum(weights)

            #Calculate final grade and final category grades
            final_grade=np.sum(weights*grades)/100.0

            for j in range(0,len(self.ncats)):
                cat=scheme.categories[j]
                catmatchcount=(self.categories==cat)*keepers

                final_cat_grade[j]=np.sum(weights[catmatchcount]*grades[catmatchcount])/100.0

            #Sanity check
            diff=abs(np.sum(final_cat_grade) - final_grade)
            if diff > 0.001:
                print('GRADE SUM ERROR',i,final_cat_grade,np.sum(final_cat_grade),final_grade)

            if return_weighting:
                return final_grade,final_cat_grade,keepers,weights
            else:
                return final_grade,final_cat_grade,keepers

    def _student_search(self,firstname=None,lastname=None,i_d=None,email=None):

        args=np.arange(0,len(self.firstnames),1)
        matches=np.ones(len(self.firstnames),dtype=bool)

        if firstname is not None:
            matches*=(self.firstnames==firstname)
        if lastname is not None:
            matches*=(self.lastnames==lastname)
        if i_d is not None:
            matches*=(self.i_ds==i_d)
        if email is not None:
            matches*=(self.emails==email)

        if np.sum(matches)>1:
            print('ERROR: Please provide more identiying information')
            return -1
        else:
            return int(args[matches][0])
