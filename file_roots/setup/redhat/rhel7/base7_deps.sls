{% import "setup/redhat/rhel7/baserpms.jinja" as deps %}

base7_deps:
  file.managed:
    - names:
      - {{deps.baserpm_path}}/RPM-GPG-KEY-CentOS-7:
        - source: http://mirror.centos.org/centos/7/os/x86_64/RPM-GPG-KEY-CentOS-7
          source_hash: md5=c45e7e322681292ce4c1d2a6d392c4b5
      {% for rpm in deps.rpmlist %} 
      - {{deps.baserpm_path}}/{{rpm[0]}}:
        - source: http://mirror.centos.org/centos/7/os/x86_64/Packages/{{rpm[0]}}
          source_hash: md5={{rpm[1]}}
      {% endfor %}
    - makedirs: True
    - user: root
    - group: root
    - file_mode: 644
    - dir_mode: 755


