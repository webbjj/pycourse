import pycourse as pyc
import numpy as np


nstudents=10
expected_grades=np.arange(10,110,10)

firstnames=np.random.rand(nstudents)
lastnames=np.random.rand(nstudents)
emails=np.random.rand(nstudents)
i_ds=np.random.rand(nstudents)


def course_check(course,nc,na,weights0,nmiss=0,tol=0.001):

		#Check keeper array
		assert abs(np.sum(course.keepers)-nc*na*nstudents+nmiss*nc*nstudents) <= tol
		
		#Check weights0 array
		assert len(course.weights0) == int(nc*na)
		assert np.sum(np.fabs(course.weights0-weights0)) <=tol
		
		#Check final grades are as expected
		assert np.sum(np.fabs(course.final_grades - expected_grades)) <= tol

def test_optimize_scheme(tol=0.001):
	ncats=[1,2,3,4]
	nassess=[2,3,4,5]

	for nc in ncats:
		for na in nassess:
			if na==2:
				nzeros=[1]
			else:
				nzeros=[1,2]

			for nz in nzeros:

				cat_names=np.linspace(1,nc,nc).astype(str)
				cat_weights=np.random.rand(nc)
				cat_weights*=(100.0/np.sum(cat_weights))

				alt_weights=cat_weights
				alt_weights[-1]=0.0
				alt_weights*=100.0/np.sum(alt_weights)

				scheme=pyc.GradingScheme(cat_names,weights=cat_weights,nmisses=0)
				altscheme=pyc.GradingScheme(cat_names,weights=alt_weights,nmisses=0)

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				print(nc,na,nz,cat_names)

				for i in range(0,nc):
					for j in range(1,na+1):
						if j<na+1-nz:
							course.add_assessment(cat_names[i],j,expected_grades)
						else:
							course.add_assessment(cat_names[i],j,np.zeros(nstudents))

				for i in range(0,len(firstnames)):
					for j in range(0,nc):
						course.add_accomodation(firstname=firstnames[i],lastname=lastnames[i],category=cat_names[j],nmisses=nz)
					print(course.accomodations[i].nmisses.keys())
					print(course.accomodations[i].nmisses.values())

				course.calc_grades(scheme)
				grades=course.grades

				course.calc_grades(altscheme)
				altgrades=course.grades

				course.optimize_grades([scheme,altscheme])
				optgrades=course.grades

				np.testing.assert_array_equal(np.maximum(grades,altgrades),optgrades)