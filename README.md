# numerical_outlier_detection
This code in this repository implements the paper *Detecting Incorrect Numerical Data in DBpedia* by Dominik Wienand and Heiko Paulheim.

##Requirements
To install the requirements
```bash
pip3 install -r requirements.txt
```

## Execution

To run the code, 
```bash

python3 main.py
```

## Data 

The _data_ directory has the outliers stored for the queries which have been run.

The _data_ directory has sub-directories, where each folder is for a query which has been run.
The _country_ sub-directory has the outliers calculated using different methods in different files. There is a file (country.parsing_exception) which has the list of the countries, whose populations are not an integer (we expect the population to be an integer).

