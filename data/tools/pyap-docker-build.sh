docker build -t rpmbuild:c6 -<<EOF_DOCKERFILE
FROM centos:6
LABEL maintainer="fccagou@gmail.com"
LABEL description="Build rpm under centos 6"


RUN yum clean all \
    && yum update -y \
    && yum install -y rpm-build \
    && yum clean all

CMD ["/bin/bash"]

EOF_DOCKERFILE

 rm -rf /tmp/src/pyap
 mkdir -p /tmp/src
 cd /tmp/src
 git clone https://github.com/fccagou/pyap
 cd pyap
 pwd
 docker run --rm -ti -v$(pwd):/src rpmbuild:c6 /src/buildrpm
 PKG=$(cd dist && ls -tr pyap-*.noarch.rpm | head -1)
 docker build -t pyap:c6 -f- . <<EOF_PYAP6
FROM centos:6
LABEL maintainer="fccagou@gmail.com"
LABEL description="Centos6 pyap"

RUN yum install -y python-argparse

COPY dist/${PKG} /tmp
RUN yum localinstall -y /tmp/${PKG} \
    && rm -f /tmp/pyap*.rpm

CMD ["/usr/bin/pyap"]

EOF_PYAP6

cat <<EOF_USAGE
Test pyap runnning next cmd 

   docker run --rm -ti pyap:c6 /usr/bin/pyap --help
   docker run --rm -ti -p 8080:8080 pyap:c6 /usr/bin/pyap -s -d -v --fg --nopid -c /etc/pyap/pyap.conf.sample/pyap.conf

EOF_USAGE
