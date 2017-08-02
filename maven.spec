%{?scl:%scl_package maven}
%{!?scl:%global pkg_name %{name}}

%bcond_without  logback

%global bundled_slf4j_version 1.7.25

Name:           %{?scl_prefix}maven
Epoch:          1
Version:        3.5.0
Release:        4.1%{?dist}
Summary:        Java project management and project comprehension tool
License:        ASL 2.0
URL:            http://maven.apache.org/
BuildArch:      noarch

Source0:        http://archive.apache.org/dist/%{pkg_name}/%{pkg_name}-3/%{version}/source/apache-%{pkg_name}-%{version}-src.tar.gz
Source1:        maven-bash-completion
Source2:        mvn.1

Patch1:         0001-Adapt-mvn-script.patch
# Part of https://github.com/apache/maven/pull/109
Patch2:         0002-Update-to-current-slf4j.patch
# Fedora specific, avoids usage of unpackaged groovy-maven-plugin
Patch3:         0003-Replace-groovy-invocation-with-antrun.patch
# Downstream-specific, avoids dependency on logback
# Used only when %without logback is in effect
Patch4:         0004-Invoke-logback-via-reflection.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(com.google.guava:guava)
BuildRequires:  %{?scl_prefix}mvn(com.google.inject:guice::no_aop:)
BuildRequires:  %{?scl_prefix}mvn(commons-cli:commons-cli)
BuildRequires:  %{?scl_prefix}mvn(commons-jxpath:commons-jxpath)
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.apache.commons:commons-lang3)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.resolver:maven-resolver-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.resolver:maven-resolver-connector-basic)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.resolver:maven-resolver-impl)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.resolver:maven-resolver-spi)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.resolver:maven-resolver-transport-wagon)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.resolver:maven-resolver-util)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.wagon:wagon-file)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.wagon:wagon-http::shaded:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  %{?scl_prefix}mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  %{?scl_prefix}mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.fusesource.jansi:jansi)
BuildRequires:  %{?scl_prefix}mvn(org.mockito:mockito-core)
BuildRequires:  %{?scl_prefix}mvn(org.slf4j:slf4j-api)
BuildRequires:  %{?scl_prefix}mvn(org.slf4j:slf4j-simple)
BuildRequires:  %{?scl_prefix}mvn(org.sonatype.plexus:plexus-cipher)
BuildRequires:  %{?scl_prefix}mvn(org.sonatype.plexus:plexus-sec-dispatcher)
BuildRequires:  %{?scl_prefix}mvn(regexp:regexp)
BuildRequires:  %{?scl_prefix}mvn(xmlunit:xmlunit)

# Missed by builddep
BuildRequires:  %{?scl_prefix}mvn(org.slf4j:jcl-over-slf4j:pom:)

BuildRequires:  %{?scl_prefix}slf4j-sources = %{bundled_slf4j_version}

%if %{with logback}
BuildRequires:  mvn(ch.qos.logback:logback-classic)
%endif

Requires:       %{name}-lib = %{epoch}:%{version}-%{release}

# Theoretically Maven might be usable with just JRE, but typical Maven
# workflow requires full JDK, so we recommend it here.
%{?fedora:Recommends}%{!?fedora:Requires}: java-devel

# XMvn does generate auto-requires, but explicit requires are still
# needed because some symlinked JARs are not present in Maven POMs or
# their dependency scope prevents them from being added automatically
# by XMvn.  It would be possible to explicitly specify only
# dependencies which are not generated automatically, but adding
# everything seems to be easier.
Requires:       %{?scl_prefix}aopalliance
Requires:       %{?scl_prefix}apache-commons-cli
Requires:       %{?scl_prefix}apache-commons-io
Requires:       %{?scl_prefix}apache-commons-lang
Requires:       %{?scl_prefix}apache-commons-lang3
Requires:       %{?scl_prefix}apache-commons-logging
Requires:       %{?scl_prefix}atinject
Requires:       %{?scl_prefix}cdi-api
Requires:       %{?scl_prefix}google-guice
Requires:       %{?scl_prefix}guava
Requires:       %{?scl_prefix}hawtjni-runtime
Requires:       %{?scl_prefix}httpcomponents-client
Requires:       %{?scl_prefix}httpcomponents-core
Requires:       %{?scl_prefix}jansi
Requires:       %{?scl_prefix}jansi-native
Requires:       %{?scl_prefix}jcl-over-slf4j
Requires:       %{?scl_prefix}maven-resolver-api
Requires:       %{?scl_prefix}maven-resolver-connector-basic
Requires:       %{?scl_prefix}maven-resolver-impl
Requires:       %{?scl_prefix}maven-resolver-spi
Requires:       %{?scl_prefix}maven-resolver-transport-wagon
Requires:       %{?scl_prefix}maven-resolver-util
Requires:       %{?scl_prefix}maven-shared-utils
Requires:       %{?scl_prefix}maven-wagon-file
Requires:       %{?scl_prefix}maven-wagon-http
Requires:       %{?scl_prefix}maven-wagon-http-shared
Requires:       %{?scl_prefix}maven-wagon-provider-api
Requires:       %{?scl_prefix}plexus-cipher
Requires:       %{?scl_prefix}plexus-classworlds
Requires:       %{?scl_prefix}plexus-containers-component-annotations
Requires:       %{?scl_prefix}plexus-interpolation
Requires:       %{?scl_prefix}plexus-sec-dispatcher
Requires:       %{?scl_prefix}plexus-utils
Requires:       %{?scl_prefix}sisu-inject
Requires:       %{?scl_prefix}sisu-plexus
Requires:       %{?scl_prefix}slf4j

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

%package        lib
Summary:        Core part of Maven
# If XMvn is part of the same RPM transaction then it should be
# installed first to avoid triggering rhbz#1014355.
OrderWithRequires: %{?scl_prefix}xmvn-minimal

# Maven upstream uses patched version of SLF4J.  They unpack
# slf4j-simple-sources.jar, apply non-upstreamable, Maven-specific
# patch (using a script written in Groovy), compile and package as
# maven-slf4j-provider.jar, together with Maven-specific additions.
Provides:       %{?scl_prefix}bundled(slf4j) = %{bundled_slf4j_version}

%description    lib
Core part of Apache Maven that can be used as a library.

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
%{summary}.

%prep
%setup -q -n apache-%{pkg_name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1

# not really used during build, but a precaution
find -name '*.jar' -not -path '*/test/*' -delete
find -name '*.class' -delete
find -name '*.bat' -delete

sed -i 's:\r::' apache-maven/src/conf/settings.xml

# Disable plugins which are not useful for us
%pom_remove_plugin -r :animal-sniffer-maven-plugin
%pom_remove_plugin -r :apache-rat-plugin
%pom_remove_plugin -r :maven-site-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :buildnumber-maven-plugin

%mvn_package :apache-maven __noinstall

%if %{without logback}
%pom_remove_dep -r :logback-classic
%patch4 -p1
%endif

%mvn_alias :maven-resolver-provider :maven-aether-provider

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

mkdir m2home
(cd m2home
    tar --delay-directory-restore -xvf ../apache-maven/target/*tar.gz
)

%install
%mvn_install

export M2_HOME=$(pwd)/m2home/apache-maven-%{version}%{?ver_add}

install -d -m 755 %{buildroot}%{_datadir}/%{pkg_name}/conf
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{pkg_name}
install -d -m 755 %{buildroot}%{_datadir}/bash-completion/completions
install -d -m 755 %{buildroot}%{_mandir}/man1

cp -a $M2_HOME/{bin,lib,boot} %{buildroot}%{_datadir}/%{pkg_name}/
xmvn-subst -R %{buildroot} -s %{buildroot}%{_datadir}/%{pkg_name}

# Transitive deps of wagon-http, missing because of unshading
build-jar-repository -s -p %{buildroot}%{_datadir}/%{pkg_name}/lib \
    commons-{codec,logging} httpcomponents/{httpclient,httpcore} maven-wagon/http-shared

# Transitive deps of cdi-api that should have been excluded
rm %{buildroot}%{_datadir}/%{pkg_name}/lib/jboss-interceptors*.jar
rm %{buildroot}%{_datadir}/%{pkg_name}/lib/javax.el-api*.jar

for cmd in mvn mvnDebug mvnyjp; do
    ln -s %{_datadir}/%{pkg_name}/bin/$cmd %{buildroot}%{_bindir}/$cmd
    echo ".so man1/mvn.1" >%{buildroot}%{_mandir}/man1/$cmd.1
done
install -p -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/mvn
mv $M2_HOME/bin/m2.conf %{buildroot}%{_sysconfdir}
ln -sf %{_sysconfdir}/m2.conf %{buildroot}%{_datadir}/%{pkg_name}/bin/m2.conf
mv $M2_HOME/conf/settings.xml %{buildroot}%{_sysconfdir}/%{pkg_name}
ln -sf %{_sysconfdir}/%{pkg_name}/settings.xml %{buildroot}%{_datadir}/%{pkg_name}/conf/settings.xml
mv $M2_HOME/conf/logging %{buildroot}%{_sysconfdir}/%{pkg_name}
ln -sf %{_sysconfdir}/%{pkg_name}/logging %{buildroot}%{_datadir}/%{pkg_name}/conf

%files lib -f .mfiles
%doc LICENSE NOTICE README.md
%{_datadir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%dir %{_sysconfdir}/%{pkg_name}
%dir %{_sysconfdir}/%{pkg_name}/logging
%config(noreplace) %{_sysconfdir}/m2.conf
%config(noreplace) %{_sysconfdir}/%{pkg_name}/settings.xml
%config(noreplace) %{_sysconfdir}/%{pkg_name}/logging/simplelogger.properties

%files
%attr(0755,root,root) %{_bindir}/mvn*
%{_datadir}/bash-completion
%{_mandir}/man1/mvn*.1.gz

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1:3.5.0-4.1
- Automated package import and SCL-ization

* Thu Jun 08 2017 Michael Simacek <msimacek@redhat.com> - 1:3.5.0-4
- Update logback conditional to replace logback usage with reflection

* Wed Apr 26 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.0-3
- Add apache-commons-codec to plexus.core
- Resolves: rhbz#1445738

* Wed Apr 19 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.0-2
- Add alias for maven-aether-provider

* Tue Apr 11 2017 Michael Simacek <msimacek@redhat.com> - 1:3.5.0-1
- Update to upstream version 3.5.0

* Fri Mar  3 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.3.9-9
- Fix bash-completion directory ownership

* Wed Mar 01 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-8
- Avoid subshell for build-jar-repository

* Thu Feb 16 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.3.9-7
- Conditionalize weak dependencies

* Tue Feb 14 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.3.9-6
- Remove BR on maven-javadoc-plugin

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-5
- Remove BR on buildnumber-plugin

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-4
- Remove buildnumber-plugin from build

* Thu Feb 02 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-3
- Add conditional for logback

* Thu Feb 02 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-2
- Remove site-plugin and enforce-plugin from build

* Wed Feb 01 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-1
- Downgrade to 3.3.9

* Wed Dec 14 2016 Michael Simacek <msimacek@redhat.com> - 3.4.0-0.6.20161118git8ae1a3e
- Bump slf4j version

* Fri Nov 18 2016 Michael Simacek <msimacek@redhat.com> - 3.4.0-0.5.20161118git8ae1a3e
- Restore compatibility with maven-polyglot

* Fri Nov 18 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-0.4.20161118git8ae1a3e
- Versioned bundled(slf4j) provides

* Fri Nov 18 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-0.3.20161118git8ae1a3e
- Update to latest upstream snapshot
- Source-bundle slf4j-simple

* Mon Aug 15 2016 Michael Simacek <msimacek@redhat.com> - 3.4.0-0.2.20160807git9f2452a
- Use patched upstream launcher instead of custom script

* Mon Aug  8 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-0.1.20160807git9f2452a
- Update to 3.4.0 snapshot

* Fri Jul  1 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-6
- Add missing BR on maven-enforcer-plugin

* Tue Jun 28 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-5
- Add maven-lib subpackage

* Thu Apr  7 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-4
- Force SLF4J SimpleLogger re-initialization
- Resolves: rhbz#1324832

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-2
- Fix symlinks: add commons-lang3 and remove geronimo-annotation

* Fri Nov 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-1
- Update to upstream version 3.3.9

* Mon Nov  2 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.8-1
- Update to upstream version 3.3.8

* Fri Jul 10 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.3-3
- Recommend java-devel instead of requiring it

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.3-1
- Update to upstream version 3.3.3

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-2
- Install mvnDebug and mvnyjp in bindir
- Update manpage
- Resolves: rhbz#1207850

* Mon Mar 16 2015 Michal Srb <msrb@redhat.com> - 3.3.1-1
- Add commons-io, commons-lang and jsoup to plexus.core (Resolves: rhbz#1202286)

* Fri Mar 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-1
- Update to upstream version 3.3.1

* Thu Mar 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.0-1
- Update to upstream version 3.3.0

* Wed Feb 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.5-2
- Add objectweb-asm to plexus.core

* Mon Jan 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.5-1
- Update to upstream version 3.2.5

* Sat Dec  6 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.2.3-4
- Fix bash completion filename

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.3-3
- Remove legacy Obsoletes/Provides for maven2

* Mon Sep 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.3-2
- Update patches

* Fri Aug 22 2014 Michal Srb <msrb@redhat.com> - 3.2.3-1
- Update to upstream version 3.2.3

* Wed Jun 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-10
- Fix artifact pattern in %%mvn_file invocation

* Wed Jun  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-9
- Install additional lib symlinks only for JAR files

* Wed Jun  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-8
- Fix dangling symlinks in Maven lib dir
- Resolves: rhbz#1104396

* Mon Jun  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-7
- Clean up patches
- Add patch for MNG-5613

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-6
- Remove BuildRequires on maven-surefire-provider-junit4

* Mon Mar 17 2014 Michal Srb <msrb@redhat.com> - 3.2.1-5
- Add missing BR: modello-maven-plugin

* Fri Mar  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-4
- Set logback dependency scope to provided

* Mon Feb 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-3
- Add patch for MNG-5591

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-2
- Migrate to Wagon subpackages

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Remove BR on plexus-containers-container-default

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Update to upstream version 3.2.1

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-1
- Update to upstream version 3.2.0

* Mon Dec 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-15
- Read user and system config files in maven-script

* Wed Nov 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-14
- Update to Sisu 0.1.0 and Guice 3.1.6

* Fri Nov  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-13
- Add wagon-http-shared4 to plexus.core

* Tue Nov  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-6
- Update F20 to upstream bugfix release 3.1.1

* Tue Nov  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-5
- Add OrderWithRequires: xmvn
- Related: rhbz#1014355

* Tue Oct 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-4
- Add explicit requires

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-3
- Rebuild to regenerate broken POM files
- Related: rhbz#1021484

* Mon Oct 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-10
- Add dependencies of wagon-http-shaded to plexus.core
- Remove objectweb-asm from plexus.core
- Add explicit requires
- Resolves: rhbz#1023872

* Mon Oct  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-1
- Update to upstream version 3.1.1
- Remove patch for MNG-5503 (included upstream)

* Mon Sep 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-9
- Synchronize JAR list in lib/ with upstream release
- Remove test dependencies on aopalliance and cglib

* Thu Aug 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-8
- Migrate from easymock 1 to easymock 3
- Resolves: rhbz#1002432

* Fri Aug 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-7
- Add patch for MNG-5503
- Resolves: rhbz#991454

* Mon Aug 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-6
- Update Aether to 0.9.0.M3

* Mon Aug 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-5
- Prepare for update to Aether 0.9.0.M3

* Fri Aug  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-4
- Remove workaround for incompatible plexus-utils

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-2
- Install simplelogger.properties into %{_sysconfdir}

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-1
- Update to upstream version 3.1.0

* Fri Jul 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-8
- Use sonatype-aether symlinks

* Mon May 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-7
- Move bash-completion files to primary location
- Resolves: rhbz#918000

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
