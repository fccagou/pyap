# syntax = docker/dockerfile:1.3
ARG RHEL_VERSION=8

FROM almalinux:$RHEL_VERSION as builder
LABEL fr.fccagouu.vendor="The Cagou Corp."
LABEL org.opencontainers.image.authors="fccagou <fccagou@gmail.com>"

RUN dnf install -y \
      python3 \
	  python3-pyusb \
	  libusb \
	  rpm-build \
	  git \
    && dnf clean all \
	&& rm -rf /var/cache/dnf

RUN dnf install -y python3 python3-pyusb libusb \
    && dnf clean all \
	&& rm -rf /var/cache/dnf

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app
RUN ./buildrpm


FROM almalinux:$RHEL_VERSION
LABEL fr.fccagouu.vendor="The Cagou Corp."
LABEL org.opencontainers.image.authors="fccagou <fccagou@gmail.com>"

COPY --from=builder /app/dist/pyap*noarch.rpm  .
RUN dnf install -y pyap*noarch.rpm

ENTRYPOINT ["/usr/bin/pyap", "--nopid", "--fg", "-v", "--server" ]
CMD ["--conf=/usr/share/doc/pyap/test.conf" ]



