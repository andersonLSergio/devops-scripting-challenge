FROM python:3.6

ENV PYTHONBUFFERED 1

WORKDIR /usr/src/app

RUN echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list
RUN apt-get -yqq update && \
    apt-get -yqq --no-install-recommends install openjdk-8-jdk-headless \
      maven \
      zip && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

# ADD env env
ADD requirements.txt .
ADD ./src/*.py ./

# Activate existing Python Virtual Env
# ENV VIRTUAL_ENV=/usr/src/app/env
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt \
    && find . -type f -name "*.pyc" -delete || true