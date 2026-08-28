FROM debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        file \
        git \
        strace \
        time \
        xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L https://c9x.me/compile/release/qbe-1.3.tar.xz -o /tmp/qbe-1.3.tar.xz \
    && echo "d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320  /tmp/qbe-1.3.tar.xz" | sha256sum --check \
    && tar -C /tmp -xf /tmp/qbe-1.3.tar.xz \
    && make -C /tmp/qbe-1.3 \
    && install -m 0755 /tmp/qbe-1.3/qbe /usr/local/bin/qbe \
    && rm -rf /tmp/qbe-1.3 /tmp/qbe-1.3.tar.xz

RUN mkdir -p /usr/local/share \
    && dpkg-query --show --showformat='${Package}\t${Version}\n' \
        > /usr/local/share/gate6d-packages.txt

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /work
