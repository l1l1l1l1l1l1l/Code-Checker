FROM python:3.7.2-alpine3.8

RUN sed -i 's/http:\/\/dl-cdn.alpinelinux.org/https:\/\/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update

# Install dependence
RUN apk add --upgrade --no-cache git bash ruby ruby-rdoc

# Install hits-of-code
WORKDIR /
RUN gem install slop
RUN git clone https://github.com/KellyGithubID/hoc.git
WORKDIR /hoc
RUN gem build hoc.gemspec
RUN gem install --local hoc-1.0.snapshot.gem
