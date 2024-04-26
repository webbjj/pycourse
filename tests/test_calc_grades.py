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
		assert len(course.weights0[0]) == int(nc*na)

		print(course.weights0)
		print(weights0)

		assert np.sum(np.fabs(course.weights0-weights0)) <=tol
		
		#Check weighted grades

		assert np.sum(np.fabs(course.weights0-weights0)) <=tol
		assert np.sum(np.sum(course.final_grade_fracs,axis=1)-course.final_grades) <=tol


		#Check final grades are as expected
		assert np.sum(np.fabs(course.final_grades - expected_grades)) <= tol


def test_equal_weights(tol=0.001):
	ncats=[1,2,3,4]
	nassess=[2,3,4,5]

	for nc in ncats:
		for na in nassess:

			scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=np.ones(nc)*100.0/nc)

			course=pyc.Course('TEST')
			course.add_students(firstnames,lastnames,emails,i_ds)

			for i in range(1,nc+1):
				for j in range(1,na+1):
					course.add_assessment(str(float(i)),j,expected_grades)

			course.calc_grades(scheme)

			for i in range(0,nstudents):
				print(nc,na,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i])

			weights0=np.ones(int(nc*na))*100.0/float(nc*na)

			course_check(course,nc,na,weights0,tol=tol)


def test_unequal_weights(tol=0.001):
	ncats=[1,2,3,4]
	nassess=[2,3,4,5]

	for nc in ncats:
		for na in nassess:

			scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=np.ones(nc)*100.0/nc)

			course=pyc.Course('TEST')
			course.add_students(firstnames,lastnames,emails,i_ds)

			for i in range(1,nc+1):
				for j in range(1,na+1):
					course.add_assessment(str(float(i)),j,expected_grades)

			course.calc_grades(scheme)

			for i in range(0,nstudents):
				print(nc,na,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i])

			weights0=np.ones(int(nc*na))*100.0/float(nc*na)

			course_check(course,nc,na,weights0,tol=tol)

def test_sub_scheme(tol=0.001):
	
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

				scheme=pyc.GradingScheme(cat_names,weights=cat_weights,nmisses=0)
				for i in range(0,nc):
					new_weights=np.zeros(na)
					new_weights[:na-nz]=cat_weights[i]/(na-nz)

					scheme.add_subscheme(cat_names[i],new_weights,optimize=False)

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				print(nc,na,nz,cat_names)

				for i in range(0,nc):
					for j in range(1,na+1):
						if j<na+1-nz:
							course.add_assessment(cat_names[i],j,expected_grades)
						else:
							course.add_assessment(cat_names[i],j,np.zeros(nstudents))

				course.calc_grades(scheme)

				for i in range(0,nstudents):
					print(nc,na,nz,course.categories,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i],course.keepers[i])

				#Check weights0 array
				weights0=np.array([])
				for i in range(0,len(cat_weights)):
					weights0=np.append(weights0,np.ones(na)*(cat_weights[i]/(na-nz)))
					if nz>=1:
						weights0[-1]=0.
					if nz>=2:
						weights0[-2]=0.


				course_check(course,nc,na,weights0,nmiss=0,tol=tol)

def test_sub_scheme_optimize(tol=0.001):
	
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

				scheme=pyc.GradingScheme(cat_names,weights=cat_weights,nmisses=0)
				for i in range(0,nc):
					new_weights=np.zeros(na)
					new_weights[:na-nz]=cat_weights[i]/(na-nz)

					scheme.add_subscheme(cat_names[i],np.flip(new_weights),optimize=True)

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				print(nc,na,nz,cat_names,np.flip(new_weights))

				for i in range(0,nc):
					for j in range(1,na+1):
						if j<na+1-nz:
							course.add_assessment(cat_names[i],j,expected_grades)
						else:
							course.add_assessment(cat_names[i],j,np.zeros(nstudents))

				course.calc_grades(scheme)

				for i in range(0,nstudents):
					print(nc,na,nz,course.categories,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i],course.keepers[i])

				#Check weights0 array
				weights0=np.array([])
				for i in range(0,len(cat_weights)):
					weights0=np.append(weights0,np.ones(na)*(cat_weights[i]/(na-nz)))
					if nz>=1:
						weights0[-1]=0.
					if nz>=2:
						weights0[-2]=0.


				course_check(course,nc,na,weights0,nmiss=0,tol=tol)

def test_misses(tol=0.001):
	ncats=[1,2,3,4]
	nassess=[2,3,4,5]

	for nc in ncats:
		for na in nassess:
			if na==2:
				nzeros=[1]
			else:
				nzeros=[1,2]

			for nz in nzeros:

				cat_weights=np.random.rand(nc)
				cat_weights*=(100.0/np.sum(cat_weights))

				scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=cat_weights,nmisses=nz)

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				for i in range(1,nc+1):
					for j in range(1,na+1):
						if j<na+1-nz:
							course.add_assessment(str(float(i)),j,expected_grades)
						else:
							course.add_assessment(str(float(i)),j,np.zeros(nstudents))

				course.calc_grades(scheme)

				for i in range(0,nstudents):
					print(nc,na,nz,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i])

				#Check weights0 array
				weights0=np.array([])
				for i in range(0,len(cat_weights)):
					weights0=np.append(weights0,np.ones(na)*(cat_weights[i]/na))

				course_check(course,nc,na,weights0,nmiss=nz,tol=tol)

def test_ndrops(tol=0.001):
	ncats=[1,2,3,4]
	nassess=[2,3,4,5]

	for nc in ncats:
		for na in nassess:
			if na==2:
				nzeros=[1]
			else:
				nzeros=[1,2]

			for nz in nzeros:

				cat_weights=np.random.rand(nc)
				cat_weights*=(100.0/np.sum(cat_weights))

				scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=cat_weights,ndrops=nz)

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				for i in range(1,nc+1):
					for j in range(1,na+1):
						if j<na+1-nz:
							course.add_assessment(str(float(i)),j,expected_grades)
						else:
							course.add_assessment(str(float(i)),j,np.zeros(nstudents))

				course.calc_grades(scheme)

				for i in range(0,nstudents):
					print(nc,na,nz,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i])

				#Check weights0 array
				weights0=np.array([])
				for i in range(0,len(cat_weights)):
					weights0=np.append(weights0,np.ones(na)*(cat_weights[i]/na))

				course_check(course,nc,na,weights0,nmiss=nz,tol=tol)

def test_ndrops_and_nmisses(tol=0.001):
	ncats=[2,3,4]
	nassess=[3,4,5]

	for nc in ncats:
		for na in nassess:

			nzeros=[2]

			for nz in nzeros:

				cat_weights=np.random.rand(nc)
				cat_weights*=(100.0/np.sum(cat_weights))

				scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=cat_weights,ndrops=1,nmisses=1)

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				for i in range(1,nc+1):
					for j in range(1,na+1):
						if j<na+1-nz:
							course.add_assessment(str(float(i)),j,expected_grades)
						else:
							course.add_assessment(str(float(i)),j,np.zeros(nstudents))

				course.calc_grades(scheme)

				for i in range(0,nstudents):
					print(nc,na,nz,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i])

				#Check weights0 array
				weights0=np.array([])
				for i in range(0,len(cat_weights)):
					weights0=np.append(weights0,np.ones(na)*(cat_weights[i]/na))

				course_check(course,nc,na,weights0,nmiss=nz,tol=tol)

def test_internal_reweighting(tol=0.001):
	ncats=[1,2,3,4]
	nassess=[2,3,4,5]

	for nc in ncats:
		for na in nassess:
			if na==2:
				nzeros=[1]
			else:
				nzeros=[1,2]

			for nz in nzeros:

				cat_weights=np.random.rand(nc)
				cat_weights*=(100.0/np.sum(cat_weights))

				scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=cat_weights,nmisses=nz,reweighting='internal')

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				for i in range(1,nc+1):

					for j in range(1,na+1):
						if j<na+1-nz or i>1:
							course.add_assessment(str(float(i)),j,expected_grades)
						elif i==1:
							course.add_assessment(str(float(i)),j,np.zeros(nstudents))

				course.calc_grades(scheme)

				#Check weights0 array
				weights0=np.array([])
				for i in range(0,len(cat_weights)):
					weights0=np.append(weights0,np.ones(na)*(cat_weights[i]/na))

				#Since reweighting is internal, the weights of kept assignments should
				#higher

				print(nc,na,nz,weights0)
				print(course.weights)

				assert abs(np.sum(weights0)-np.sum(course.weights[i]))<=tol

				for i in range(0,len(course.firstnames)):
					for j in range(0,len(course.cat)):
						catmatch=(course.categories==course.cat[j])
						assert abs(np.sum(weights0[catmatch])-np.sum(course.weights[i][catmatch]))<tol
						if j==0:
							assert course.weights[i][catmatch][0]>weights0[catmatch][0]
						assert np.sum(course.weights[i]==0) == nz

def test_external_reweighting(tol=0.001):
	ncats=[2,2,3,4]
	nassess=[2,3,4,5]

	for nc in ncats:
		for na in nassess:
			if na==2:
				nzeros=[1]
			else:
				nzeros=[1,2]

			for nz in nzeros:

				cat_weights=np.random.rand(nc)
				cat_weights*=(100.0/np.sum(cat_weights))

				scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=cat_weights,nmisses=nz,reweighting='external')

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				for i in range(1,nc+1):

					for j in range(1,na+1):
						if j<na+1-nz or i>1:
							course.add_assessment(str(float(i)),j,expected_grades)
						elif i==1:
							course.add_assessment(str(float(i)),j,np.zeros(nstudents))

				course.calc_grades(scheme)

				#Check weights0 array
				weights0=np.array([])
				for i in range(0,len(cat_weights)):
					weights0=np.append(weights0,np.ones(na)*(cat_weights[i]/na))

				#Since reweighting is internal, the weights of kept assignments should
				#higher

				print(nc,na,nz,weights0)
				print(course.weights)

				assert abs(np.sum(weights0)-np.sum(course.weights[i]))<=tol

				for i in range(0,len(course.firstnames)):
					for j in range(0,len(course.cat)):
						catmatch=(course.categories==course.cat[j])

						if j==0:
							assert np.sum(weights0[catmatch])>np.sum(course.weights[i][catmatch])
						else:
							assert np.sum(weights0[catmatch])<np.sum(course.weights[i][catmatch])

						assert course.weights[i][catmatch][0]>weights0[catmatch][0]
						assert np.sum(course.weights[i]==0) == nz

					nonzeros=course.weights[i]!=0
					for j in range(0,np.sum(nonzeros)):
						assert abs(course.weights[i][nonzeros][j]/weights0[nonzeros][j]-100.0/(100.0-np.sum(weights0[np.invert(nonzeros)])))<tol

def test_optional(tol=0.001):
	ncats=[1,2,3,4]
	nassess=[2,3,4,5]

	#Check when optional assessments are 0
	for nc in ncats:
		for na in nassess:
			if na==2:
				nopts=[1]
			else:
				nopts=[1,2]
				
			for nopt in nopts:

				cat_weights=np.random.rand(nc)
				cat_weights*=(100.0/np.sum(cat_weights))

				scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=cat_weights)

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				for i in range(1,nc+1):
					for j in range(1,na+1):
						if j<na+1-nopt:
							course.add_assessment(str(float(i)),j,expected_grades)
						else:
							course.add_assessment(str(float(i)),j,np.zeros(nstudents),optional=True)

				course.calc_grades(scheme)

				for i in range(0,nstudents):
					print(nc,na,nopt,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i])

				#Check weights0 array
				weights0=np.array([])
				for i in range(0,len(cat_weights)):
					weights0=np.append(weights0,np.ones(na)*(cat_weights[i]/na))

				course_check(course,nc,na,weights0,nmiss=nopt,tol=tol)

		#Check when optional assessments are not zero
		for nc in ncats:
			for na in nassess:

				scheme=pyc.GradingScheme(np.linspace(1,nc,nc).astype(str),weights=np.ones(nc)*100.0/nc)

				course=pyc.Course('TEST')
				course.add_students(firstnames,lastnames,emails,i_ds)

				for i in range(1,nc+1):
					for j in range(1,na+1):
						course.add_assessment(str(float(i)),j,expected_grades,optional=True)

				course.calc_grades(scheme)

				for i in range(0,nstudents):
					print(nc,na,course.final_cat_grades[i],course.grades[i],course.final_grades[i],expected_grades[i])

				weights0=np.ones(int(nc*na))*100.0/float(nc*na)

				course_check(course,nc,na,weights0,tol=tol)