import numpy as np
import get_data as gd


def iqr(data, upper, lower):
    if lower>upper:
        lower, upper = upper, lower
    qUpper, qLower = np.percentile(data, [upper,lower])
    return qUpper - qLower

def find_outliers_using_MAD(data, multiplyingFactor=1, preprocess = False, clusters = None):
    """This function is used to find outliers using the Median Absolute Dispersion
    
        The arguments are
        data: The numpy array in which we want to find the outliers.        
        multiplyingFactor : This is the multiplying factor        
        preprocess : This is a boolean which sets the \
                                        options to enable preprocessing
        clusters : The clusters which are provided if preprocess \
                                            is set to true (numpy array)
    
        The function returns a numpy array which contains the indices of the numpy \
                    array, which are outliers.

    """
    if preprocess and clusters is not None:
        no_of_clusters = np.maximum(clusters) + 1
        indices = np.empty(shape=(0,1))
        for i in range(no_of_clusters):
            data_cluster_i = data[clusters==i]
            median = np.median(data_cluster_i)
            MAD = np.median(np.abs(data - median))
            indices = np.concatenate((np.where(np.abs(data_cluster_i-median)>=\
                                        (multiplyingFactor*MAD)), indices), axis=0)
        return indices
    else:
        median = np.median(data)
        MAD = np.median(np.abs(data - median))
        return np.where(np.abs(data-median)>=(multiplyingFactor*MAD))
        
def find_outliers_using_IQR(data, upper = 75, lower = 25, multiplyingFactor = 1.5, \
                                              preprocess = False, clusters = None):
    """The function is used to find outliers from a given numpy array.


        The arguments are 
        data: The numpy array in which we want to find the outliers.
        upper: The higher percentile value to calculate the IQR
        lower: The lower percentile value to calculate the IQR
        multiplyingFactor: This is the multiplying factor for the IQR
        preprocess : This is a boolean which sets the \
                                        options to enable preprocessing
        clusters : The clusters which are provided if preprocess \
                                            is set to true (numpy array)
        The function returns a numpy array which contains the indices of the numpy \
                    array, which are outliers.
    """
    if lower>upper:
        lower, upper = upper, lower


    if preprocess and clusters is not None:
        no_of_clusters = np.maximum(clusters) + 1
        indices = np.empty(shape=(0,1))
        for i in range(no_of_clusters):
            data_cluster_i = data[clusters==i]
            qUpper, qLower = np.percentile(data_cluster_i, [upper,lower])
            iqrFactored = multiplyingFactor*(qUpper-qLower)
            indices = np.concatenate((np.where((data_cluster_i<(qLower-iqrFactored)) | \
                        (data_cluster_i>(qUpper+iqrFactored))), indices), axis = 0)
            return indices
    else:
        qUpper, qLower = np.percentile(data, [upper,lower])
        iqrFactored = multiplyingFactor*(qUpper-qLower)
        return np.where((data<(qLower-iqrFactored)) | (data>(qUpper+iqrFactored)))
    
def statistics(data):
    """This function prints the following statistics
        mean, median, minimum, maximum"""
    print("mean = ", np.mean(data))
    print("median = ", np.median(data))
    print("minimum value = ", data.min())
    print("maximum value = ", data.max())

def gauss(x, mu, sigma):
    return (1/sigma*(np.sqrt(2*np.pi)))*np.exp((-1/(2*sigma*sigma))*((x-mu)**2))

def KDE(x, h = None, threshold = 1, preprocess = False, clusters = None):
    """The function is used to find the outliers using
    the Kernel Density Estimation Technique"""
    if h is None:
        h = (((4*(sigma**5))/(3*n))**0.2)

    if preprocess and clusters is not None:
        indices = np.empty(shape=(0,1))
        no_of_clusters = np.maximum(clusters) + 1
        for i in range(no_of_clusters):
            data_cluster_i = x[clusters==i]
            n = data_cluster_i.size
            fnh = np.zeros(n)
            mu = np.mean(data_cluster_i)
            sigma = np.std(data_cluster_i)

           
            for i in range(data_cluster_i.size):
                fnh[i] = np.sum(gauss((data_cluster_i-data_cluster_i[i])/h, \
                                mu, sigma))/(n*h)
            
            normalizing = np.sum(fnh)/n
            fnh = fnh/normalizing
            indices = np.concatenate((indices, np.where(fnh<threshold)), axis = 0)
        return indices
    else:
        n = x.size
        fnh = np.zeros(n)
        mu = np.mean(x)
        sigma = np.std(x)

       
        for i in range(x.size):
            fnh[i] = np.sum(gauss((x-x[i])/h, mu, sigma))/(n*h)
        
        normalizing = np.sum(fnh)/n
        fnh = fnh/normalizing
        return np.where(fnh<threshold)
    
      

    
def get_data(argument):
    """This function would be used to access data from DBPedia"""
    print("Fetching data from DBPedia SPARQL endpoint")    
    if argument.lower() == 'city':
        return gd.get_city_population()
    elif argument.lower() == 'country':
        return gd.get_country_population()
    print("Data fetched")
    
def print_entities_from_index(list_of_entities, index):
    """ This function will print the details given the indices.
        The arguments to the function are
        list_of_entities : A list containing the URI entities."""
    for i in index:
        print(list_of_entities[i])


def find_overlap_between_multiple_arrays(array_a, array_b, *argv):
    """ This function gives the elements which are common to
        both (and additional ) arrays.
        The arguments of the function are:
            array_a : This is the first array
            array_b : This is the second array
            argv : Variable arguments
    """
    answer = np.intersect1d(array_a, array_b)
    for arg in argv:
        answer = np.intersect1d(answer, arg)
    
    return answer

if __name__=="__main__":
    print("*"*80)
    #Applying the numerical methods on cities
    city_name_populations = get_data('City') 
    data = np.asarray(city_name_populations[0])
    print("No of datapoints", data.size)
    IQR_outliers = find_outliers_using_IQR(data, upper = 95, lower = 5)[0]
    MAD_outliers = find_outliers_using_MAD(data)[0]
    KDE_outliers = KDE(data)[0]
    statistics(data)    
    print("Number of outliers using IQR = ", len(IQR_outliers))
    print("Number of outliers using MAD = ", len(MAD_outliers))
    print("Number of outliers using KDE = ", len(KDE_outliers))
    overlap = find_overlap_between_multiple_arrays(IQR_outliers, MAD_outliers, KDE_outliers)
    print("Number of outliers using common to IQR, MAD and KDE = ", len(overlap))
    print_entities_from_index(city_name_populations[1], overlap)


    print("*"*80)

    #Applying the numerical methods on coutries
    country_name_populations = get_data('Country') 
    data = np.asarray(country_name_populations[0])
    print("No of datapoints", data.size)
    IQR_outliers = find_outliers_using_IQR(data, upper = 95, lower = 5)[0]
    MAD_outliers = find_outliers_using_MAD(data)[0]
    KDE_outliers = KDE(data)[0]
    statistics(data)    
    print("Number of outliers using IQR = ", len(IQR_outliers))
    print("Number of outliers using MAD = ", len(MAD_outliers))
    print("Number of outliers using KDE = ", len(KDE_outliers))
    overlap = find_overlap_between_multiple_arrays(IQR_outliers, MAD_outliers, KDE_outliers)
    print("Number of outliers using common to IQR, MAD and KDE = ", len(overlap))
    print_entities_from_index(country_name_populations[1], overlap)
