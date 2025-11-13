# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# This includes the tv_organizer package, pyproject.toml, README, etc.
COPY . .

# Install the package. The '.' refers to the current directory, where pyproject.toml is located.
# This command will install the 'tv-organizer' script into the container's PATH.
RUN pip install .

# Set the entrypoint for the container to be the installed script.
# This allows running the container as an executable.
# e.g., docker run <imagename> --gui
# e.g., docker run <imagename> /path/to/data --dry-run
ENTRYPOINT ["tv-organizer"]
