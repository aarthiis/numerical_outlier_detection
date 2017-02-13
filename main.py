import numpy as np
import get_data as gd


def iqr(data, upper, lower):
    if lower>upper:
        lower, upper = upper, lower
    qUpper, qLower = np.percentile(data, [upper,lower])
    return qUpper - qLower

def find_outliers_using_MAD(data, multiplyingFactor=1):
    median = np.median(data)
    MAD = np.median(np.abs(data - median))
    return np.where(np.abs(data-median)>=(multiplyingFactor*MAD))
    
def find_outliers_using_IQR(data, upper = 75, lower = 25, multiplyingFactor = 1.5):
    """The function is used to find outliers from a given numpy array.


        The arguments are 
        data: The numpy array in which we want to find the outliers.
        upper: The higher percentile value to calculate the IQR
        lower: The lower percentile value to calculate the IQR
        multiplyingFactor: This is the multiplying factor for the IQR

        The function returns a numpy array which contains the indices of the numpy array, \
                            which are outliers.
    """
    if lower>upper:
        lower, upper = upper, lower
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

def KDE(x, h = None, threshold = 1):
    """The function is used to find the outliers using
    the Kernel Density Estimation Technique"""
    n = x.size
    fnh = np.zeros(n)
    mu = np.mean(x)
    sigma = np.std(x)
    if h is None:
        h = (((4*(sigma**5))/(3*n))**0.2)

   
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
    #data = np.random.rand(100)
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
