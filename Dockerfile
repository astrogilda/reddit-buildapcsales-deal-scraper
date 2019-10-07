FROM frolvlad/alpine-python3 

MAINTAINER Jonathan Weaver

ENV email="redacted"
ENV pass="redacted"

RUN apk update && apk upgrade && pip install praw
RUN mkdir /scripts

CMD python /scripts/deals.py

