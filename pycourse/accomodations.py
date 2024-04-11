import numpy as np

class Accomodation(object):
	def __init__(self,firstname,lastname,i_d,email):

		"""Add a student accomodation

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
		ndrops : int or float
		    Array of number of lowest assessments to drop (default: 0)
		nmisses : int or float
		    Array of number of missed assessments to drop (default: 0)
		"""

		self.firstname=firstname
		self.lastname=lastname
		self.i_d=i_d
		self.email=email

		self.categories=np.array([])
		self.nums=np.array([])
		self.ndrops={}
		self.nmisses={}

	def add_accomodation(self,category,num=None,ndrop=None,nmiss=None):

		if np.sum(np.array([num is not None,ndrop is not None, nmiss is not None])) > 1:
			print('Can only specific one accomodation')
			return -1

		else:
			self.categories=np.append(self.categories,category)
			self.nums=np.append(self.nums,num)

			if len(self.ndrops) == 0 and ndrop is not None:
				self.ndrops.update({category : ndrop})
			elif len(self.ndrops) >=1 and category not in self.ndrops.keys():
				self.ndrops.update({category : ndrop})				
			elif ndrop is not None and category in self.ndrops.keys():
				self.ndrops[category]+=ndrop

			
			if len(self.nmisses) == 0 and nmiss is not None:
				self.nmisses.update({category : nmiss})
			elif len(self.nmisses) >=1 and category not in self.nmisses.keys():
				self.nmisses.update({category : nmiss})				
			elif nmiss is not None and cateogry in self.nmisses.keys():
				self.nmisses[category]+=nmiss


