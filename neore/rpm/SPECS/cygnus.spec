# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
# 
# This file is part of fiware-cygnus (FI-WARE project).
# 
# fiware-cygnus is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# fiware-cygnus is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
# 
# You should have received a copy of the GNU Affero General Public License along with fiware-cygnus. If not, see
# http://www.gnu.org/licenses/.
# 
# For those usages not covered by the GNU Affero General Public License please contact with iot_support at tid dot es

Summary:          Package for cygnus component
Name:             cygnus
Version:          %{_product_version}
Release:          %{_product_release}
License:          AGPLv3
BuildRoot:        %{_topdir}/BUILDROOT/
BuildArch:        x86_64
Requires(post):   /sbin/chkconfig, /usr/sbin/useradd
Requires(preun):  /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Group:            Applications/cygnus
Vendor:           Telefonica I+D
Provides:         cygnus%{_name_suffix} = %{_product_version}-%{_product_release}

%define _rpmfilename %%{ARCH}/%%{NAME}%{_name_suffix}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

%description
This connector is a (conceptual) derivative work of ngsi2cosmos, and implements
a Flume-based connector for context data coming from Orion Context Broker.

# Project information 
%define _project_name cygnus
%define _project_user cygnus
%define _service_name cygnus

# improve package speed avoiding jar repack
%define __jar_repack %{nil}

# System folders
# _sourcedir =${topdir}/SOURCES
%define _srcdir %{_sourcedir}/../../../
%define _install_dir /usr
%define _project_install_dir %{_install_dir}/%{_project_name}

# _localstatedir is a system var that goes to /var
 %define _log_dir %{_localstatedir}/log/%{_project_name}

# RPM Building folder
%define _build_root_project %{buildroot}%{_project_install_dir}

# -------------------------------------------------------------------------------------------- #
# prep section, setup macro:
# -------------------------------------------------------------------------------------------- #
%prep
# read from SOURCES, write into BUILD

echo "[INFO] Preparing installation"
# Create rpm/BUILDROOT folder
rm -Rf $RPM_BUILD_ROOT && mkdir -p $RPM_BUILD_ROOT
[ -d %{_build_root_project} ] || mkdir -p %{_build_root_project}

# Copy all from src to rpm/BUILD
cp -R  %{_srcdir}/src \
       %{_srcdir}/pom.xml \
       %{_srcdir}/README.md \
       %{_builddir}

# Copy "extra files" from rpm/SOURCES to rpm/BUILDROOT
cp -R %{_sourcedir}/* %{_builddir}

# -------------------------------------------------------------------------------------------- #
# Build section:
# -------------------------------------------------------------------------------------------- #
%build
# Read from BUILD, write into BUILD


# -------------------------------------------------------------------------------------------- #
# pre-install section:
# -------------------------------------------------------------------------------------------- #
%pre
# Read from BUILD, write into BUILDROOT

echo "[INFO] Creating %{_project_user} user"
getent group  %{_project_user} >/dev/null || groupadd -r %{_project_user}
getent passwd %{_project_user} >/dev/null || useradd -r -g %{_project_user} -m -s /bin/bash -c 'Cygnus user account' %{_project_user}

# -------------------------------------------------------------------------------------------- #
# Install section:
# -------------------------------------------------------------------------------------------- #
%install
# Read from BUILD and write into BUILDROOT
# RPM_BUILD_ROOT = BUILDROOT

echo "[INFO] Installing the %{name}"

echo "[INFO] Creating the directories"
mkdir -p %{_build_root_project}/init.d
# Create folder to store the PID (used by the Service)
mkdir -p %{buildroot}/var/run/%{_project_name}
# Create log folder
mkdir -p %{buildroot}/${_log_dir}
# Create /etc/cron.d directory
mkdir -p %{buildroot}/etc/cron.d
# Create /etc/logrotate.d directory
mkdir -p %{buildroot}/etc/logrotate.d
# create /etc/cygnus
mkdir -p %{buildroot}/etc/%{_project_name}
# create /etc/init.d
mkdir -p %{buildroot}/etc/init.d
# create /usr/bin
mkdir -p %{buildroot}/usr/bin

cp -R %{_builddir}/usr/cygnus/*                       %{_build_root_project}
cp %{_builddir}/init.d/%{_service_name}               %{_build_root_project}/init.d/%{_service_name}
cp %{_builddir}/config/*                              %{_build_root_project}/conf/
cp %{_builddir}/cron.d/cleanup_old_cygnus_logfiles    %{buildroot}/etc/cron.d
cp %{_builddir}/logrotate.d/logrotate-cygnus-daily    %{buildroot}/etc/logrotate.d

ln -s %{_project_install_dir}/init.d/%{_service_name}  %{buildroot}/etc/init.d/%{_service_name}
ln -s %{_project_install_dir}/conf                     %{buildroot}/etc/%{_project_name}/conf
ln -s %{_project_install_dir}/bin/flume-ng             %{buildroot}/usr/bin/flume-ng

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post

#Logs
echo "[INFO] Creating log directory"
mkdir -p %{_log_dir}
chown %{_project_user}:%{_project_user} %{_log_dir}
chmod g+s %{_log_dir}
setfacl -d -m g::rwx %{_log_dir}
setfacl -d -m o::rx %{_log_dir}

echo "Done"

# -------------------------------------------------------------------------------------------- #
# pre-uninstall section:
# -------------------------------------------------------------------------------------------- #
%preun

/sbin/service %{_service_name} stop


# -------------------------------------------------------------------------------------------- #
# post-uninstall section:
# clean section:
# -------------------------------------------------------------------------------------------- #
%postun


%clean
rm -rf $RPM_BUILD_ROOT


# -------------------------------------------------------------------------------------------- #
# Files to add to the RPM
# -------------------------------------------------------------------------------------------- #
%files
%defattr(755,%{_project_user},%{_project_user},755)
%attr(0644, root, root) /etc/cron.d/cleanup_old_cygnus_logfiles
%attr(0644, root, root) /etc/logrotate.d/logrotate-cygnus-daily
%attr(0777, root, root) /etc/cygnus/conf
%attr(0777, root, root) /etc/init.d/cygnus
%attr(0777, root, root) /usr/bin/flume-ng

%{_project_install_dir}
/var/run/%{_project_name}

%changelog
* Tue Feb 16 2016 Francisco Romero <francisco.romerobueno@telefonica.com> 0.12.1
- [BUG] Fix wrong spec date regarding release/0.12.0 (#750)
- [BUG] Fix the name of the fiware service path field in all the sinks (#764)
- [BUG] Fix the generalized Hive-like encoding style used in OrionHDFSSink (#781)

* Mon Feb 01 2016 Francisco Romero <francisco.romerobueno@telefonica.com> 0.12.0
- [FEATURE] Add postgreSQL sink support (#511)
- [FEATURE] Add batching support to OrionTestSink (#572)
- [HARDENING] Add the minimum HW requirements (#640)
- [HARDENING] Rename the HTTP and Flume header constants (#662)
- [HARDENING] Remove the dual batch accumulation in OrionSink (#664)
- [HARDENING] Add "requests" package as a requirement for cygnus_translator_pre0.10.0_to_0.10.0_ckan.py (#667)
- [HARDENING] Allow SSL connections to CKAN servers in cygnus_translator_pre0.10.0_to_0.10.0_ckan.py (#666)
- [BUG] Fix the grouped destination when using batches (#675)
- [HARDENING] Add the maximum accepted batch size in OrionDynamoDBSink (#672)
- [HARDENING] Add interface and implementation to MongoBackend (#654)
- [FEATURE] Add a general data_model parameter (#659)
- [HARDENING] Add grouping_rules.conf & flume-env.sh configuration files in the documentation (#657)
- [BUG] Use pagination when retrieving all the records to backup in cygnus_translator_pre0.10.0_to_0.10.0_ckan.py (#665)
- [FEATURE] Enable per-user or default Hive database creation in OrionHDFSSink (#516)
- [HARDENING] Document the service_as_namespace OrionHDFSSink parameter (#692)
- [HARDENING] Add a piece of documentation about multitenancy (#607)
- [BUG] Fix the log file when running as a service (#656)
- [HARDENING] Add a piece of documentation about required dependencies to be manually installed when building and installing without dependencies (#635)
- [HARDENING] Add a configurable value for CSV separator in OrionHDFSSink (#495)
- [HARDENING] Rename initializeBatching with initialize in all the sinks (#704)
- [FEATURE] Use TimeInstant (when available) instead of the reception time in OrionSTHSink (#651)
- [HARDENING] Do rollbacking of batches (#563)
- [HARDENING] Include service and servicePath in logs (#707)
- [HARDENING] Fix libthrift installation (#706)
- [BUG] Fix of the Cygnus installation using yum (#652)
- [BUG] Update links referring to sinks documentation (#713)
- [HARDENING] Finish a transaction only when it is really persisted, not rollbacked (#715)
- [FEATURE] Add batching support to OrionMongoSink (#570)
- [HARDENING] Document the Grouping Rules in the Installation and Administration Guide (#658)
- [HARDENING] Update Java and Fix which in docker (#709)
- [HARDENING] Document how to connect Orion and Cygnus (#726)
- [BUG] Fix some typos in agent.conf.template and OrionMySQLSink.md (#729)

* Fri Dec 04 2015 Francisco Romero <francisco.romerobueno@telefonica.com> 0.11.0
- [RELEASE] Maintenance tasks in fiware-cygnus Git repository (#402)
- [FEATURE] Add support to batch processing within a transaction in OrionCKANSink (#567)
- [HARDENING] Remove unnecessary http mock in OrionHDFSSinkTest and fix some output messages (#605)
- [HARDENING] Trace the table_type parameter in OrionMySQLSink (#614)
- [HARDENING] Add enable_grouping parameter for OrionKafkaSink in agent.conf.template (#615)
- [FEATURE] Add OrionDynamoSink (#584)
- [HARDENING] Add flume-env.sh.template file to the configuration folder (#613)
- [HARDENING] Documentation refactoring (#611)
- [HARDENING] Change the name of the default log file, from flume.log to cygnus.log (#622)
- [BUG] Escape all the non-alphanumeric characters in Hive fields of column-like tables (#619)
- [FEATURE] The package name now has the Hadoop Core version Cygnus is compatible with (#565)
- [BUG] OrionTestSink now inherits the configuration from OrionSink base class (#632)
- [HARDENING] Add administration and programmers sections to all the sinks documentation (#631)
- [FEATURE] Add some interesting fields to CKAN persisted data (servicePath in row-like modes, servicePath, entityId and entityType in column-like modes), including migration script (#543)
- [FEATURE] Add batching support to OrionKafkaSink (#569)
- [HARDENING] Add the Quick Start Guide to readthedocs (#645)
- [HARDENING] Add a document containing a table in charge of relating features and Cygnus version (#638)

* Wed Nov 04 2015 Francisco Romero <francisco.romerobueno@telefonica.com> 0.10.0
- [HARDENING] Cygnus user creation added to the from the sources installation guide (#558)
- [FEATURE] Add a binary implementation of the HDFS backend (#537)
- [HARDENING] Add docker as an option in the README for installing Cygnus (#552)
- [FEATURE] Add support to batch processing within a transaction in OrionHDFSSink (#554)
- [FEATURE] Add support to batch processing within a transaction in OrionMySQLSink (#568)
- [BUG] Add support to CKAN 2.4 API changes (#546)
- [BUG] Remove final line feed in the HDFS aggregation (#575)
- [FEATURE] Add some interesting fields to HDFS persisted data (servicePath in row-like modes, servicePath, entityId and entityType in column-like modes), including migration script (#544)
- [HARDENING] Document how to choose the hadoop-core dependency for compilation purposes (#559)
- [HARDENING] Add a batching timeout and accumulate the transaction IDs for right tracing (#562)
- [BUG] Ask for CKAN resources when populating a package cache after calling organization_show (#589)
- [FEATURE] Add some interesting fields to MySQL persisted data (servicePath in row-like modes, servicePath, entityId and entityType in column-like modes), including migration script (#501)
- [BUG] Fix the CKAN resource name building, removing references to old default destination (#592)
- [FEATURE] Allow enabling/disabling Hive in OrionHDFSSink (#555)
- [HARDENING] Explain the batching mechanism in the performance document (#564)
- [HARDENING] Fix the documentation regarding the installation from sources (#596)
- [BUG] Add extra fields (servicePath in row-like modes, servicePath, entityId and entityType in column-like modes) to Hive tables (#598)
- [FEATURE] Column-like persistence in OrionMongoSink (#548)

* Fri Oct 02 2015 Francisco Romero <francisco.romerobueno@telefonica.com> 0.9.0
- [FEATURE] Add support for multiple file formats in HDFS; JSON is maintained and CSV is added (#303)
- [HARDENING] Add detailed information about reporting issues and contact information (#478)
- [HARDENING] Update the Quick Start Guide in order is is aligned with latest features (#490)
- [HARDENING] Remove patch supporting old versions of the CKAN API (<= 2.0) (#188)
- [FEATURE] The notified user agent is not checked anymore (#493)
- [FEATURE] Add OrionKafkaSink (#456)
- [HARDENING] Add missing configuration and documentation regarding OrionMongoSink and OrionSTHSink (#505)
- [FEATURE] Enable/disable grouping rules usage per sink (#447)
- [FEATURE] Add HiveServer2 support to OrionHDFSSink (#513)
- [FEATURE] Add Python-based clients both for HiveServer1 and HiveServer2 (#519)
- [FEATURE] Add Java-based clients both for HiveServer1 and HiveServer2 (#518)
- [HARDENING] Replace logs containing "HttpFS response" by "Server response" (#517)
- [BUG] Use a testing version of Zookeeper in OrionKafkaSink (#514)
- [BUG] Always create the Hive tables if not existing yet (#401)
- [HARDENING] Add {headers,body} structure to messages sent to Kafka (#512)
- [FEATURE] Allow selecting the table type (by service, servicePath or destination) (#540)
- [BUG] A second CKAN resource may be added to an existeng dataset in row mode (#280)
- [HARDENING] Add references to FIWARE and Cosmos Big Data Analysis GE in the README (#534)
- [BUG] entityId and entityType are now added to the CKAN resources when using OrionCKANSink in row mode (#539)

* Wed Jul 08 2015 Francisco Romero <francisco.romerobueno@telefonica.com> 0.8.2
- [BUG] Fix many errors in the docuemtnation (#435)
- [BUG] Fix OrionMySQLLink in the README (#442)
- [BUG] Fix MySQL connections, adding a permanent connection to each database/fiware-service (#445)
- [BUG] Fix mongo-sink appearance in sth-sink configuration (both template and README) (#449)
- [BUG] Fix OrionMySQLSink, time zone is not added to the timestamp fields (#441)
- [HARDENING] Link the Quick Start Guide from the README (#454)
- [BUG] Fix the grouping rules validator, now empty fields and non-numeric ids are not allowed (#460)
- [HARDENING] Add detailed explanation about the syntax of the grouping rules (#459)
- [FEATURE] OAuth2 support for OrionHDFSSink (#483)

* Mon May 25 2015 Francisco Romero <francisco.romerobueno@telefonica.com> 0.8.1
- [HARDENING] OrionHDFSSink parameters are now called "hdfs_*" instead of "cosmos_*" (#374)
- [HARDENING] Add a permament connection to the MySQL Backend (#364)
- [BUG] Add the original (and removed by OrionRESTHandler) slash character to fiware-servicePath (#403)
- [FEATURE] Use Json-like rules definition for pattern-based grouping (#387)
- [BUG] Set the Fiware-Service and Fiware-ServicePath maximum lenght to 50 characters (previously, it was 32 characters) (#406)
- [FEATURE] Add implementation details to the specific sinks documentation (#397)
- [BUG] Fix the origin date in OrionSTHSink (#413)
- [HARDENING] Remove unnecessary hfds_api parameter in OrionHDFSSink (#415)
- [FEATURE] Hashing based collections for OrionMongoSink and OrionSTHSink (#420)
- [HARDENING] Set data_model to collection-per-entity (#419)
- [BUG] Use multiple Fiware-ServicePaths in the sinks (#384)

* Thu May 07 2015 Francisco Romero <francisco.romerobueno@telefonica.com> 0.8.0
- Ordered death of Cygnus if the logging system fails or it is stoped (#320)
- Management interface port is not opened twice anymore (#302)
- Added a polling interval parameter for reloading the Flume configuration (#334)
- Bug fix, flume-conf.properties.template file from Apache Flume is not copied anymore to Cygnus folder (#348)
- Cygnus exits if the HTTPSource listening port is already in use (#340)
- Added OrionMongoSink (#363)
- Bug fixed: matching table name can be null (no Flume parameter is used) or wrong (#367)
- Add specific sink documents, pointing to them from the README (#322)
- UTC/Z time zone detail added to all the sink timestamps (#370)
- Added OrionSTHSink (#19)
- Multitenancy support in HDFS (#338)
- ISODate objects are used for timestamping in OrionMongoSink (#372)
- Let the origin offset for months in aggregated points starts by 1 instead of 0 (#381)

* Fri Mar 06 2015 Francisco Romero <francisco.romerobueno@telefonica.com> 0.7.1
- Added option to start/stop/status only one instance configured in Cygnus using init.d script (#332)
- Added a Quick Start Guide (#319)
- Added an explanation on the different configuration files in the README (#342)

* Fri Feb 20 2015 Francisco Romero <francisco.romerobueno@telefonica.com> 0.7.0
- Added Kerberos authentication in OrionHDFSSink (#290)
- Added posibility to start multiple instances of Cygnus (#299)
- Bug fixing: same port in log4j example about two Cygnus instances (#305)
- Bug fixing: error in configuration template (cygnusagent.sinks.hdfs-sink.krb5_auth.krb5_login_conf_file) (#308)
- Encourage the usage of FQDNs regarding HDFS namenodes when using Kerberos (#309)
- Fixed the RoundRoundChannelSelector, now it works for multiple storages (#298)
- Allow for infinite TTL (#236)
- Added OrionTestSink (#307)
- Fixed OrionMySQLSink logger (now it logs as OrionMySQLSink, not as OrionHDFSSink) (#321)

* Wed Dec 17 2014 Daniel Moran <daniel.moranjimenez@telefonica.com> 0.6.0
- Remove the "resource" prefixing feature from MySQL and HDFS (#224)
- Add the "fiware-servicePath" header as a valid field of the grouping mechanism (#215)
- fiware-servicePath header processing (#212)
- Define and validate a common character set for all service and all resource names (#207)
- Bug fixing: correctly read the URL in the NGSI testing scripts (#255)
- Bug fixing: Document the correct Cygnus version in the README (#259)
- "iot_support at tid dot es" as contact email (#260)
- Round-Robin-like Flume Channel Selector (#254)
- Tuning tips for increading the Cygnus performance (#199)
- Bug fixing: The CKAN organization is not created in column mode anymore (#181)
- Bug fixing: Correct treatment of a root ("/") fiware-servicePath (#263)
- Run the Jetty server supporting the management interface from the appropriate place (#232)
- Do the resource URL in CKAN points to "none" (#246)
- Include changelog in Cygnus spec (#269)
- Change the way the PID is determined (#219)
- Removed execution privileges from configuration files (#264)
- Document how to install and run Cygnus from RPM (#275)
- Discard invalid matching rules at DestinationExtractor (#271)

* Tue Nov 11 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.4.2
- Enable https connections in CKAN (#230)
- Bug fixing: solve a conflict with Monit when running Cygnus as a service (#214)
- Bug fixing: delete the "cygnus" user when removing the Cygnus RPM (#213)
- Bug fixing: fix the events TTL parameter in the configuration template (#210)
- Bug fixing: errors when using '.' in CKAN organization names (#200)
- Bug fixing: process notifications with no contextAttributeList (#194)

* Sun Oct 19 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.5.1
- Bug fixing: typo in the configuration template (#238)
- Bug fixing: wrong path for the matching table (#239)

* Thu Oct 02 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.5
- Usage of SAX parser for XML-based notifications (#201)
- Cygnus version and snapshot shown in the logs (#187)
- Document how a developer may build his/her own sink (#136)
- Pattern-based grouping into tables (#107)
- Bug fixig: process notifications with no contextAttributeList (#222)
- Bug fixing: do the RPM scripts do not change the ownership of the whole /var/run folder (#203)
- Bug fixing: process the "value" tag in XML notifications instead of "contextValue" (#227)

* Wed Sep 05 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.4.1
- Only Flume events related to a persistence error are reínjected in the agent channel (#52)
- A TTL has been added to the re-injected Flume events (#126)
- Cygnus version is now showed in the logs (#104)
- Manual build and RPM build both using the same lo4j.properties.template (#111)
- Usage of Timestamp Interceptor instead of custom timestamping mechanism (#143)
- Configurable Hive endpoint independent of the HDFS endpoint (#173)
- Multiple HDFS endpoint setup (#175)
- Migration from Cygnus 0.1 to 0.2 or higher has been documented (#135)
- Migration from ngsi2cosmos to Cygnus has been documented (#105)
- Alarms related to Cygnus have been documented (#112)

* Thu Jul 31 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.4
- TDAF-like logs (#109)
- Standardize the default Cygnus logs path (#91)
- Bug fixing: quotes appearing in CKAN resource values (PR #97)
- Script for removing old data within CKAN-based short term historic (#62)
- CKAN basic management script (PR #99)
- CKAN cleanup script (PR #98)

* Thu Jul 03 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.3
- Attribute metadata persistence (#41)
- Multi-tenancy features (#36)
- Per column attribute persistence (#54 #60 #51)
- Move reception timestamping from the sink to the source (#53)
- MySQL connector added as a pom dependency (#78)
- RPM building framework (#76)
- Relaxed Orion version checking (#70)
- MySQL Connector added to pom.xml (#78)
- Translation scripts from Cygnus 0.1 to Cygnus 0.3 (#65)
- Script for removing old data within MySQL-based short term historic (#63)

* Wed Jun 04 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.2.1
- Change the OrionMySQLSink database and table names, by removing the "cygnus_" part (#57)
- Fixed bug in CKAN insertion mechanism

* Tue Jun 03 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.2
- Support for complex attribute values, specifically, vectors and objects (#43)
- Json-like persistency, independently of the notification type (XML or Json) or the backend (#29)
- Persistence in a MySQL backend (#42)
- Persistence in a CKAN backend (basic functionality) (#31)
- HDFS dataset and Hive table creation at startup time (#13)
- Change package names accordingly to the new repo structure (#30)
- Unit tests (#18)
- Add a template for cygnus.conf (#37)
- README files in UTF-8 (#33)
- Avoid special characters in HDFS file names, CKAN datastores IDs and MySQL table names (#9)
- Refactor the sinks and the HDFS backends, getting common code (#34)
- Per column attribute persistence in MySQL sink (#50)
- Hive basic client (#26)
- Plague Tracker application (#27)
- Translation scripts for moving from Cygnus 0.1 to Cygnus 0.2 (#29)
- XML and Json simple and compound notifications examples for testing (#39)

* Thu Mar 20 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.1
- Parsing of simple (string-like values only) Json notifications (#8)
- Parsing of simple (string-like values only) XML notifications (#3)
- Persistence in a WebHDFS/HttpFS backend (#20)
- SFTP basic client
