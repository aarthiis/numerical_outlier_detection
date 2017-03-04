from SPARQLWrapper import SPARQLWrapper, JSON

def get_company_count():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    country_pops = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX yago:<http://dbpedia.org/class/yago/>

    SELECT (COUNT(?company_name) as ?count)
    WHERE {
        ?company_name a dbo:Company .
        ?company_name dbo:numberOfEmployees ?population
    }
        """
    sparql.setQuery(country_pops)  # the previous query as a literal string

    results = sparql.query().convert()
    return int(results['results']['bindings'][0]['count']['value'])

    

def get_company_population(parsing_exception_file):
    total_companies = get_company_count()
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    ordered_pop = []
    ordered_name = []
    parsing_error = {}

    for j in range(total_companies//10000 + 1):
        country_pops = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX : <http://dbpedia.org/resource/>
        PREFIX dbpedia2: <http://dbpedia.org/property/>
        PREFIX dbpedia: <http://dbpedia.org/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX yago:<http://dbpedia.org/class/yago/>

        SELECT ?company_name ?company_population
        WHERE {
            ?company_name a dbo:Company .
            ?company_name dbo:numberOfEmployees ?company_population
        } 
            ORDER BY ?company_name
            OFFSET %d
            """ %(j*10000)
        sparql.setQuery(country_pops)  # the previous query as a literal string

        results = sparql.query().convert()
        spo_triples = results['results']['bindings']
        for each in spo_triples:
            try:
                company_name = each['company_name']['value']
                pop = int(each['company_population']['value'])
                ordered_name.append(company_name)
                ordered_pop.append(pop)
            except Exception as e:
                parsing_error[company_name] = each['company_population']['value']
                pass

    #Writing all the values which were not parsed properly to a file    
    if len(parsing_error)!=0:
        f = open(parsing_exception_file, "w")
        for each in parsing_error:
            f.write(each + ":" + parsing_error[each] + "\n")
        f.close()
        
        
    return (ordered_pop, ordered_name)



def get_types(entity_URI):
    query ="""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX yago:<http://dbpedia.org/class/yago/>

    SELECT DISTINCT ?concept
    WHERE {
        %s a ?concept .
    }
    """ % (entity_URI)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)  # the previous query as a literal string
    return sparql.query().convert()

def get_country_population(parsing_exception_file):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    

    country_pops = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX yago:<http://dbpedia.org/class/yago/>

    SELECT ?country_name ?population
    WHERE {
        ?country_name a dbo:Country .
        ?country_name a yago:WikicatCountries .
        
        ?country_name dbpedia2:populationEstimate ?population . 
    }
    """
    sparql.setQuery(country_pops)  # the previous query as a literal string

    results = sparql.query().convert()
    spo_triples = results['results']['bindings']
    ordered_pop = []
    ordered_name = []
    parsing_error = {}
    for each in spo_triples:
        try:
            country_name = each['country_name']['value']
            pop = int(each['population']['value'])
            ordered_name.append(country_name)
            ordered_pop.append(pop)
        except Exception as e:
            parsing_error[country_name] = each['population']['value']
            pass

    #Writing all the values which were not parsed properly to a file    
    if len(parsing_error)!=0:
        f = open(parsing_exception_file, "w")
        for each in parsing_error:
            f.write(each + ":" + parsing_error[each] + "\n")
        f.close()
        
        
    return (ordered_pop, ordered_name)



def get_city_population(parsing_exception_file):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)


    city_pops = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX yago:<http://dbpedia.org/class/yago/>

    SELECT ?city_name ?enName ?population
    WHERE {
        ?city_name a dbo:City .
        OPTIONAL { ?city_name dbo:populationTotal ?population . }
    }
    """
    sparql.setQuery(city_pops)  # the previous query as a literal string

    results = sparql.query().convert()
    spo_triples = results['results']['bindings']
    ordered_pop = []
    ordered_name = []
    parsing_error = {}
    for each in spo_triples:
        try:
            city_name = each['city_name']['value']
            pop = int(each['population']['value'])
            ordered_name.append(city_name)
            ordered_pop.append(pop)
        except Exception as e:
            parsing_error[country_name] = each['population']['value']



    #Writing all the values which were not parsed properly to a file    
    if len(parsing_error)!=0:
        f = open(parsing_exception_file, "w")
        for each in parsing_error:
            f.write(each + ":" + parsing_error[each] + "\n")
        f.close() 
    return (ordered_pop, ordered_name)
"""
if __name__=="__main__":
    Z = get_city_population()
    print(Z)
    print(len(Z[0]), len(Z[1]))
"""
