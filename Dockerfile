FROM amazonlinux:2

RUN yum install -y amazon-linux-extras

RUN amazon-linux-extras enable python3.8
RUN yum install -y python3.8

# RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

RUN curl -sL https://rpm.nodesource.com/setup_16.x | bash -

RUN yum install -y nodejs gcc-c++ make

RUN npm install -g serverless

WORKDIR /app

COPY ./*.json .

COPY ./*.lock .

RUN npm install

COPY ./modules ./modules

COPY ./*.py .

COPY ./*.txt .

COPY ./*.yml .

RUN sls package -p .serverless-docker