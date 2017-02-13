import numpy as np


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
    print(qLower-iqrFactored, qUpper+iqrFactored)
    return np.where((data<(qLower-iqrFactored)) | (data>(qUpper+iqrFactored)))
    

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
    
      

    
def get_data():
    """This function would be used to access data from DBPedia"""
    pass    


if __name__=="__main__":
    data = np.random.rand(100000)
    #print(iqr(data, 95, 5))
    #print(iqr(data, 5, 95))
    print(data[find_outliers_using_IQR(data, 75, 50, 1.5)].size)
    print(data[find_outliers_using_MAD(data)].size)
    print(data[KDE(data)].size) 
