%global _use_internal_dependency_generator 0
%global __find_requires_orig %{__find_requires}
%define __find_requires %{_builddir}/%{?buildsubdir}/build/find-requires %{__find_requires_orig}

Summary:   Processing for serial crystallography
Name:      crystfel
Version:   0.7.0
Release:   4%{?dist}
Source0:   %{name}-%{version}-patch1.tar.gz
Source1:   crystfel-find-req
Source2:   cbf2hdf5.cpp
Source3:   cellgnu.sh
Source4:   mosflm-7.2.1-noX11
Source5:   clibd.tgz
Source6:   environ.def
Source7:   default.def
License:   GPL
Group:     Applications/Scientific
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:    %{_prefix}
Vendor:    CFEL
Url:       http://www.desy.de/~twhite/crystfel/
Requires:  hdf5, fftw, gsl, gtk2, gnuplot
BuildRequires: hdf5-devel, fftw-devel, gsl-devel, gtk2-devel
AutoReqProv: no

%description
CrystFEL is a suite of programs for processing diffraction data acquired "serially" in a "snapshot" manner, such as when using the technique of Serial Femtosecond Crystallography (SFX) with a free-electron laser source. CrystFEL comprises programs for indexing and integrating diffraction patterns, scaling and merging intensities, simulating patterns, calculating figures of merit for the data and visualising the results.

%prep
%setup -n %{name}-%{version} 


%build
mkdir build && cd build
cmake3 -DCMAKE_INSTALL_PREFIX=/opt/crystfel ..
make


%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT 
mkdir -p %{_builddir}/%{?buildsubdir}/build/
#install -m 755 %{SOURCE1}  %{_builddir}/%{?buildsubdir}/build/find-requires
chmod +x $RPM_BUILD_ROOT/opt/crystfel/share/doc/crystfel/scripts/*
chmod -x $RPM_BUILD_ROOT/opt/crystfel/share/doc/crystfel/scripts/README
ln -s /opt/crystfel/share/doc/crystfel/scripts $RPM_BUILD_ROOT/opt/crystfel/

c++ -O2 -fPIC %{SOURCE2} -o $RPM_BUILD_ROOT/opt/crystfel/bin/cbf2hdf5 -lhdf5 -lm

# small gnuplot scriplet
install -m 755 %{SOURCE3} %{buildroot}/opt/crystfel/bin/cellgnu.sh

# still having problems using crystfel with mosflm v7.2.2 
install -m 755 %{SOURCE4} %{buildroot}/opt/crystfel/bin/mosflm


mkdir -p %{buildroot}/etc/modulefiles/tools/
cat <<EOF > %{buildroot}/etc/modulefiles/tools/crystfel
#%Module 1.0
#
#  ccp4 and related. 
# 
module-whatis  "Setup for CrystFEL "

prepend-path          PATH             /opt/crystfel/bin:/opt/crystfel/scripts
prepend-path          MANPATH          /opt/crystfel/share/man/
setenv                CINCL            /opt/crystfel/include
setenv                CLIBD            /opt/crystfel/data
setenv                CCP4_SCR         /tmp

proc ModulesHelp { } {
    puts stdout     "This module sets the environment for CrystFEL"
    puts stdout     "It also load the xray module to include ccp4, xds, ipmosflm etc "
}

EOF

install -m 755 %{SOURCE4} %{buildroot}/opt/crystfel/bin/mosflm

#
#  CCP4 standalone files
#
tar -C %{buildroot}/opt/crystfel/ -xvf  %{SOURCE5} 

install -m 755 %{SOURCE6} %{buildroot}/opt/crystfel/include/environ.def
install -m 755 %{SOURCE7} %{buildroot}/opt/crystfel/include/default.def


cat <<EOF> %{buildroot}/opt/crystfel/bin/crystfel.setup.sh
export CINCL=/opt/crystfel/include
export CLIBD=/opt/crystfel/data
export CCP4_SCR=/tmp
export PATH=/opt/crystfel/bin:/opt/crystfel/share/doc/crystfel/scripts:$PATH
EOF

cat <<EOF> %{buildroot}/opt/crystfel/bin/crystfel.setup.csh
setenv CINCL /opt/crystfel/include
setenv CLIBD /opt/crystfel/data
setenv CCP4_SCR /tmp
setenv PATH /opt/crystfel/bin:/opt/crystfel/share/doc/crystfel/scripts:$PATH
EOF

chmod 755 %{buildroot}/opt/crystfel/bin/crystfel.setup*

# buggy
rm -f %{buildroot}/opt/crystfel/data/monomers/pdb_v2to3.py

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
/opt/crystfel/*
/etc/modulefiles/tools/crystfel

%changelog
* Tue Oct 02 2018 crystfel-0.7.0-4
- add ccp4 data files 
- add environment script
* Mon Oct 01 2018 crystfel-0.7.0-3
- still problems with v7.2.2 revert back to v7.2.1
* Mon Oct 01 2018 crystfel-0.7.0-2
- patch to work with mosflm 7.2.2
- just fetched updated code from git repository
* Wed Sep 05 2018 crystfel-0.7.0-1
- update
* Wed Sep 05 2018 crystfel-0.6.1-3
- minor changes
* Tue Jan 19 2016 crystfel-0.6.1-2
- add cbf2hdf5
* Mon Sep 28 2015 crystfel-0.6.1-1
- first 

