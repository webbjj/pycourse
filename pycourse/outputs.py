import numpy as np

def output(course,identifier='i_d',filename='output.csv',header=True,assessments=False,weights=False,duedates=False,postdates=False,lettergrade=False,roundup=False,roundto50=None):
	"""output final grades and potentially other details

	Parameters
	----------
	course : class
	    A course class object with final grades calculated
	identifier : str
		A single str or array of strings with identifying information to be outputted (e.g. 'firstname', 'lastname', 'email', and/or 'i_d') (default: 'i_d')
	filename : str
		Name of file to ouput data to (default: 'output.csv')
	header : bool
		If True, a header is included in the output file that labels each column (default: False)
	assessments : bool
		If True, individual assessment grades will also be written to the output file (default: False)
	weights : bool
		If True, the weight of each assessement will also be written to the output file (default: False)
	duedates : bool
		If True, the due date of each assessment will also be written to the output file (default: False)
	postdates : bool
		If True, the grade posting date of each assessment will also be written to the output file (default: False)
	lettergrade : bool
		If True, the final grade written to the output file will be a letter grade (default: False)
	roundup : bool
		If True, final grades will be rounded up to the nearest integeger value
	roundto50 : None
		If set, all final grades between roundto50 and 50.0 will be rounded to 50.0 (default : None)
	"""

	final_grades=grade_maker(course.final_grades,lettergrade,roundup,roundto50)

	outfile=open(filename,'w')

	if isinstance(identifier,np.ndarray) or isinstance(identifier,list):
		nid=len(identifier)
	else:
		nid=0

	if header:

		if 'firstname' in identifier:
			outfile.write('First Name,')
		if 'lastname' in identifier:
			outfile.write('Last Name,')
		if 'email' in identifier:
			outfile.write('Email,')
		if 'i_d' in identifier:
			outfile.write('ID,')

		if assessments:
			for i in range(0,len(course.assessments)):
				outfile.write('%s %s,' % (course.assessments[i].category,course.assessments[i].num))

				if weights:
					outfile.write('Weight,')

				if duedates:
					outfile.write('Due Date,')

				if postdates:
					outfile.write('Post Date,')

		outfile.write('Grade')

		outfile.write('\n')

	for i in range(0,len(course.firstnames)):

		if 'firstname' in identifier:
			outfile.write('%s,' % course.firstnames[i])
		if 'lastname' in identifier:
			outfile.write('%s,' % course.lastnames[i])
		if 'email' in identifier:
			outfile.write('%s,' % course.emails[i])
		if 'i_d' in identifier:
			outfile.write('%s,' %course.i_ds[i])

		if assessments:
			for j in range(0,len(course.assessments)):
				outfile.write('%f,' % (course.grades[i][j]))

				if weights:
					outfile.write('%f,' % (course.weights[i][j]))

				if duedates:
					outfile.write('%s,' % (course.assessments[j].duedate))

				if postdates:
					outfile.write('%s,' % (course.assessments[j].postdate))

		if lettergrade:
			outfile.write('%s' % final_grades[i])
		else:
			outfile.write('%f' % final_grades[i])
		outfile.write('\n')

	outfile.close()

def grade_maker(grades,lettergrade=False,roundup=False,roundto50=None):
	"""convert an initial grade caluclation to a final form for output

	Parameters
	----------
	grades : class
	    initial caluclation of grades
	lettergrade : bool
		If True, the final grade written to the output file will be a letter grade (default: False)
	roundup : bool
		If True, final grades will be rounded up to the nearest integeger value
	roundto50 : None
		If set, all final grades between roundto50 and 50.0 will be rounded to 50.0 (default : None)
	"""


	new_grades=np.zeros(len(grades))

	if roundup:
		new_grades=np.ceil(grades)
	else:
		new_grades=grades

	if roundto50 is not None:
		indx=(new_grades>=roundto50) * (new_grades < 50.0)
		new_grades[indx]=50.0

	if lettergrade:
		new_grades=letter_maker(new_grades)

	return new_grades


def letter_maker(grades): 
	"""convert an numerical grade caluclation to a letter grade

	Parameters
	----------
	grades : class
	    initial caluclation of grades
	"""
	letter_grades=np.array([])

	lowers=[90,80,75,70,65,60,55,50,40,0]
	labels=['A+','A','B+','B','C+','C','D+','D','E','F']

	for grade in grades:

		for j in range(0,len(lowers)):
			if grade >= lowers[j]:
				letter_grades=np.append(letter_grades,labels[j])
				break
	return letter_grades





