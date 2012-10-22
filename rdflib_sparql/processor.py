
"""
Code for tying SPARQL Engine into RDFLib

These should be automatically registered with RDFLib 

"""


from rdflib.query import Processor, Result

from rdflib_sparql.sparql import Query
from rdflib_sparql.parser import parseQuery
from rdflib_sparql.evaluate import evalQuery
from rdflib_sparql.algebra import translateQuery

class SPARQLResult(Result):
    
    def __init__(self, res): 
        Result.__init__(self,res["type_"])
        self.vars=res.get("vars_")
        self.bindings=res.get("bindings")
        self.askAnswer=res.get("askAnswer")
        self.graph=res.get("graph")


class SPARQLProcessor(Processor): 

    def __init__(self, graph):
        self.graph=graph

    def query(self, strOrQuery, initBindings={}, initNs={}, base=None, DEBUG=False):
        """
        Evaluate a query with the given initial bindings, and initial namespaces
        The given base is used to resolve relative URIs in the query and 
        will be overridden by any BASE given in the query
        """
        
        if not isinstance(strOrQuery, Query):
            parsetree=parseQuery(strOrQuery)
            query=translateQuery(parsetree,base)
        else: 
            query=strOrQuery
        
        return evalQuery(self.graph, query, initBindings, initNs, base)
        
