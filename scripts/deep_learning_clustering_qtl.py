#!/usr/bin/env python
"""
Summary:
This script contains code to do clustering using neural networks (deep learning)
Dependencies: 
- vector_data.py -> data, preprocessing_qtl
Neural networks are used to predict description or trait category of validation data
Modelling by qtl (chromosome number)
"""


# 1. Import X from vector_data script, select relevant columns and transform in appropriate format

from vector_data import X_train, X_valid, X_test, preprocessing_qtl

import numpy as np

y_train=X_train['desc']

X_train=X_train[['one_hot_desc1', 'one_hot_desc2', 'one_hot_desc3', 'p_lrt', 'chr_num']]

y_valid=X_valid['desc']

X_valid=X_valid[['one_hot_desc1', 'one_hot_desc2', 'one_hot_desc3', 'p_lrt', 'chr_num']]

y_test=X_test['desc']

X_test=X_test[['one_hot_desc1', 'one_hot_desc2', 'one_hot_desc3', 'p_lrt', 'chr_num']]



# 2. Select the 2 columns, do clustering and plot

import tensorflow as tf
import matplotlib.pyplot as plt # import plot manager
import os
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import silhouette_score
from random import choice

from tensorflow.keras.utils import to_categorical

tf.keras.utils.set_random_seed(2024) # set random seed for tf, np and python


out_dir=os.path.abspath('../output/') # define directory to save plots to



class Columns2Clustering:

    """
    Represent clustering task on 2 columns extracted from dimensionality reduction
    """
    
    def __init__(self, training, validation, test):
        self.training=training
        self.validation=validation
        self.test=test
    
    
    def get_features(self):
        """
        Extract 2 PCA from preprocessing_hits pipeline
        """
        preprocessed_training=preprocessing_qtl.fit_transform(self.training)
        preprocessed_validation=preprocessing_qtl.transform(self.validation)
        preprocessed_test=preprocessing_qtl.transform(self.test)
        
        return preprocessed_training, preprocessed_validation, preprocessed_test
        

    def perform_neural_clustering(self, reduced_features_train):
        """
        Perform neural clustering on 2 features columns
        """
        normalization_layer_unsup=tf.keras.layers.Normalization(input_shape=(2,))
        neural_model_unsup=tf.keras.models.Sequential([
        normalization_layer_unsup,
        tf.keras.layers.Dense(units=10, activation='relu'),
        tf.keras.layers.Dense(units=10, activation='relu'),
        tf.keras.layers.Dense(units=10, activation='relu'),
        tf.keras.layers.Dense(units=10, activation='relu'),
        tf.keras.layers.Dense(units=10, activation='relu'),
        tf.keras.layers.Dense(units=5, activation='softmax'), # number of clusters set to 5 here
        ])
        neural_clustering=Pipeline([('preprocessing_qtl', preprocessing_qtl), ('neural_unsupervised', neural_model_unsup)])
        neural_clustering[1].compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        normalization_layer_unsup.adapt(np.array(reduced_features_train))
        neural_clustering.fit(self.training, y_train, neural_unsupervised__epochs=10, neural_unsupervised__batch_size=1000)
        #print('The labels for the first 5 training data are: ', dbscan_clustering.labels_[:5]) # check labels of first 5 training data

        return neural_clustering
    
    
    def get_clusters_labels(raw_predictions_proba):
    
        """
        Loop through output dimensions and select the cluster with the highest probability
        """
        clusters_unsup=[]
        for i in raw_predictions_proba:
            temp=[]
            for (x,y) in enumerate(i):
                if y==max(i):
                    temp.append(x)
            clusters_unsup.append(choice(temp))
        
        return clusters_unsup
        
    
    def visualize_plot(neural_clustering, X_train, get_clusters_labels, size=500):
        """
        Generate actual visualization of clusters
        Save figure
        """
        y_pred_unsup_train=neural_clustering.predict(X_train)
        
        #print('The probabilities of clusters assignment are: ', y_pred_unsup_train[:10])
        
        clusters_unsup_train=get_clusters_labels(y_pred_unsup_train)
        
        #print('The silhouette score obtained as clustering performance measure on training set is:', silhouette_score(X_train, clusters_unsup_train))
        
        plt.figure(figsize=(10, 10))
        plt.scatter(X_train[:, 0], X_train[:, 1], c=clusters_unsup_train)
        plt.xlabel("PC 1", fontsize=10)
        plt.ylabel("PC 2", fontsize=10, rotation=90)
        plt.savefig(os.path.join(out_dir, f"Project_PCA_neural_clustering_result_by_qtl"))
        
        
     
    def predict_neural_clustering(neural_clustering, X_valid, get_clusters_labels):
        """
        Use neural networks to predict clustering on validation set
        """
        y_pred_unsup_valid=neural_clustering.predict(X_valid)
        
        clusters_unsup_valid=get_clusters_labels(y_pred_unsup_valid)
        
        #print('The silhouette score obtained as clustering performance measure on validation set is:', silhouette_score(X_valid, clusters_unsup_valid))
        
        return clusters_unsup_valid

     

# Main

def main():

    clustering_task=Columns2Clustering(X_train, X_valid, X_test)

    X_train_features, X_valid_features, X_test_features=clustering_task.get_features()

    actual_clustering=clustering_task.perform_neural_clustering(X_train_features)

    Columns2Clustering.visualize_plot(actual_clustering[1], X_train_features, Columns2Clustering.get_clusters_labels)

    Columns2Clustering.visualize_plot(actual_clustering[1], X_valid_features, Columns2Clustering.get_clusters_labels)

    prediction_clusters=Columns2Clustering.predict_neural_clustering(actual_clustering[1], X_valid_features, Columns2Clustering.get_clusters_labels)

    

import timeit

time_taken = timeit.timeit(lambda: main(), number=5)
print(f"Execution time for deep_learning_clustering_qtl.py is : {time_taken} seconds")
