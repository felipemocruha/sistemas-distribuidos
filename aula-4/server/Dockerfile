FROM python:3.8-slim-buster

RUN apt update \
	&& apt install --no-install-recommends -y git build-essential libev-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip && mkdir /app

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]
