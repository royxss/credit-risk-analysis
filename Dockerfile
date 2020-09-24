###########################################
#           Install Backend 
###########################################
# Using official python runtime base image
FROM nikolaik/python-nodejs:python3.7-nodejs10-stretch

# Label
LABEL maintainer="Roy Subhadeep <findroy@outlook.in>"

# Upgrade pip
RUN pip install --upgrade pip

# Set the application directory
WORKDIR /app

# Install our requirements.txt
ADD requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -U pip
RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
COPY . ./

###########################################
#           Install Frontend 
###########################################

# set working directory
WORKDIR /app/react-apps

# install app dependencies
RUN npm install

#CMD ["npm", "start"]
RUN npm run build

###########################################
#           Finally 
###########################################

# Entry point
WORKDIR /app
EXPOSE 9090
RUN chmod 775 ./development_use_start_server.sh
CMD ["./development_use_start_server.sh"]

###########################################
#           try if frontend is working. Comment lines 43-46 
###########################################
#WORKDIR /app/react-apps
#EXPOSE 3000
#CMD ["npm", "start"]