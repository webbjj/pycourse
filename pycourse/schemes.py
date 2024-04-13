import numpy as np

class GradingScheme(object):
	def __init__(self,categories=None,weights=None,ndrops=0,nmisses=0,reweighting='external'):
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

		self.categories=categories


		if weights is None:
			self.weights=dict(zip(self.categories,np.ones(len(self.categories))*100.0/len(self.categories)))
		else:
			self.weights=dict(zip(self.categories,weights))

		if ndrops==0:
			self.ndrops=dict(zip(self.categories,np.zeros(len(self.categories))))
		elif isinstance(ndrops,float) or isinstance(ndrops,int):
			self.ndrops=dict(zip(self.categories,ndrops*np.ones(len(self.categories))))
		else:
			self.ndrops=dict(zip(self.categories,ndrops))

		if nmisses==0:
			self.nmisses=dict(zip(self.categories,np.zeros(len(self.categories))))

		elif isinstance(nmisses,float) or isinstance(nmisses,int):
			self.nmisses=dict(zip(self.categories,nmisses*np.ones(len(self.categories))))
		else:
			self.nmisses=dict(zip(self.categories,nmisses))

		if reweighting == 'external':
			self.reweighting=dict(zip(self.categories,[reweighting]*len(self.categories)))
		elif reweighting == 'internal':
			self.reweighting=dict(zip(self.categories,[reweighting]*len(self.categories)))
		else:
			self.reweighting=dict(zip(self.categories,reweighting))

		self.subscheme=dict(zip(self.categories,np.zeros(len(self.categories),dtype=bool)))
		self.subweights=dict(zip(self.categories,np.zeros(len(self.categories))))
		self.optimize=dict(zip(self.categories,np.zeros(len(self.categories),dtype=bool)))

	def add_subscheme(self,category,weights,optimize=False):
		"""Add a subscheme to a category if assessments are not equally weighted within
			- note 
		Parameters
		----------
		category : str
		    Array of category names
		weights : int or float
		    Array of category weights
	    optimize : bool
	    	If True, highest weight will be given to highest grade
	    	If False, order of weights must match order assessments are loaded
	    	(Default: False)
		"""

		self.subscheme[category]=True
		self.subweights[category]=weights
		self.optimize[category]=optimize




