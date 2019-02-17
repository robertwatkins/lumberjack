#!/usr/local/bin/python3
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy.interpolate import griddata
import math
import hashlib
import networkx as nx
import seaborn as sns
import scipy as sp
import itertools
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import pairwise_distances
import pickle

# PREREQUISITES
# pip3 install pandas
# pip3 install scikit-learn
# pip3 install matplotlib
# pip3 install networkx
# pip3 install hdbscan
# pip3 install seaborn


apiServer = "http://127.0.0.1:8888"
trainingDir = "/trainingdata"
testDataDir = "/testdata"
nGramLength = 5
training_data = None
unique_url_map = None
distance_matrix = None
ngram_as_path = None
agent_id = None
data_root_path = None
clustering = None
sample_n_gram_list_as_ids = None

def train(path):
    data_root_path = path
    print('in apache trainer: path='+data_root_path)
    if sanityCheckPath(path):
        isSuccessful = start(data_root_path)
    else:
        return False
    return isSuccessful

def start(path):
    # read this document to follow this method
    # https://github.com/robertwatkins/playground-robert/blob/master/Python/Jupyter/apache/ApacheNGram-Experiment2.ipynb
    training_data = getTrainingData(path)
    unique_url_map = replacePathWithID(training_data)
    ngram_as_path = findNgrams(nGramLength)
    distance_matrix = calculateDistanceMatrix(ngram_as_path)
    cluster_options = calculateClusterOptions()
    preparePrediction()
    # evaluate options for prediction
    saveAgentData()
    return True

def preparePrediction():
    i = 20
    new_ngram = sample_n_gram_list_as_ids[i]
    my_eps = 2
    my_leaf_size = 30
    clustering = DBSCAN(algorithm='auto', eps=my_eps, leaf_size=my_leaf_size, metric='precomputed').fit_predict(
        distance_matrix)

def saveAgentData():
    saveData(distance_matrix,"distance_matrix.data")
    saveData(ngram_as_path,"ngram_as_path.data")
    pass

def saveData(data,filename):
    pickle.dump(data, open(data_root_path + "/" + filename, "wb"))

def predict(new_data, cluster, eps, metric, training_data):
    matching_clusters = []
    closest_cluster = -1
    for i in range (0, len(cluster)):
        distance = metric(new_data,training_data[i])
        if (distance <= eps):
            matching_clusters.append(clustering[i])
    return set(matching_clusters)


def calculateClusterOptions():
    my_leaf_size = 30

    X = []
    cluster_count_Y = []
    results = []
    for my_eps in range(1, 6):
        clustering = DBSCAN(algorithm='auto', eps=my_eps, leaf_size=my_leaf_size, metric='precomputed').fit(
            distance_matrix)
        cluster_count = clustering.labels_.max()
        X.append(my_eps)
        cluster_count_Y.append(cluster_count)
        results.append([my_eps, cluster_count])
    print("Cluster options:")
    print(results)
    return results

def calculateDistanceMatrix(ngram_as_path):
    sample_n_gram_list_as_ids = n_gram_list_to_ids(ngram_as_path)
    return pairwise_distances(sample_n_gram_list_as_ids, metric=get_levenshtein_distance)

def findNgrams (n):
    # Sort unique users by number of requests made to the web server
    visitor_addresses = training_data.host
    histogram_visitor_address = visitor_addresses.value_counts()

    # start with empty n-gram list
    ith_most_active_user_path_n_gram = list()

    for row in histogram_visitor_address.iteritems():
        visitor = row[0]
        # print(visitor)
        # get just the entries from the second most active user
        ith_most_active_user_logs = training_data.loc[training_data['host'] == visitor]
        # get a list of just the URLs for that user
        ith_most_active_user_path = ith_most_active_user_logs['url']

        # create n-gram for graph
        ith_most_active_user_path_n_gram.extend(list(find_ngrams(ith_most_active_user_path, n)))

        # remove duplicates
        ith_most_active_user_path_n_gram.sort()
        ith_most_active_user_path_n_gram = list(
            ith_most_active_user_path_n_gram for ith_most_active_user_path_n_gram, _ in
            itertools.groupby(ith_most_active_user_path_n_gram))

    print("First 3 n-grams :\n", ith_most_active_user_path_n_gram[:3])
    return ith_most_active_user_path_n_gram

def getTrainingData(path):
    training_data_path = 'rawData/nasa_19950801.tsv'
    return pd.read_csv(training_data_path, sep='\t', header=0)

# functions to convert to/from id and url
def get_id_from_url(url):
    return unique_url_map.index[unique_url_map['url'] == url][0]

def get_url_from_id(id):
    return unique_url_map.loc[id,'url']

def replacePathWithID(training_data):
    # get list of unique urls to get unique id.
    unique_urls_as_set = set(training_data['url'])
    unique_urls_as_list = list(unique_urls_as_set)
    unique_urls_as_array = np.array(unique_urls_as_list)
    return pd.DataFrame(unique_urls_as_array, columns={"url"})

#convert n-gram from urls to ids
def n_gram_to_id (n_gram_of_urls):
    n_gram_of_ids = list(n_gram_of_urls)
    for i in range(0, len(n_gram_of_urls)):
        n_gram_of_ids[i] = get_id_from_url(n_gram_of_urls[i])
    return n_gram_of_ids

#convert n-grams from ids to urls
def n_gram_to_url (n_gram_of_ids):
    n_gram_of_urls = list(n_gram_of_ids)
    for i in range(0, len(n_gram_of_ids)):
        n_gram_of_urls[i] = get_url_from_id(n_gram_of_ids[i])
    return n_gram_of_urls

#convert list of n-grams from urls to ids
def n_gram_list_to_ids (n_gram_list_of_urls):
    n_gram_list_of_ids = list(n_gram_list_of_urls)
    for i in range(0, len(n_gram_list_of_urls)):
        n_gram_list_of_ids[i] = n_gram_to_id(n_gram_list_of_urls[i])
    return n_gram_list_of_ids

#convert list of n-grams from ids to urls
def n_gram_list_to_urls (n_gram_list_of_ids):
    n_gram_list_of_urls = list(n_gram_list_of_ids)
    for i in range(0, len(n_gram_list_of_ids)):
        n_gram_list_of_urls[i] = n_gram_to_url(n_gram_list_of_ids[i])
    return n_gram_list_of_urls

#should unwind this a bit to make the purpose more clear
#also, there should be padding added to the front/back to indicate beginning and ending of a path
def find_ngrams(input_list, n):
  return [list(x) for x in set(tuple(x) for x in list(zip(*[input_list[i:] for i in range(n)])))]


def sanityCheckPath(path):
    isValidTrainingDir = os.access(path+trainingDir, os.R_OK)
    print("Is Training Directory  " + path + trainingDir + " valid? " + str(isValidTrainingDir))
    isValidTestDataDir = os.access(path+testDataDir, os.R_OK)
    print("Is Test Data Directory " + path + testDataDir + " valid? " + str(isValidTrainingDir))
    return isValidTrainingDir and isValidTestDataDir

def get_levenshtein_distance(path1, path2):
    """
    https://en.wikipedia.org/wiki/Levenshtein_distance
    :param path1:
    :param path2:
    :return:
    """
    matrix = [[0 for x in range(len(path2) + 1)] for x in range(len(path1) + 1)]

    for x in range(len(path1) + 1):
        matrix[x][0] = x
    for y in range(len(path2) + 1):
        matrix[0][y] = y

    for x in range(1, len(path1) + 1):
        for y in range(1, len(path2) + 1):
            if path1[x - 1] == path2[y - 1]:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1],
                    matrix[x][y - 1] + 1
                )
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1] + 1,
                    matrix[x][y - 1] + 1
                )

    return matrix[len(path1)][len(path2)]

if __name__ == '__main__':
    train(sys.argv[1])
