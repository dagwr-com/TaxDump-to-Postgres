#!/usr/bin/env python3
import time
from BioSQL import BioSeqDatabase
from Bio import SeqIO
import urllib.request
import gzip

# Wait for the PostgreSQL server to start
time.sleep(10)

# Download a sample GenBank file from NCBI
urllib.request.urlretrieve('https://ftp.ncbi.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.gbff.gz', 'data.gbff.gz')

# Create a connection to the BioSQL database
server = BioSeqDatabase.open_database(driver='psycopg2', user='biosqluser', passwd='biosqlpass', host='localhost', db='biosql')

# Create a new BioSQL namespace
db = server.new_database('my_namespace')

# Load data from the GenBank file into the BioSQL database
with gzip.open('data.gbff.gz', 'rt') as input_handle:
    count = db.load(SeqIO.parse(input_handle, 'genbank'))
print(f'Loaded {count} records')
