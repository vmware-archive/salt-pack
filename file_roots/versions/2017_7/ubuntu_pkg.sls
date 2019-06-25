{% import "setup/ubuntu/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'ubuntu1804' %}

    - pkg.python-ioflo.1_5_0.ubuntu1804
    - pkg.python-raet.0_6_5.ubuntu1804
    - pkg.python-timelib.0_2_4.ubuntu1804
    - pkg.salt.2017_7.ubuntu1804

{% elif buildcfg.build_release == 'ubuntu1604' %}

##    - pkg.libsodium.1_0_8.ubuntu1604      ## xenial libsodium18 1.0.8-5
    - pkg.python-ioflo.1_5_0.ubuntu1604
    - pkg.python-libcloud.1_5_0.ubuntu1604
    - pkg.python-libnacl.4_1.ubuntu1604
    - pkg.python-raet.0_6_5.ubuntu1604
    - pkg.python-timelib.0_2_4.ubuntu1604
##    - pkg.python-tornado.4_2_1.ubuntu1604 ## xenial 4.2.1-1ubuntu3
    - pkg.salt.2017_7.ubuntu1604

{% endif %}
