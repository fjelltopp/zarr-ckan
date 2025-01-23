import logging
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import Namespace, RDF, RDFS, DC, DCTERMS, DCAT, FOAF
from ckanext.dcat.profiles import RDFProfile

# WIP

# Additional namespaces we might need
ADMS = Namespace("http://www.w3.org/ns/adms#")
PROV = Namespace("http://www.w3.org/ns/prov#")
DQV = Namespace("http://www.w3.org/ns/dqv#")
DCT = Namespace("http://purl.org/dc/terms/")

log = logging.getLogger(__name__)


def add_fair_enhancements(g, dataset_dict, dataset_ref):
    # Identifier (DOI)
    if dataset_dict.get('doi'):
        # Check if it's a DOI
        if dataset_dict['doi'].startswith('10.'):
            g.add((dataset_ref, DCT.identifier, Literal(dataset_dict['identifier'])))
            g.add((dataset_ref, ADMS.identifier, Literal(dataset_dict['identifier'], datatype=URIRef("http://purl.org/spar/datacite/doi"))))
        else:
            # If it's not a DOI, treat it as a general identifier
            g.add((dataset_ref, DCT.identifier, Literal(dataset_dict['identifier'])))

    # Data Standard
    if dataset_dict.get('data_standard'):
        g.add((dataset_ref, DCT.conformsTo, Literal(dataset_dict['data_standard'])))

    # Provenance
    if dataset_dict.get('provenance'):
        provenance = BNode()
        g.add((dataset_ref, DCT.provenance, provenance))
        g.add((provenance, RDF.type, PROV.Entity))
        g.add((provenance, RDFS.label, Literal(dataset_dict['provenance'])))

    # Quality Indicator
    if dataset_dict.get('quality_indicator'):
        quality = BNode()
        g.add((dataset_ref, DQV.hasQualityMeasurement, quality))
        g.add((quality, RDF.type, DQV.QualityMeasurement))
        g.add((quality, SKOS.notation, Literal(dataset_dict['quality_indicator'])))

    # Preservation Statement
    if dataset_dict.get('preservation_statement'):
        g.add((dataset_ref, ADMS.status, Literal(dataset_dict['preservation_statement'])))

    return g


class DublinCoreDCATProfile(RDFProfile):
    """
    An RDF profile for Dublin Core metadata aligned with DCAT
    """

    name = 'dublin_core_dcat'

    def graph_from_dataset(self, dataset_dict, dataset_ref):
        g = self.g

        # Basic fields
        items = [
            ('title', DCT.title),
            ('notes', DCT.description),
            ('version', DCAT.version),
            ('issued', DCT.issued),
            ('modified', DCT.modified),
            ('creator', DCT.creator),
            ('contributor', DCT.contributor),
            ('rights', DCT.rights),
            ('source', DCT.source),
            ('language', DCT.language),
            ('type', DCT.type),
            ('relation', DCT.relation),
        ]
        for item in items:
            key, predicate = item
            if dataset_dict.get(key):
                if isinstance(dataset_dict[key], list):
                    for value in dataset_dict[key]:
                        g.add((dataset_ref, predicate, Literal(value)))
                else:
                    g.add((dataset_ref, predicate, Literal(dataset_dict[key])))
                log.debug(f"Added {key}: {dataset_dict[key]}")

        # Tags / Keywords
        for tag in dataset_dict.get('tags', []):
            g.add((dataset_ref, DCAT.keyword, Literal(tag['name'])))
            log.debug(f"Added keyword: {tag['name']}")

        # Publisher
        if dataset_dict.get('publisher_name'):
            publisher = BNode()
            g.add((dataset_ref, DCT.publisher, publisher))
            g.add((publisher, RDF.type, FOAF.Organization))
            g.add((publisher, FOAF.name, Literal(dataset_dict['publisher_name'])))
            log.debug(f"Added publisher: {dataset_dict['publisher_name']}")

        # Temporal
        if dataset_dict.get('temporal_coverage'):
            temporal = BNode()
            g.add((dataset_ref, DCT.temporal, temporal))
            g.add((temporal, RDF.type, DCT.PeriodOfTime))
            if isinstance(dataset_dict['temporal_coverage'], list):
                if len(dataset_dict['temporal_coverage']) > 0:
                    g.add((temporal, DCAT.startDate, Literal(dataset_dict['temporal_coverage'][0])))
                if len(dataset_dict['temporal_coverage']) > 1:
                    g.add((temporal, DCAT.endDate, Literal(dataset_dict['temporal_coverage'][1])))
            else:
                g.add((temporal, RDFS.label, Literal(dataset_dict['temporal_coverage'])))
            log.debug(f"Added temporal coverage: {dataset_dict['temporal_coverage']}")

        # Spatial
        if dataset_dict.get('spatial_coverage'):
            g.add((dataset_ref, DCT.spatial, Literal(dataset_dict['spatial_coverage'])))
            log.debug(f"Added spatial coverage: {dataset_dict['spatial_coverage']}")

        # Resources / Distributions
        for resource in dataset_dict.get('resources', []):
            resource_ref = URIRef(resource['url'])
            g.add((dataset_ref, DCAT.distribution, resource_ref))
            g.add((resource_ref, RDF.type, DCAT.Distribution))

            # Basic resource properties
            if resource.get('name'):
                g.add((resource_ref, DCT.title, Literal(resource['name'])))
            if resource.get('description'):
                g.add((resource_ref, DCT.description, Literal(resource['description'])))
            if resource.get('format'):
                g.add((resource_ref, DCT['format'], Literal(resource['format'])))

            # Additional resource properties
            if resource.get('issued'):
                g.add((resource_ref, DCT.issued, Literal(resource['issued'])))
            if resource.get('modified'):
                g.add((resource_ref, DCT.modified, Literal(resource['modified'])))
            if resource.get('license'):
                g.add((resource_ref, DCT.license, Literal(resource['license'])))

            # Access URL and Download URL
            g.add((resource_ref, DCAT.accessURL, URIRef(resource['url'])))
            if resource.get('download_url'):
                g.add((resource_ref, DCAT.downloadURL, URIRef(resource['download_url'])))

            # Byte Size
            if resource.get('size'):
                g.add((resource_ref, DCAT.byteSize, Literal(resource['size'])))

            # Media Type
            if resource.get('mimetype'):
                g.add((resource_ref, DCAT.mediaType, Literal(resource['mimetype'])))

            log.debug(f"Added distribution: {resource.get('name', 'Unnamed resource')}")

        log.debug(f"Finished processing dataset: {dataset_dict.get('name', 'Unnamed dataset')}")

        # Add FAIR enhancements
        g = add_fair_enhancements(g, dataset_dict, dataset_ref)
        return g

    def graph_from_catalog(self, catalog_dict, catalog_ref):
        g = self.g

        for item in [
            ('title', DCT.title),
            ('description', DCT.description),
        ]:
            if catalog_dict.get(item[0]):
                g.add((catalog_ref, item[1], Literal(catalog_dict[item[0]])))

        return g
