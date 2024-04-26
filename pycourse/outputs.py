import numpy as np

def output(course,identifier,filename='output.csv',assessments=False,weights=False,duedates=False,postdates=False,header=True):

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


		outfile.write('%f' % course.final_grades[i])
		outfile.write('\n')

	outfile.close()




