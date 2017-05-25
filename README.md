# fmi-pediatrics-oncology
[![Gitter](https://badges.gitter.im/bioithackathons/project-3.svg)](https://gitter.im/bioithackathons/project-3)

A project developed in the Bio-IT FAIR Data Hackathon

## Self-evaluation
How well does FMI Pediatrics Oncology data align with FAIR data principles?  

For each of the 15 FAIR principles, rate your dataset before and after your hackathon work.  A rating of "1" is least FAIR; "5" is most FAIR.

### Findable
> F1. (meta)data are assigned a globally unique and persistent identifier
* Before: 1.
    * No, There is some reference to refseq identifier and gene symbol of hugo, but not globally unique and persistent identifiers. Diseases are references as name
* After:4 
    * Mapping has been done on disease to UMLS instances, by matching disease name. The references to transcripts and gene have been transfored to global identifiers.
      Samples and Variants have local unique identifier

> F2. data are described with rich metadata (defined by R1 below)
* Before: 1
    * No
* After: 3
    We added a description, the source, the typed of the instances.. to the data

> F3. metadata clearly and explicitly include the identifier of the data it describes
* Before: 1
    * No
* After:4

> F4. (meta)data are registered or indexed in a searchable resource
* Before: 1
    * No
* After:5
    * The data and meta data are avaible through disqover platform. 

### Accessible
> A1. (meta)data are retrievable by their identifier using a standardized communications protocol
* Before: 1
    * No
* After:4
    * Data and meta data could be retrieve through API

> A1.1 the protocol is open, free, and universally implementable
* Before: 1
    * No
* After:5

> A1.2 the protocol allows for an authentication and authorization procedure, where necessary
* Before: 1
    * No
* After:5

> A2. metadata are accessible, even when the data are no longer available
* Before: 1
    * No
* After:1

### Interoperable
> I1. (meta)data use a formal, accessible, shared, and broadly applicable language for knowledge representation.
* Before: 3
    * Yes
* After:4

> I2. (meta)data use vocabularies that follow FAIR principles
* Before: 2
    * No
* After:4

> I3. (meta)data include qualified references to other (meta)data
* Before: 3
    * There is some references to other data (e.g refseq, but no for all e.g. disease has no qualified reference to other dataset)
* After:4


### Reusable
> R1. meta(data) are richly described with a plurality of accurate and relevant attributes
* Before: 3
* After: 5

> R1.1. (meta)data are released with a clear and accessible data usage license
* Before: 4
    * When logging to the portal, to access download file, there is an authentication with license information
* After: 4

> R1.2. (meta)data are associated with detailed provenance
* Before: 4
* After:5

> R1.3. (meta)data meet domain-relevant community standards
* Before: 3
    * variant representation, with allele details is not provided. Public references to variant (eg. dnpsnp,....) might have been provided
* After:4
