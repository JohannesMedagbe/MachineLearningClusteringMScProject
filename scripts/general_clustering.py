#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
    
class ModellingDBSCAN:

    """
    Represent ML operations using DBSCAN by hits
    """
    
    def __init__(self, training, validation, test):
        """
        Instantiate a class object
        """
        self.training=training
        self.validation=validation
        self.test=test
        
    
    def plot_dbscan(dbscan, X, size, show_xlabels=True, show_ylabels=True):
        """
        Display DBSCAN clustering distinguishing, core, non core and anomalies instances
        Data plotted according to 2 features provided
        """
        core_mask=np.zeros_like(dbscan.labels_, dtype=bool)
        core_mask[dbscan.core_sample_indices_]= True
        anomalies_mask=dbscan.labels_== -1
        non_core_mask= ~(core_mask | anomalies_mask)
        cores=dbscan.components_
        anomalies=X[anomalies_mask]
        non_cores=X[non_core_mask]
    
        plt.scatter(cores[:, 0], cores[:, 1], c=dbscan.labels_[core_mask], marker='o', s=size, cmap="Paired")
        plt.scatter(cores[:, 0], cores[:, 1], marker='*', s=20, c=dbscan.labels_[core_mask])
        plt.scatter(anomalies[:, 0], anomalies[:, 1], c="r", marker="x", s=100)
        plt.scatter(non_cores[:, 0], non_cores[:, 1], c=dbscan.labels_[non_core_mask], marker=".")
    
        if show_xlabels:
            plt.xlabel("PCA 1", fontsize=10)
        else:
            plt.tick_params(labelbottom=False)
    
        if show_ylabels:
            plt.ylabel("PCA 2", fontsize=10, rotation=90)
        else:
            plt.tick_params(labelleft=False)
    
    

class ModellingKMeans:

    """
    Represent ML operations using KMeans by hits
    """
    
    def __init__(self, training, validation, test):
        """
        Instantiate a class object
        """
        self.training=training
        self.validation=validation
        self.test=test
        
    def plot_decision_boundaries(clusterer, X, resolution=1000, show_centroids=True, show_xlabels=True, show_ylabels=True):
        """
        Display the clustering of the data, the centroids and the decision boundaries of kmeans
        """
        mins=X.min(axis=0) - 0.1
        maxs=X.max(axis=0) + 0.1
        xx, yy = np.meshgrid(np.linspace(mins[0], maxs[0], resolution), np.linspace(mins[1], maxs[1], resolution))
        Z=clusterer.predict(np.c_[xx.ravel(), yy.ravel()])
        Z=Z.reshape(xx.shape)
    
        plt.contourf(Z, extent=(mins[0], maxs[0], mins[1], maxs[1]), cmap="Pastel2")
        plt.contour(Z, extent=(mins[0], maxs[0], mins[1], maxs[1]), linewidths=1, colors='k', alpha=0.5)
    
    
    
        def plot_data(X):
            """
            Plot data according 2 columns selected
            """
            plt.plot(X[:, 0], X[:, 1], 'k.', markersize=2)
        
        plot_data(X)
    
    
    
        def plot_centroids(centroids, weights=None, circle_color='w', cross_color='k'):

            """
            Represent centroids differently
            """
            if weights is not None:
                centroids=centroids[weights > weights.max()/10]
            plt.scatter(centroids[:, 0], centroids[:, 1], marker='o', s=35, linewidths=8, color=circle_color, zorder=10, alpha=0.4)
            plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=2, linewidths=12, color=cross_color, zorder=11, alpha=0.6)
    

        if show_centroids:
            plot_centroids(clusterer.cluster_centers_)
        
        if show_xlabels:
            plt.xlabel("PCA 1", fontsize=20)
        else:
            plt.tick_params(labelbottom=False)
        if show_ylabels:
            plt.ylabel("PCA 2", fontsize=20, rotation=90)
        else:
            plt.tick_params(labelleft=False)



