## Description:

This application performs credit risk analysis using machine learning and identifies customers who are most likely to default on their payment next month.

## How to start the application:

#### Use docker container to start the application from the folder where Dockerfile exists. _Note: Please make sure docker is installed in your machine_

- git pull
- docker stop \$(docker ps -q --filter ancestor=credit-risk-app-monolith) # if already running
- docker build -t credit-risk-app-monolith .
- docker run --rm -d -p 9090:9090 credit-risk-app-monolith

#### Test only front-end?

- docker build -t frontend .
- docker run -it -p 3000:3000 frontend:latest

#### Open browser using `http://0.0.0.0:9090/dashboard/`

![Alt Text](./demo.gif)
