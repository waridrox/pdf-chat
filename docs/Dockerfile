# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Set the working directory in the container
WORKDIR /docs_src

# Copy the MkDocs configuration file from the build context (docs directory) to the working directory
COPY mkdocs.yml mkdocs.yml

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the documentation content (markdown files, etc.) from the build context
# The build context is 'docs', so '.' copies everything in 'docs' into WORKDIR/ (e.g. /docs_src/index.md)
COPY . .

# Expose port 8001 for MkDocs
EXPOSE 8001

# Run mkdocs when the container launches
# mkdocs.yml is in the WORKDIR, and markdown files are also in WORKDIR
# The -f flag should point to mkdocs.yml in the WORKDIR.
# The docs themselves will be served from the WORKDIR.
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8001", "-f", "mkdocs.yml"]
