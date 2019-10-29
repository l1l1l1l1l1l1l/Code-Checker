FROM python:3.7.2-alpine3.8

RUN sed -i 's/http:\/\/dl-cdn.alpinelinux.org/https:\/\/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update

# Install dependence
RUN apk add --upgrade --no-cache git bash ruby ruby-rdoc
RUN pip3 install gitpython
RUN pip3 install bandit
RUN pip3 install coverage

# Install hits-of-code
RUN gem install hoc

COPY . /app/Code-Checker
WORKDIR /app/Code-Checker
ENV PYTHONPATH "."
RUN chmod -R 777 ./test/coverage.sh
