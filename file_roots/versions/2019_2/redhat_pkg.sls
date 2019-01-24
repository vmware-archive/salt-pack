{% import "setup/redhat/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'rhel7' %}

    - pkg.libsodium.1_0_16.rhel7        ## EPEL     1.0.16-1.el7
##     - pkg.libtomcrypt.1_17.rhel7     ## extras   1.17-26.el7
##     - pkg.libtommath.0_42_0.rhel7    ## extras   0.42.0-6.el7
    - pkg.openpgm.5_2_122.rhel7         ## EPEL     5.2.122-2.el7
    - pkg.openssl.1_0_2k.rhel7        ## base     1:1.0.2k-16.el7
##    - pkg.python-chardet.2_2_1.rhel7  ## base     2.2.1-1.el7_1
    - pkg.python-cherrypy.5_6_0.rhel7   ## base     3.2.2-4.el7
    - pkg.python-crypto.2_6_1.rhel7     ## extras   2.6.1-1.el7.centos
    - pkg.python-pycryptodome.3_6_1.rhel7   ## EPEL python2-pycryptodomex.x86_64    3.7.0-1.el7
##    - pkg.python-enum34.1_0.rhel7     ## base     1.0.4-1.el7
##    - pkg.python-futures.3_0_3.rhel7  ## base     python2-futures     3.1.1-5.el7
    - pkg.python-ioflo.1_3_8.rhel7
    - pkg.python-libcloud.2_0_0.rhel7   ## EPEL     python2-libcloud    2.0.0rc2-1.el7
    - pkg.python-libnacl.1_6_1.rhel7
    - pkg.python-m2crypto.0_31_0.rhel7  ## base     0.21.1-17.el7
    - pkg.python-msgpack.0_4_6.rhel7    ## EPEL     python2-msgpack     0.5.6-4.el7
    - pkg.python-mock.1_0_1.rhel7       ## extras   1.2.17-1.el7.centos
    - pkg.python-psutil.2_2_1.rhel7     ## EPEL     python2-psutil      2.2.1-4.el7
    - pkg.python-pyzmq.15_3_0.rhel7     ## EPEL     14.3.1-1.el7
    - pkg.python-raet.0_6_5.rhel7
    - pkg.python-simplejson.3_3_3.rhel7 ## EPEL     python2-simplejson  3.10.0-1.el7
    - pkg.python-timelib.0_2_4.rhel7
##    - pkg.python-tornado.4_2_1.rhel7  ## base     4.2.1-4.el7
    - pkg.python-typing.3_5_2_2.rhel7
##    - pkg.python-urllib3.1_10_2.rhel7 ## base     1.10.2-2.el7_1  available 1.10.2-5.el7
    - pkg.python-yaml.3_11.rhel7
    - pkg.salt.2019_2.rhel7
    - pkg.zeromq.4_1_4.rhel7            ## EPEL     4.1.4-5.el7

{% elif buildcfg.build_release == 'rhel6' %}

    - pkg.babel.0_9_4.rhel6
    - pkg.libgit2.0_20_0.rhel6
    - pkg.libsodium.0_4_5.rhel6
    - pkg.libtomcrypt.1_17.rhel6
    - pkg.libtommath.0_42_0.rhel6
    - pkg.libyaml.0_1_3.rhel6
    - pkg.pciutils.3_1_10.rhel6
    - pkg.python27.2_7_13.rhel6
    - pkg.python-backports.1_0.rhel6
    - pkg.python-backports-ssl_match_hostname.3_4_0_2.rhel6
    - pkg.python-chardet.3_0_4.rhel6
    - pkg.python-cherrypy.5_6_0.rhel6
    - pkg.python-crypto.2_6_1.rhel6
{% if buildcfg.build_arch == 'x86_64' %}
    - pkg.python-pycryptodome.3_6_1.rhel6
{% endif %}
    - pkg.python-enum34.1_0.rhel6
    - pkg.python-futures.3_0_3.rhel6
    - pkg.python-importlib.1_0_2.rhel6
    - pkg.python-idna.2_7.rhel6
    - pkg.python-ioflo.1_3_8.rhel6
    - pkg.python-ipaddress.1_0_18.rhel6
    - pkg.python-jinja2.2_8_1.rhel6
    - pkg.python-libcloud.2_0_0.rhel6
    - pkg.python-libnacl.1_6_1.rhel6
    - pkg.python-markupsafe.0_11.rhel6
    - pkg.python-msgpack.0_4_6.rhel6
    - pkg.python-mock.1_0_1.rhel6
    - pkg.python-nose.1_3_7.rhel6
    - pkg.python-pip.9_0_1.rhel6
    - pkg.python-psutil.5_4_2.rhel6
    - pkg.python-py.1_4_27.rhel6
    - pkg.python-pycurl.7_19_0.rhel6
    - pkg.python-pygit2.0_20_3.rhel6
    - pkg.python-pysocks.1_6_8.rhel6
    - pkg.python-pyzmq.14_5_0.rhel6
    - pkg.python-raet.0_6_6.rhel6
    - pkg.python-requests.2_7_0.rhel6
    - pkg.python-setuptools.36_6_0.rhel6
    - pkg.python-six.1_9_0.rhel6
    - pkg.python-timelib.0_2_4.rhel6
    - pkg.python-tornado.4_2_1.rhel6
    - pkg.python-urllib3.1_23.rhel6
    - pkg.python-yaml.3_11.rhel6
    - pkg.salt.2019_2.rhel6
    - pkg.yum-utils.1_1_30.rhel6
    - pkg.zeromq.4_0_5.rhel6

{% elif buildcfg.build_release == 'fedora' %}

    - pkg.salt.2019_2.fedora

{% endif %}
