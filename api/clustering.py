from sklearn.cluster import KMeans

class Clustering:
	def __init__(self):
		self.km = KMeans(n_jobs=-1)

	def cluster(self, X):
		self.labels = self.km.fit_predict(X)
		return self.labels

cluster = Clustering()