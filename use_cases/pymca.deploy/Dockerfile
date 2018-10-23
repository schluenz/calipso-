# The base image. If not present, will be loaded from Dockerhub automatically
FROM centos:7

LABEL maintainer="Calipso+" 
LABEL version="5.4.0" 
LABEL description="Container for PyMca"
LABEL Packager="Calipso+"
LABEL Author="Calipso+"

ENV PATH=/opt/anaconda/3/bin:$PATH

CMD /opt/anaconda/3/bin/pymca

RUN yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y 2>&1 | grep -v "already installed and latest version"
RUN yum install -y dbus dejavu-lgc-sans-fonts gedit unzip gzip tar pam libXt GConf2 gtk2 libXtst python xterm wget which curl mesa-libGLU-devel mesa-libGL bzip2 hdf5 hdf5-devel gtk2-devel libpng-devel ncurses-devel fftw-devel gmp-devel mpfr-devel libmpc-devel autoconf automake m4
RUN yum groupinstall -y "Development tools"

RUN mkdir -p /TMP && wget https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh -O /TMP/Anaconda3-5.3.0-Linux-x86_64.sh && /bin/bash /TMP/Anaconda3-5.3.0-Linux-x86_64.sh -b -p /opt/anaconda/3

RUN export PATH=/opt/anaconda/3/bin:$PATH

RUN conda install -y numpy h5py matplotlib
RUN conda install -y -c conda-forge fisx silx pyside libglu 
RUN pip install pymca==5.4.0

RUN dbus-uuidgen > /var/lib/dbus/machine-id
#
#  Clean up
#
RUN rm -rf /TMP 
RUN yum remove \*-devel -y
