## Credit Risk Analysis App

### Demo

![Alt Text](./demo.gif)

### Start Application using Docker:

#### Note: There is no compose here as it is just one container.

- docker build -t creditriskapp .
- docker run -d -p 9090:9090 creditriskapp:latest

#### Test only front-end?

- docker build -t frontend .
- docker run -it -p 3000:3000 frontend:latest
