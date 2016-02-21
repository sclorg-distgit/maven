%global pkg_name maven
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global debug_package %{nil}

Name:           %{?scl_prefix}%{pkg_name}
Version:        3.0.5
Release:        16.25%{?dist}
Summary:        Java project management and project comprehension tool

License:        ASL 2.0
URL:            http://maven.apache.org/
Source0:        http://archive.apache.org/dist/%{pkg_name}/%{pkg_name}-3/%{version}/source/apache-%{pkg_name}-%{version}-src.tar.gz
Source1:        maven-bash-completion
Source2:        mvn.1

# 2xx for created non-buildable sources
Source200:      %{pkg_name}-script

# Patch1XX could be upstreamed probably
Patch100:       0005-Use-generics-in-modello-generated-code.patch

# Patch2XX backported from upstream
# Fixes MNG-5402 (patch from upstream commit f95ab2e)
Patch200:       0001-MNG-5402-Better-build-number-for-git.patch

# Access Maven Central via HTTPS by default
Patch300:       0001-default-to-ssl-for-central.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}xmvn >= 1.3.0-5

BuildRequires:  %{?scl_prefix}aether-api >= 1.13.1-8
BuildRequires:  %{?scl_prefix}aether-connector-wagon
BuildRequires:  %{?scl_prefix}aether-impl
BuildRequires:  %{?scl_prefix}aether-spi
BuildRequires:  %{?scl_prefix}aether-util
BuildRequires:  %{?scl_prefix}aopalliance
BuildRequires:  %{?scl_prefix_java_common}apache-commons-cli
BuildRequires:  %{?scl_prefix}apache-commons-jxpath
BuildRequires:  %{?scl_prefix}apache-resource-bundles
BuildRequires:  %{?scl_prefix_java_common}atinject
BuildRequires:  %{?scl_prefix}cglib
BuildRequires:  %{?scl_prefix_java_common}easymock
BuildRequires:  %{?scl_prefix}google-guice >= 3.1.3-8
BuildRequires:  %{?scl_prefix_java_common}hamcrest
BuildRequires:  %{?scl_prefix_java_common}junit
BuildRequires:  %{?scl_prefix}maven-assembly-plugin
BuildRequires:  %{?scl_prefix}maven-compiler-plugin
BuildRequires:  %{?scl_prefix}maven-install-plugin
BuildRequires:  %{?scl_prefix}maven-jar-plugin
BuildRequires:  %{?scl_prefix}maven-javadoc-plugin
BuildRequires:  %{?scl_prefix}maven-parent
BuildRequires:  %{?scl_prefix}maven-remote-resources-plugin
BuildRequires:  %{?scl_prefix}maven-resources-plugin
BuildRequires:  %{?scl_prefix}maven-site-plugin
BuildRequires:  %{?scl_prefix}maven-surefire-plugin
BuildRequires:  %{?scl_prefix}maven-wagon-file
BuildRequires:  %{?scl_prefix}maven-wagon-http
BuildRequires:  %{?scl_prefix}maven-wagon-http-shared4
BuildRequires:  %{?scl_prefix}maven-wagon-provider-api
BuildRequires:  %{?scl_prefix_java_common}objectweb-asm
BuildRequires:  %{?scl_prefix}plexus-cipher
BuildRequires:  %{?scl_prefix}plexus-classworlds
BuildRequires:  %{?scl_prefix}plexus-containers-component-annotations
BuildRequires:  %{?scl_prefix}plexus-containers-component-metadata >= 1.5.5
BuildRequires:  %{?scl_prefix}plexus-interpolation
BuildRequires:  %{?scl_prefix}plexus-sec-dispatcher
BuildRequires:  %{?scl_prefix}plexus-utils
BuildRequires:  %{?scl_prefix}sisu-inject-bean
BuildRequires:  %{?scl_prefix}sisu-inject-plexus
BuildRequires:  %{?scl_prefix}xmlunit
%if 0%{?fedora}
BuildRequires:  %{?scl_prefix}animal-sniffer >= 1.6-5
%endif

Requires:       which

# XMvn does generate auto-requires, but explicit requires are still
# needed because some symlinked JARs are not present in Maven POMs or
# their dependency scope prevents them from being added automatically
# by XMvn.  It would be possible to explicitly specify only
# dependencies which are not generated automatically, but adding
# everything seems to be easier.
Requires:       %{?scl_prefix}aether-api
Requires:       %{?scl_prefix}aether-connector-wagon
Requires:       %{?scl_prefix}aether-impl
Requires:       %{?scl_prefix}aether-spi
Requires:       %{?scl_prefix}aether-util
Requires:       %{?scl_prefix}aopalliance
Requires:       %{?scl_prefix_java_common}apache-commons-cli
Requires:       %{?scl_prefix_java_common}apache-commons-codec
Requires:       %{?scl_prefix_java_common}apache-commons-logging
Requires:       %{?scl_prefix_java_common}atinject
Requires:       %{?scl_prefix}cglib
Requires:       %{?scl_prefix}google-guice
Requires:       %{?scl_prefix_java_common}guava
Requires:       %{?scl_prefix}httpcomponents-client
Requires:       %{?scl_prefix}httpcomponents-core
Requires:       %{?scl_prefix}maven-wagon-file
Requires:       %{?scl_prefix}maven-wagon-http
Requires:       %{?scl_prefix}maven-wagon-http-shared4
Requires:       %{?scl_prefix}maven-wagon-provider-api
Requires:       %{?scl_prefix_java_common}objectweb-asm
Requires:       %{?scl_prefix}plexus-cipher
Requires:       %{?scl_prefix}plexus-containers-component-annotations
Requires:       %{?scl_prefix}plexus-interpolation
Requires:       %{?scl_prefix}plexus-sec-dispatcher
Requires:       %{?scl_prefix}plexus-utils
Requires:       %{?scl_prefix}sisu-inject-bean
Requires:       %{?scl_prefix}sisu-inject-plexus

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
%{summary}.

%prep
%setup -q -n apache-%{pkg_name}-%{version}%{?ver_add}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch100 -p1
%patch200 -p1
%patch300 -p1

# Generate build number based on package release number
%pom_remove_plugin :buildnumber-maven-plugin maven-core
sed -i "
/buildNumber=/ {
  s/=.*/=Red Hat %{version}-%{release}/
  s/%{dist}$//
}
/timestamp=/ d
" `find -name build.properties`

# Create Maven scripts
sed s/@MVN@/mvn/      %{SOURCE200} >mvn
sed s/@MVN@/mvnDebug/ %{SOURCE200} >mvnDebug
sed s/@MVN@/mvnyjp/   %{SOURCE200} >mvnyjp

# not really used during build, but a precaution
rm maven-ant-tasks-*.jar

# fix line endings
sed -i 's:\r::' *.txt

# fix for animal-sniffer (we don't generate 1.5 signatures)
sed -i 's:check-java-1.5-compat:check-java-1.6-compat:' pom.xml

rm -f apache-maven/src/bin/*.bat
sed -i 's:\r::' apache-maven/src/conf/settings.xml

# Update shell scripts to use unversioned classworlds
sed -i -e s:'-classpath "${M2_HOME}"/boot/plexus-classworlds-\*.jar':'-classpath "${M2_HOME}"/boot/plexus-classworlds.jar':g \
        apache-maven/src/bin/mvn*

# Disable animal-sniffer on RHEL
# Temporarily disabled for fedora to solve asm & asm4 clashing on classpath
#if [ %{?rhel} ]; then
%pom_remove_plugin :animal-sniffer-maven-plugin
#fi
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Put all JARs in standard location, but create symlinks in Maven lib
# directory so that Plexus Classworlds can find them.
%mvn_file ":{*}:jar:" %{pkg_name}/@1 %{_datadir}/%{pkg_name}/lib/@1

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

mkdir m2home
(cd m2home
    tar --delay-directory-restore -xvf ../apache-maven/target/*tar.gz
    chmod -R +rwX apache-%{pkg_name}-%{version}%{?ver_add}
    chmod -x apache-%{pkg_name}-%{version}%{?ver_add}/conf/settings.xml
)
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install

export M2_HOME=$(pwd)/m2home/apache-maven-%{version}%{?ver_add}

install -d -m 755 %{buildroot}%{_datadir}/%{pkg_name}/bin
install -d -m 755 %{buildroot}%{_datadir}/%{pkg_name}/conf
install -d -m 755 %{buildroot}%{_datadir}/%{pkg_name}/boot
install -d -m 755 %{buildroot}%{_datadir}/%{pkg_name}/lib/ext
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{pkg_name}
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -d -m 755 %{buildroot}%{_mandir}/man1

install -p -m 755 mvn %{buildroot}%{_bindir}/
install -p -m 755 mvnDebug %{buildroot}%{_bindir}/
install -p -m 755 mvnyjp %{buildroot}%{_bindir}/
install -p -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/bash_completion.d/%{pkg_name}
mv $M2_HOME/bin/m2.conf %{buildroot}%{_sysconfdir}
ln -sf %{_sysconfdir}/m2.conf %{buildroot}%{_datadir}/%{pkg_name}/bin/m2.conf
mv $M2_HOME/conf/settings.xml %{buildroot}%{_sysconfdir}/%{pkg_name}
ln -sf %{_sysconfdir}/%{pkg_name}/settings.xml %{buildroot}%{_datadir}/%{pkg_name}/conf/settings.xml

cp -a $M2_HOME/bin/* %{buildroot}%{_datadir}/%{pkg_name}/bin

ln -sf $(build-classpath plexus/classworlds) \
    %{buildroot}%{_datadir}/%{pkg_name}/boot/plexus-classworlds.jar

(cd %{buildroot}%{_datadir}/%{pkg_name}/lib
    # 1. atinject, aopalliance and objectweb-asm are bundled in
    #    sisu-inject-bean upstream normally
    # 2. httpcomponents-core, httpcomponents-client, commons-logging
    #    and commons-codec are bundled in wagon-http-shaded upstream
    #    normally
    build-jar-repository -s -p . \
        aether/aether-api \
        aether/aether-connector-wagon \
        aether/aether-impl \
        aether/aether-spi \
        aether/aether-util \
        commons-cli \
        plexus/plexus-cipher \
        plexus/containers-component-annotations \
        plexus/interpolation \
        plexus/plexus-sec-dispatcher \
        plexus/utils \
        guava \
        google-guice-no_aop \
        sisu/sisu-inject-bean \
        sisu/sisu-inject-plexus \
        maven-wagon/file \
        maven-wagon/http-shaded \
        maven-wagon/provider-api \
        \
        atinject \
        aopalliance \
        cglib \
        objectweb-asm/asm-all \
        \
        maven-wagon/http-shared4 \
        httpcomponents/httpclient-4.2 \
        httpcomponents/httpcore-4.2 \
        commons-logging \
        commons-codec \
)
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE.txt NOTICE.txt README.txt
%{_datadir}/%{pkg_name}
%{_bindir}/mvn*
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_sysconfdir}/%{pkg_name}
%config(noreplace) %{_sysconfdir}/m2.conf
%config(noreplace) %{_sysconfdir}/%{pkg_name}/settings.xml
%dir %{_sysconfdir}/bash_completion.d
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{pkg_name}
%{_mandir}/man1/mvn.1.gz

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 3.0.5-16.25
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 3.0.5-16.24
- maven33 rebuild

* Tue Jul 21 2015 Michal Srb <msrb@redhat.com> - 3.0.5-16.23
- Access Maven Central via HTTPS by default
- Resolves: rhbz#1231711

* Fri Jan 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.22
- Add R on which

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.21
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michal Srb <msrb@redhat.com> - 3.0.5-16.20
- Rebuild to fix httpcommons symlinks

* Tue Jan 13 2015 Michal Srb <msrb@redhat.com> - 3.0.5-16.19
- Migrate to httpcomponents 4.2 (compat)

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 3.0.5-16.18
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.17
- Rebuild to fix symlinks

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 3.0.5-16.16
- BR/R on packages from rh-java-common

* Fri Jan  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.15
- Don't install POM symlinks in Maven lib/ dir

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 3.0.5-16.14
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.13
- Mass rebuild 2014-05-26

* Fri Feb 28 2014 Michael Simacek <msimacek@redhat.com> - 3.0.5-16.12
- Remove BR on slf4j

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 3.0.5-16.11
- Adjust maven-wagon R/BR

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.10
- Remove dependency on Plexus container

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 3.0.5-16.9
- Fix directory ownership

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.8
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.7
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Michal Srb <msrb@redhat.com> - 3.0.5-16.6
- SCL-ize maven-script

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.5
- Rebuild to fix incorrect auto-requires

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.4
- Remove requires on java

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16.1
- First maven30 software collection build

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-16
- BuildRequire xmvn >= 1.3.0-5

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.0.5-15
- Mass rebuild 2013-12-27

* Thu Nov  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-14
- Add cglib to plexus.core

* Wed Nov  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-13
- Add wagon-http-shared4 to plexus.core
- Add explcit requires

* Mon Oct 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-12
- Add missing dependencies to plexus.core
- Add patch for MNG-5402

* Wed Oct 16 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.5-11
- Add objectweb-asm back to dependencies
- Resolves: rhbz#1019834

* Tue Oct 08 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.5-10
- Rebuild and use no_aop guice
- Synchronize dependencies with upstream
- Resolves: rhbz#1016447

* Tue Sep 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-9
- Generate build number based on package release number

* Mon Jul 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-8
- Install mvnDebug and mvnyjp scripts
- Resolves: rhbz#986976

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-7
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri May 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-6
- Remove unneeded BR: async-http-client
- Add Requires on java-devel

* Thu May  2 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-5
- BR proper aether subpackages
- Resolves: rhbz#958160

* Fri Apr 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-4
- Add missing BuildRequires

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-3
- Make ext/ a subdirectory of lib/

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-2
- In maven-script don't override M2_HOME if already set

* Fri Mar  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-1
- Update to upstream version 3.0.5
- Move settings.xml to /etc

* Mon Feb 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-32
- Remove xerces-j2 from plexus.core realm
- Resolves: rhbz#784816

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-31
- Migrate BR from sisu to sisu subpackages

* Wed Feb  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-30
- Remove unneeded R: maven-local

* Fri Jan 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-29
- Drop support for local mode
- Build with xmvn, rely on auto-requires

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-28
- Move mvn-local and mvn-rpmbuild out of %_bindir

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-27
- Move some parts to maven-local package

* Thu Nov 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-26
- Force source >= 1.5 and target >= source

* Mon Nov 19 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-25
- Fix license tag

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-24
- Install NOTICE file with javadoc package

* Tue Nov 13 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-23
- Temporarly require Plexus POMs as a workaround

* Mon Nov 12 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-22
- Drop dependency on maven2-common-poms
- Drop support for /etc/maven/fragments

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-21
- Add support for custom jar/pom/fragment directories

* Thu Nov  8 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-20
- Remove all slf4j providers except nop from maven realm

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-19
- Add aopalliance and cglib to maven-model-builder test dependencies

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-18
- Add objectweb-asm to classpath

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-17
- Add aopalliance, cglib, slf4j to classpath

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-16
- Don't echo JAVA_HOME in maven-script
- Add bash completion for -Dproject.build.sourceEncoding

* Mon Oct 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-15
- Add a few bash completion goals

* Wed Oct 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-14
- Enable test skipping patch only for local mode (#869399)

* Fri Oct 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-13
- Make sure we look for requested pom file and not resolved

* Thu Oct 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-12
- Look into maven.repo.local first to handle corner-case packages (#865599)
- Finish handling of compatibility packages
- Disable animal-sniffer temporarily in Fedora as well

* Mon Aug 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-11
- Disable animal-sniffer on RHEL

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-10
- Fix exit code of mvn-rpmbuild outside of mock
- Fix bug in compatibility jar handling

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-9
- Run redundant dependency checks only in mock

* Tue Jul 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-8
- Add manual page

* Mon Jun 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-7
- Implement redundant dependency checks

* Thu May 24 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.0.4-6
- Bug 824789 -Use the version if it is possible.

* Mon May 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-5
- Use Obsoletes instead of Conflicts

* Mon May 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-4
- Obsolete and provide maven2

* Thu Mar 29 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-3
- Make package noarch again to simplify bootstrapping

* Thu Feb  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-2
- Make javadoc noarch
- Make compilation source level 1.5
- Fix borked tarball unpacking (reason unknown)

* Tue Jan 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-1
- Update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-16
- Add maven2-common-poms to Requires

* Tue Oct 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-15
- Provide mvn script now instead of maven2
- Conflict with older versions of maven2

* Tue Aug 30 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-14
- Fix test scope skipping

* Mon Aug 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-13
- Remove unnecessary deps causing problems from lib/
- Add utf-8 source encoding patch

* Thu Jul 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-12
- Disable debug package creation

* Thu Jul 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-11
- Change to arch specific since we are using _libdir for _jnidir

* Tue Jul 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-10
- Add bash completion (#706856)

* Mon Jul  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-9
- Add resolving from jnidir and java-jni

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-8
- Add maven-parent to BR/R

* Wed Jun 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-7
- Process fragments in alphabetical order

* Tue Jun 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-6
- Fix handling of fallback default_poms
- Add empty-dep into maven package to not require maven2 version

* Fri Jun 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-5
- Process fragments directly instead of maven2-depmap.xml
- Expect fragments in /usr/share/maven-fragments
- Resolve poms also from /usr/share/maven-poms

* Mon Jun  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-4
- Add help to mvn-rpmbuild and mvn-local (rhbz#710448)

* Tue May 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-3
- Improve and clean up depmap handling for m2/m3 repos

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-2
- Enable MAVEN_OPTS override in scripts

* Fri Mar  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-1
- Update to 3.0.3
- Add ext subdirectory to lib

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-0.1.rc1
- Update to 3.0.3rc1
- Enable tests again

* Thu Feb 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-2
- Added mvn-rpmbuild script to be used in spec files
- mvn-local is now mixed mode (online with javadir priority)
- Changed mvn.jpp to mvn.local

* Fri Jan 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-1
- Update to latest version (3.0.2)
- Ignore test failures temporarily

* Wed Jan 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-6
- Fix bug #669034

* Tue Jan 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-5
- Fix bugs #667625 #667614 and #667636
- Install maven metadata so they are not downloaded when mvn is run
- Rename mvn3-local to mvn-local
- Add more comments to resolver patch

* Tue Dec 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-4
- Add fedora local resolver
- Fix quoting of arguments to mvn scripts
- Add javadoc subpackage
- Make jars versionless and remove unneeded clean section

* Wed Dec  1 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-3
- Remove maven-ant-tasks jar in prep
- Make fragment file as %%config

* Tue Nov 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-2
- Added apache-commons-parent to BR after commons changes

* Tue Oct 12 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-1
- Initial package with vanilla maven (no jpp mode yet)
