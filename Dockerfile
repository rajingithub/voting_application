# official python3.10 as base image
FROM python:3.10

# create a directory(/app) in new created container
WORKDIR /app

# copy the requirements.txt file inside the container. This step is done first bcs
# requirements changes are very less. In docker if any particular layer changes all
# the below layers will be created again, if requirements.txt is copied later layers
# if above layer is changed, the requirements will be downloaded again
COPY requirements.txt /app/

# Installing Dependencies for the application
RUN pip install --no-cache-dir -r requirements.txt

# copy the code to the container
COPY . /app/

# creating volume for database(sqlite only) bcs DB should be persistent across
# containers. data should not be removed if we restart or create new container
# these volume is shared by all the containers.
VOLUME /app

# Run the initial DB migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port 8000 of the container
EXPOSE 8000

# Run Django application when continer starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


## To create the Image
# sudo docker build -t voting_app1 .

## once Image is build, to start the container use the below command.
# port => host port : container port(container port need to be exposed as above EXPOSE command)
# -d is to run in the background
# sudo docker run -d -p 80:8000 voting_app1







