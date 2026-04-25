# start from a base image having python already installed
FROM python:3.11-slim

#set the working directory inside the container
WORKDIR /app


#copy the dependencies file to the working directory
COPY requirements.txt .

#install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy the content of the local src directory to the working directory   
COPY app.py  .

#Expose the port
EXPOSE 5000

#run the application
CMD ["python", "app.py"]