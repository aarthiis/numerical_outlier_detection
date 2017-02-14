
import get_data as gd
import numpy as np
from sklearn import mixture

def get_all_types(ordered_entities):
    """This function will get all the types related with a URI.
        The arguments are:
        ordered_entities: This is a list containing all the entities whose 
        types have to be extracted"
        
        It will return the following two things:
        entity_type : A dictionary which has list of each entity and types
            associated with it.
        all_types: A dictionary having all the types, with its value as the number of times
        it has occured.
    """
    all_types = {}
    entity_type = {}
    for each in ordered_entities:
        entity_type_each_list = []
        results = gd.get_types("<" + each + ">")['results']['bindings']
        for each_type in results:
            _type = each_type['concept']['value']
            if _type not in all_types:
                all_types[_type] = 0
            all_types[_type]+=1
            entity_type_each_list.append(_type)
        entity_type[each] = entity_type_each_list
    return (entity_type, all_types)
    
def discard_p(all_types, total_entities, p = 0.05):
    """This function is used to decide the top p%
    and the (1-p)% types which will be discarded."""
    discard = {}
    for each in all_types:
        if (all_types[each]/total_entities)>=(1-p) or (all_types[each]/total_entities)<=p:
            discard[each] = 1
    return discard

def feature_index_map(all_types, discards):
    """This function generates a feature Index Map:
    It maps every feature with an index of an array
    The arguments are 
    all_types : Which is a dictionary having all the types as keys, and the 
    times they have occured as values.
    discards : is a dictionary of the types, which will be 
    discarded due to being very common or very rare.
    
    Returns a dictionary which has the types as its key and the index as 
    its corresponding value.
    """
    features_index_map_d = {}
    index = 0
    for each in all_types:
        if each not in discards:
            features_index_map_d[each] = index
            index+=1      
    return features_index_map_d
    
def prepare_dataset(ordered_entities, p = 0.05):
    entity_type, all_types = get_all_types(ordered_entities)
    discards = discard_p(all_types, len(all_types), p)
    feature_map = feature_index_map(all_types, discards)
    data_feature = np.zeros(shape = (len(ordered_entities), len(feature_map)), dtype = int)
    print(feature_map)
    for i in range(len(ordered_entities)):
        for j in entity_type[ordered_entities[i]]:
            try:
                data_feature[i][feature_map[j]] = 1
            except Exception as e:
                pass
                #print("Feature Removed Because of p constraints")
    return data_feature
    
def find_best_gmm(X,n = 7):
    """This function attempt to find the best GMM for a 
    given dataset. It tries to find the best no of clusters
    and the different cv_types
    The arguments are:
    1. X which is the dataset
    2. n which is the number of clusters upto which it needs to check"""
    
    lowest_bic = np.infty
    bic = []
    n_components_range = range(1, n)
    cv_types = ['spherical', 'tied', 'diag', 'full']
    for cv_type in cv_types:
        for n_components in n_components_range:
            # Fit a Gaussian mixture with EM
            gmm = mixture.GaussianMixture(n_components=n_components,
                                          covariance_type=cv_type)
            gmm.fit(X)
            bic.append(gmm.bic(X))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm
    return best_gmm


def cluster(ordered_entities, p =0.05):
    """This is the final function which is used to cluster"""
    ds = prepare_dataset(ordered_entities, p = p)
    best_gmm = find_best_gmm(ds, 10)
    return best_gmm.predict(ds)
