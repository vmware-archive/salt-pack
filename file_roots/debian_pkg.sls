{% import "setup/debian/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'debian8' %}

    - pkg.bsdmainutils.9_0_6.debian8
    - pkg.libsodium.1_0_3.debian8
    - pkg.openpgm.5_2_122.debian8
    - pkg.python-cherrypy.2_3_0.debian8
    - pkg.python-croniter.0_3_4.debian8
    - pkg.python-crypto.2_6_1.debian8
    - pkg.python-enum34.1_0_4.debian8
    - pkg.python-future.0_14_3.debian8
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-ioflo.1_3_8.debian8
    - pkg.python-jinja2.2_7_3.debian8
    - pkg.python-libcloud.0_20_0.debian8
    - pkg.python-libnacl.4_1.debian8
    - pkg.python-msgpack.0_4_2.debian8
    - pkg.python-pyzmq.14_4_0.debian8
    - pkg.python-raet.0_6_3.debian8
    - pkg.python-requests.2_7_0.debian8
    - pkg.python-timelib.0_2_4.debian8
    - pkg.python-tornado.4_2_1.debian8
    - pkg.python-urllib3.1_10_4.debian8
    - pkg.python-yaml.3_11.debian8
    - pkg.salt.2015_8_8.debian8
    - pkg.zeromq.4_0_5.debian8

{% elif buildcfg.build_release == 'debian7' %}

    - pkg.bsdmainutils.9_0_3.debian7    # 9.0.3
    - pkg.libsodium.1_0_3.debian7       #
    - pkg.python-backports-ssl_match_hostname.3_4_0_2.debian7
    - pkg.openpgm.5_2_122.debian7       #
    - pkg.python-cherrypy.2_3_0.debian7 # 2.3.0-3
    - pkg.python-croniter.0_3_4.debian7 #
    - pkg.python-crypto.2_6_1.debian7   # 2.6-4+deb7u3 - going to use 2_6_1-5
    - pkg.python-enum34.1_0_4.debian7   #
    - pkg.python-future.0_14_3.debian7  #
    - pkg.python-futures.3_0_3.debian7  #
    - pkg.python-ioflo.1_3_8.debian7    #
    - pkg.python-jinja2.2_6.debian7     # 2.6-1
    - pkg.python-libcloud.0_20_0.debian7 #
    - pkg.python-libnacl.4_1.debian7    #
    - pkg.python-msgpack.0_3_0.debian7  # 0.3.0-1~bpo70+2
    - pkg.python-pyzmq.13_1_0.debian7   #
    - pkg.python-raet.0_6_3.debian7     #
    - pkg.python-requests.2_0_0.debian7 # 2.0.0-1~bpo70+2 wheezy-backports/main
    - pkg.python-timelib.0_2_4.debian7  #
    - pkg.python-tornado.4_2_1.debian7  # 2.3-2
    - pkg.python-urllib3.1_7_1.debian7  # 1.7.1-1~bpo70+1 wheezy-backports/main
    - pkg.python-yaml.3_10.debian7      # 3.10-4+deb7u1
    - pkg.salt.2015_8_8.debian7         #
    - pkg.zeromq.3_2_3.debian7          #

{% endif %}
