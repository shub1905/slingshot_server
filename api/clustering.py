from sklearn.cluster import KMeans
from collections import defaultdict

class Clustering:

    def __init__(self):
        self.n_clusters = 4
        self.km = KMeans(n_clusters=self.n_clusters, n_jobs=-1)

    def cluster(self, X, names):
        if X.shape[0] < self.n_clusters:
            self.km = KMeans(n_clusters=X.shape[0], n_jobs=-1)

        prev_iner = 0
        best_iner = 10**8
        best_clusters = 4

        for i in range(3, 10):
            self.km = KMeans(n_clusters=i, n_jobs=-1)
            self.labels = self.km.fit_predict(X)
            if i==3:
                diff = 100
            else:
                diff = (prev_iner - self.km.inertia_) * 100.0 / self.km.inertia_

            prev_iner = self.km.inertia_
            print 'cluster numbers:', i, diff, best_iner, best_clusters
            if diff < best_iner:
                best_iner = diff
                best_clusters = i

            if best_iner < 3.:
                break

        self.km = KMeans(n_clusters=best_clusters, n_jobs=-1)
        self.labels = self.km.fit_predict(X)
        self.groups = defaultdict(list)

        for i, lab in enumerate(self.labels):
            self.groups[lab].append(names[i][1])

        return self.groups

cluster = Clustering()
