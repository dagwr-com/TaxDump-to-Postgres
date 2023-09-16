# Use the official PostgreSQL image from the Docker Hub
FROM postgres:latest

# Install Python3 and pip
RUN apt-get update && \
  apt-get install -y python3 python3-pip python3-venv wget && \
  python3 -m venv /opt/venv && \
  . /opt/venv/bin/activate && \
  pip install --no-cache-dir biopython

# Download and set up the BioSQL schema
RUN wget https://raw.githubusercontent.com/biosql/biosql/master/sql/biosqldb-pg.sql -O /docker-entrypoint-initdb.d/biosqldb-pg.sql

# Set environment variables for PostgreSQL (change these to your liking)
ENV POSTGRES_DB=biosql
ENV POSTGRES_USER=biosqluser
ENV POSTGRES_PASSWORD=biosqlpass

# Add a script to download a GenBank file and load it into the BioSQL database
# Copy the data loading script into the container
COPY load_data.py /docker-entrypoint-initdb.d/load_data.py

# Make the script executable and run it after the database is initialized
RUN chmod +x /docker-entrypoint-initdb.d/load_data.py
CMD ["python3", "/docker-entrypoint-initdb.d/load_data.py"]