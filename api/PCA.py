import numpy as np
from sklearn.decomposition import PCA


class ComponentAnalysis:

    def __init__(self, n_components=30):
        self.pca = PCA(n_components=n_components)

    def dim_reduction(self, X):
        X_new = self.pca.fit_transform(X)
        return X_new


pca_model = ComponentAnalysis()
