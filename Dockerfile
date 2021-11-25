FROM python:3.9-buster

WORKDIR /app

# RUN apt upgrade -y && apt update -y && apt install libsodium-dev libsecp256k1-dev libgmp-dev

RUN apt-get update && apt-get install -y \
  libgmp-dev \
  libsecp256k1-dev \
  libsodium-dev \
  && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV PATH "$PATH:/app/execs"
ENV TEZOS_CLIENT_UNSAFE_DISABLE_DISCLAIMER yes

COPY execs .
COPY validators .

CMD ["python", "validators/validator.py"]