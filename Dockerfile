# The base image. If not present, will be loaded from Dockerhub automatically
FROM centos:7
LABEL maintainer="Calipso+" 
LABEL version="0.7.0" 
LABEL description="Container for the CrystFEL"

ENV CINCL=/usr/local/crystfel/include
ENV CLIBD=/usr/local/crystfel/data
ENV CCP4_SCR=/tmp
ENV PATH=/usr/local/crystfel/bin:$PATH

RUN yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y 2>&1 | grep -v "already installed and latest version"
RUN yum install -y gcc gcc-gfortran libstdc++ GConf2 gtk2 libXtst curl hdf5 hdf5-devel libstdc++-devel libstdc++-static libgcc gtk2-devel libpng-devel ncurses-devel fftw-devel cairo-gobject-devel pango-devel gtk-doc gsl-devel bzip2 make cmake gcc gfortran autoconf automake tar unzip 2>&1 | grep -v "already installed and latest version"
RUN mkdir -p /usr/local/src /usr/local/crystfel/bin

#
#  Crystfel itself
#
RUN curl -L http://www.desy.de/~twhite/crystfel/crystfel-0.7.0.tar.gz  | gzip -dc | tar -xv -C /usr/local
WORKDIR /usr/local/crystfel-0.7.0
RUN ./configure --prefix=/usr/local/crystfel
RUN make && make install
RUN rm -rf /usr/local/crystfel-0.7.0

#
#  MOSFLM
#
# v7.2.2 has problems. revert back to mosflm 7.2.1!
RUN curl -s -L http://www.desy.de/~schluenz/crystfel/mosflm-7.2.1.tgz | gzip -dc | tar -xv -C /usr/local/crystfel/bin/
RUN ln -sf /usr/local/crystfel/bin/mosflm-linux-64-noX11 /usr/local/crystfel/bin/mosflm
RUN ln -sf /usr/local/crystfel/bin/mosflm-linux-64-noX11 /usr/local/crystfel/bin/ipmosflm

#
#  aux files
#
RUN curl -s -L http://www.desy.de/~schluenz/crystfel/default.def -o  /usr/local/crystfel/include/default.def
RUN curl -s -L http://www.desy.de/~schluenz/crystfel/environ.def -o  /usr/local/crystfel/include/environ.def
RUN curl -s -L http://www.desy.de/~schluenz/crystfel/clibd.tgz | gzip -dc | tar -xv -C /usr/local/crystfel/

#
#  ssh [might not be needed in general]
#
RUN yum install -y openssh-clients openssh-server && ssh-keygen -A && \
    sed -i 's/required\(.*pam_loginuid\)/optional\1/' /etc/pam.d/sshd

#
#  Clean up
#
RUN rm -rf /usr/local/src
RUN yum remove \*-devel -y
WORKDIR /

