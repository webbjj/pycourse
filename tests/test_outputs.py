import pycourse as pyc
import numpy as np

nstudents=10

firstnames=np.random.rand(nstudents)
lastnames=np.random.rand(nstudents)
emails=np.random.rand(nstudents)
i_ds=np.random.rand(nstudents)

def initialize_random_course():

	scheme=pyc.GradingScheme('1',weights=[100.0],nmisses=0)

	course=pyc.Course('TEST')
	course.add_students(firstnames,lastnames,emails,i_ds)
	course.add_assessment('1',1,np.random.rand(nstudents)*100.0)
	course.calc_grades(scheme)

	return course

def test_roundup():

	course=initialize_random_course()

	pyc.output(course,identifier='i_d',filename='test_output.csv',header=False,lettergrade=False,roundup=True)

	data=np.loadtxt('test_output.csv',dtype=str,delimiter=',')

	for i in range(0,len(data)):
		assert float(data[i,1]) % 1 == 0.0

def test_roundto50():

	course=initialize_random_course()

	pyc.output(course,identifier='i_d',filename='test_output.csv',header=False,lettergrade=False,roundup=True,roundto50=0.0)

	nround=np.sum(course.final_grades < 50.0)
	n50i=np.sum(course.final_grades == 50.0)


	data=np.loadtxt('test_output.csv',dtype=str,delimiter=',')

	outgrades=data[:,1].astype(float)

	nout=np.sum(outgrades<50)
	n50=np.sum(outgrades==50.0)

	assert nout == 0.
	assert nround >= nout
	assert nround+n50i == n50

def test_letter_grades():

	grades=[35,45,52.5,57.5,62.5,67.5,72.5,77.5,85.0,95.0]
	expected_letter=['F','E','D','D+','C','C+','B','B+','A','A+']

	course=initialize_random_course()

	course.final_grades=grades

	pyc.output(course,identifier='i_d',filename='test_output.csv',header=False,lettergrade=True)

	data=np.loadtxt('test_output.csv',dtype=str,delimiter=',')

	for i in range(0,len(data)):
		assert data[i,1] == expected_letter[i]
