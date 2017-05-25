#
#summary script:
#
# sys.argv[1] = outdir
# sys.argv[2] = fmifundation_alteration_file

# >> This script is converting data downloaded from Foundation Medicine Pediatric Portal, into a ttl format.

import csv
import os
import re
import sys
import urllib

from rdfwriter import Graph, Literal, Namespace, RDF, URIRef

NSS = Namespace("http://ns.ontoforce.com/ontologies/sample/", "nss")
NSSC = Namespace("http://ns.ontoforce.com/ontologies/sample/classes/", "nssc")
NSV = Namespace("http://ns.ontoforce.com/ontologies/variant/", "nsv")
NSVC = Namespace("http://ns.ontoforce.com/ontologies/variant/classes/", "nsvc")

DISQ = Namespace("http://ns.ontoforce.com/2013/disqover#", "disq")
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#', "rdfs")


class Sample(object):

    def __init__(self):
        self.sampleId = None
        self.age = None
        self.assayVersion = None
        self.gender = None
        self.disease_combinaison = None
        self.disease_subtype = None
        self.disease = None

    def parse(self, entryline):
        self.sampleId = entryline['sampleId']
        self.age = entryline['age']
        self.assayVersion = entryline['assayVersion']
        self.disease_combinaison = clean_bracket("{} {}".format(entryline['diseaseSubType'], entryline['disease']))
        self.disease_subtype = clean_bracket(entryline['diseaseSubType'])
        self.disease = clean_bracket(entryline['disease'])
        if entryline['gender'] == "M":
            self.gender = "Male"
        if entryline['gender'] == "F":
            self.gender = "Female"

    def write_ttl(self, g):
        uri = URIRef("http://ns.ontoforce.com/foundtionmedicine_pediatricportal/sample/" + to_uri(self.sampleId))
        g.add((uri, RDF.type, NSSC['fmi_pp_sample']))
        g.add((uri, DISQ['preferredLabel'], (Literal("FMI Sample {}".format(self.sampleId)))))
        g.add((uri, RDFS['label'], (Literal("FMI Sample {}".format(self.sampleId)))))
        g.add((uri, NSS['at_sample_age'], Literal(self.age)))
        g.add((uri, NSS['at_sample_gender'], Literal(self.gender)))
        g.add((uri, NSS['assayVersion'], Literal(self.assayVersion)))
        diseaseuri = URIRef('http://ns.ontoforce.com/foundtionmedicine_pediatricportal/disease/' + to_uri(self.disease))
        g.add((diseaseuri, RDF.type, URIRef("http://ns.ontoforce.com/ontologies/integration_ontology#Disease")))
        g.add((diseaseuri, RDFS["label"], Literal(self.disease)))
        g.add((diseaseuri, DISQ["matchLabel"], Literal(self.disease)))
        g.add((uri, NSS['disease'], diseaseuri))
        diseasesubtypeuri = URIRef('http://ns.ontoforce.com/foundtionmedicine_pediatricportal/disease/' + to_uri(self.disease_subtype))
        g.add((diseasesubtypeuri, RDF.type, URIRef("http://ns.ontoforce.com/ontologies/integration_ontology#Disease")))
        g.add((diseasesubtypeuri, RDFS["label"], Literal(self.disease_subtype)))
        g.add((diseasesubtypeuri, DISQ["matchLabel"], Literal(self.disease_subtype)))
        g.add((uri, NSS['diseaseSubType'], diseasesubtypeuri))
        diseaseconburi = URIRef('http://ns.ontoforce.com/foundtionmedicine_pediatricportal/disease/' + to_uri(self.disease_combinaison))
        g.add((diseaseconburi, RDF.type, URIRef("http://ns.ontoforce.com/ontologies/integration_ontology#Disease")))
        g.add((diseaseconburi, RDFS["label"], Literal(self.disease_combinaison)))
        g.add((diseaseconburi, DISQ["matchLabel"], Literal(self.disease_combinaison)))
        g.add((uri, NSS['diseaseCombinaison'], diseaseconburi))


class Variant(object):

    def __init__(self):
        self.variant_type = None
        self.gene = None
        self.transcript = None
        self.variantClass = None
        self.proteinEffect = None
        self.codon = None
        self.position = None
        self.allele_frequency = None
        self.total_depth = None
        self.copy_number = None
        self.split_read_number = None
        self.chromosome = None
        self.sampleId = None

    def parse(self, entryline):
        self.variant_type = entryline['variantType']
        self.gene = entryline['gene']
        if entryline['transcript'] != "none":
            self.transcript = entryline['transcript']
        self.variantClass = entryline['variantClass'].capitalize()
        self.proteinEffect = entryline['proteinEffect']
        if entryline['codon']:
            self.codon = entryline['codon']
        self.position = entryline['position']
        infos = entryline['variantInfo'].split(";")
        for info in infos:
            if 'AF:' in info:
                self.allele_frequency = info.replace('AF:','').strip()
            if 'DP:' in info:
                self.total_depth = info.replace('DP:','').strip()
            if 'CN:' in info:
                self.copy_number = info.replace('CN:','').strip()
            if 'SR:' in info:
                self.split_read_number = info.replace('SR:','').strip()
        self.chromosome = entryline['position'].split(":")[0].replace('chr', '')
        self.sampleId = entryline['sampleId']

    def write_ttl(self, g):
        sample_uri = URIRef("http://ns.ontoforce.com/foundtionmedicine_pediatricportal/sample/" + to_uri(self.sampleId))
        uri = URIRef("http://ns.ontoforce.com/foundtionmedicine_pediatricportal/variant/" + to_uri("{}_prot:{}".format(self.position, self.proteinEffect)))
        g.add((uri, RDF.type, NSVC['fmi_pp_variant']))
        g.add((uri, RDFS['label'], (Literal("FMI Sample {}".format(self.sampleId)))))
        gene_uri = URIRef("http://identifiers.org/hgnc.symbol/" + to_uri(self.gene))
        g.add((uri, NSV['gene'], gene_uri))
        g.add((gene_uri, DISQ['inRemote'], Literal("public")))
        if self.transcript:
            transcript_uri = URIRef("http://identifiers.org/refseq/" + self.transcript)
            g.add((uri, NSV['transcript'], transcript_uri))
            g.add((transcript_uri, DISQ['inRemote'], Literal("public")))
        g.add((uri, NSV['variantClass'], Literal(self.variantClass)))
        g.add((uri, NSV['variantType'], Literal(self.variant_type)))
        g.add((uri, NSV['proteinEffect'], Literal(self.proteinEffect)))
        if self.codon:
            g.add((uri, NSV['codon'], Literal(self.codon)))
        g.add((uri, NSV['position'], Literal(self.position)))
        if self.allele_frequency:
            g.add((uri, NSV['alleleFrequency'], Literal(self.allele_frequency)))
        if self.total_depth:
            g.add((uri, NSV['totalDepth'], Literal(self.total_depth)))
        if self.copy_number:
            g.add((uri, NSV['copyNumber'], Literal(self.copy_number)))
        if self.split_read_number:
            g.add((uri, NSV['splitReadNumber'], Literal(self.split_read_number)))
        g.add((uri, NSV['chromosome'], Literal(self.chromosome)))
        g.add((sample_uri, NSS['identifiedVariant'], uri))


def clean_bracket(text):
    return re.sub("[\(].*?[\)]", "", text).strip()


def to_uri(literal, conserveCase=False):
    literal = literal.strip()
    if not conserveCase:
        literal = literal.lower()
    return urllib.quote_plus(re.sub(r'[;,./ ]', '_', literal).encode("utf-8"))


def main():
    outdir = sys.argv[1]
    data_file = sys.argv[2]
    filename = os.path.basename(os.path.splitext(data_file)[0])
    loc= os.path.join(outdir, filename)
    ttl = open(loc + ".ttl", "w")

    g = Graph(ttl)
    g.add(NSV)
    g.add(NSVC)
    g.add(NSS)
    g.add(NSSC)
    g.add(DISQ)
    g.add(RDFS)
    #For each entry (moleculartest[sample, assay, variant]), create the molecular test and related data, and add it to graph
    with open(data_file) as tsvfile:
        datatsv = csv.DictReader(tsvfile, delimiter=',')
        for row in datatsv:
            m = Sample()
            v = Variant()
            try:
                m.parse(row)
                v.parse(row)
            except:
                print ("Parsing {}".format(m.sampleId))
            try:
                m.write_ttl(g)
                v.write_ttl(g)
            except:
                print ("Writing {}".format(m.sampleId))

# Close file
    print "Finished conversion {}".format(data_file)
    g.serialize()
    ttl.close()

if __name__ == "__main__":
    main()
