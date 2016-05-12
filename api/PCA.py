import numpy as np
from sklearn.decomposition import PCA

class PCA:
	def __init__(self, n_components=30):
		self.pca = PCA(n_components=n_components)

	def fit(self, X):
		self.pca.fit(X)

	def dim_reduction(self, X):
		self.fit(X)
		red_X = numpy.dot(self.pca.components_, X.T)
		return red_X.T