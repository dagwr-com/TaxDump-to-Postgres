# Use the official PostgreSQL image from the Docker Hub
FROM postgres:latest

# Install Python3 and pip
RUN apt-get update && \
  apt-get install -y python3 python3-pip wget && \
  pip3 install biopython

# Download and set up the BioSQL schema
RUN wget https://raw.githubusercontent.com/biosql/biosql/master/sql/biosqldb-pg.sql -O /docker-entrypoint-initdb.d/biosqldb-pg.sql

# Set environment variables for PostgreSQL (change these to your liking)
ENV POSTGRES_DB=biosql
ENV POSTGRES_USER=biosqluser
ENV POSTGRES_PASSWORD=biosqlpass

# Add a script to download a GenBank file and load it into the BioSQL database
RUN echo "import time\n\
  from BioSQL import BioSeqDatabase\n\
  from Bio import SeqIO\n\
  import urllib.request\n\
  \n\
  # Wait for the PostgreSQL server to start\n\
  time.sleep(10)\n\
  \n\
  # Download a sample GenBank file from NCBI\n\
  urllib.request.urlretrieve('https://ftp.ncbi.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.gbff.gz', 'data.gbff.gz')\n\
  \n\
  # Create a connection to the BioSQL database\n\
  server = BioSeqDatabase.open_database(driver='psycopg2', user='biosqluser', passwd='biosqlpass', host='localhost', db='biosql')\n\
  \n\
  # Create a new BioSQL namespace\n\
  db = server.new_database('my_namespace')\n\
  \n\
  # Load data from the GenBank file into the BioSQL database\n\
  with open('data.gbff.gz', 'rt') as input_handle:\n\
  count = db.load(SeqIO.parse(input_handle, 'genbank'))\n\
  print(f'Loaded {count} records')\n\
  " > /docker-entrypoint-initdb.d/load_data.py

# Make the script executable and run it after the database is initialized
RUN chmod +x /docker-entrypoint-initdb.d/load_data.py
CMD ["python3", "/docker-entrypoint-initdb.d/load_data.py"]
