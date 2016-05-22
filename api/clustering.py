from sklearn.cluster import KMeans
from collections import defaultdict


class Clustering:

    def __init__(self):
        self.n_clusters = 4
        self.km = KMeans(n_clusters=self.n_clusters, n_jobs=-1)

    def cluster(self, X, names):
        if X.shape[0] < self.n_clusters:
            self.km = KMeans(n_clusters=X.shape[0], n_jobs=-1)
        self.labels = self.km.fit_predict(X)
        self.groups = defaultdict(list)

        for i, lab in enumerate(self.labels):
            self.groups[lab].append(names[i][1])

        return self.groups

cluster = Clustering()
