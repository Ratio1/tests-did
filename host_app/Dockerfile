FROM docker:dind

# add python
RUN apk add --no-cache python3 py3-pip

WORKDIR /app

COPY main.py .

CMD ["python3", "main.py"]
