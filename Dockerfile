# syntax = docker/dockerfile:1.3
ARG RHELVER=8
ARG RHELDISTRIB=almalinux

FROM $RHELDISTRIB:$RHELVER as builder
LABEL fr.fccagouu.vendor="The Cagou Corp."
LABEL org.opencontainers.image.authors="fccagou <fccagou@gmail.com>"

RUN dnf install -y \
	  rpm-build \
    && dnf clean all \
	&& rm -rf /var/cache/dnf

RUN dnf install -y python3 python3-pyusb libusb \
    && dnf clean all \
	&& rm -rf /var/cache/dnf

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app
RUN ./buildrpm


FROM $RHELDISTRIB:$RHELVER
LABEL fr.fccagou.vendor="The Cagou Corp."
LABEL org.opencontainers.image.authors="fccagou <fccagou@gmail.com>"

COPY --from=builder /app/dist/pyap*.rpm  .
RUN dnf install -y pyap*noarch.rpm

ENTRYPOINT ["/usr/bin/pyap", "--nopid", "--fg", "-v", "--server" ]
CMD ["--conf=/usr/share/doc/pyap/test.conf" ]



