FROM python:3.8

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# for dev
ENV PYTHONDONTWRITEBYTECODE 1

# Application ENV
ENV PORT '80'

# Install dependencies
RUN apt-get update && apt-get install -y vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#RUN pip3 install Flask
RUN pip3 install pipenv

# Create the application directory
RUN set -ex && mkdir -p /app
WORKDIR /app

# Adding Pipfiles
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

# Install dependencies
RUN pipenv install --deploy --system

EXPOSE 80
CMD ["/bin/bash"]

