{% import "setup/debian/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'debian9' %}

    - pkg.python-ioflo.1_6_7.debian9        ## need update to latest, was 1.3.8
    - pkg.python-jinja2.2_9_4.debian9
    - pkg.python-raet.0_6_7.debian9         ## need update to latest, was 0.6.3
    - pkg.python-timelib.0_2_4.debian9
    - pkg.salt.2019_2_3.debian9

{% elif buildcfg.build_release == 'debian8' %}

{% if buildcfg.build_arch == 'armhf' %}

    - pkg.libsodium.1_0_3.debian8
    - pkg.python-future.0_14_3.debian8
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-ioflo.1_3_8.debian8
    - pkg.python-libcloud.1_5_0.debian8
    - pkg.python-libnacl.4_1.debian8
    - pkg.python-pyzmq.14_4_0.debian8
    - pkg.python-raet.0_6_3.debian8
    - pkg.python-systemd.231.debian8
    - pkg.python-timelib.0_2_4.debian8
    - pkg.python-tornado.4_2_1.debian8
    - pkg.salt.2019_2_3.debian8
##    - pkg.zeromq.4_0_5.debian8            ## jessie libzmq3 4.0.5+dfsg-2+deb8u1

{% else %}
    - pkg.libsodium.1_0_3.debian8
##    - pkg.python-cherrypy.2_3_0.debian8   ## jessie 2.3.0-3
##    - pkg.python-croniter.0_3_4.debian8   ## jessie 0.3.4-1, jessie-backports 0.3.12-1~bpo8+1
##    - pkg.python-crypto.2_6_1.debian8     ## jessie 2.6.1-5+deb8u1
##    - pkg.python-enum34.1_0_4.debian8     ## jessie 1.0.3-1
##    - pkg.python-future.0_14_3.debian8    ## jessie 0.15.2-4~bpo8+1
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-ioflo.1_3_8.debian8
    - pkg.python-jinja2.2_9_4.debian8       ## jessie 2.7.3-1, jessie-backports 2.8-1~bpo8+1
    - pkg.python-libcloud.1_5_0.debian8     ## jessie 0.15.1-1
    - pkg.python-libnacl.4_1.debian8
##    - pkg.python-msgpack.0_4_2.debian8    ## jessie 0.4.2-1, jessie-backports 0.4.6-1~bpo8+1
##    - pkg.python-pyzmq.14_4_0.debian8     ## jessie 14.4.0-1
    - pkg.python-raet.0_6_3.debian8
    - pkg.python-systemd.231.debian8        ## jessie backports 233-1~bpo8+1
    - pkg.python-timelib.0_2_4.debian8
    - pkg.python-tornado.4_2_1.debian8      ## jessie 3.2.2-1.1, jessie-backports 4.4.3-1~bpo8+1
    - pkg.python-urllib3.1_10_4.debian8     ## jessie 1.9.1-3, jessie-backports 1.16-1~bpo8+1
##    - pkg.python-yaml.3_11.debian8        ## jessie 3.11-2
    - pkg.salt.2019_2_3.debian8
##    - pkg.zeromq.4_0_5.debian8            ## jessie libzmq3 4.0.5+dfsg-2+deb8u1

{% endif %}

{% endif %}
