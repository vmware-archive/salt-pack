{% import "setup/redhat/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'rhel7' %}

    - pkg.libsodium.1_0_16.rhel7        ## EPEL     1.0.16-1.el7
    - pkg.libtomcrypt.1_17.rhel7     ## extras   1.17-26.el7
    - pkg.libtommath.0_42_0.rhel7    ## extras   0.42.0-6.el7
    - pkg.openpgm.5_2_122.rhel7         ## EPEL     5.2.122-2.el7
    - pkg.openssl.1_0_2k.rhel7        ## base     1:1.0.2k-16.el7
    - pkg.python-backports_abc.0_5.rhel7
    - pkg.python-cherrypy.5_6_0.rhel7   ## base     3.2.2-4.el7
    - pkg.python-crypto.2_6_1.rhel7     ## extras   2.6.1-1.el7.centos
    - pkg.python-pycryptodome.3_6_1.rhel7   ## EPEL python2-pycryptodomex.x86_64    3.7.0-1.el7
    - pkg.python-futures.3_0_3.rhel7  ## base     python2-futures     3.1.1-5.el7
    - pkg.python-libcloud.2_0_0.rhel7   ## EPEL     python2-libcloud    2.0.0rc2-1.el7
    - pkg.python-m2crypto.0_31_0.rhel7  ## base     0.21.1-17.el7
    - pkg.python-msgpack.0_6_2.rhel7    ## EPEL     python2-msgpack     0.5.6-4.el7
    - pkg.python-mock.1_0_1.rhel7       ## extras   1.2.17-1.el7.centos
    - pkg.python-psutil.2_2_1.rhel7     ## EPEL     python2-psutil      2.2.1-4.el7
    - pkg.python-pyzmq.15_3_0.rhel7     ## EPEL     14.3.1-1.el7
    - pkg.python-setuptools.36_6_0.rhel7
    - pkg.python-simplejson.3_3_3.rhel7 ## EPEL     python2-simplejson  3.10.0-1.el7
    - pkg.python-singledispatch.3_4_0_3.rhel7
    - pkg.python-typing.3_5_2_2.rhel7
    - pkg.python-urllib3.1_10_2.rhel7 ## base     1.10.2-2.el7_1  available 1.10.2-5.el7
    - pkg.python-yaml.3_11.rhel7
    - pkg.salt.3000_9.rhel7
    - pkg.zeromq.4_1_4.rhel7            ## EPEL     4.1.4-5.el7

{% elif buildcfg.build_release == 'fedora' %}

    - pkg.salt.3000_0_0.fedora

{% endif %}

