 {% import "setup/amazon/map.jinja" as buildcfg %}

 ensure_user_access:
  file.directory:
    - name: {{buildcfg.build_dest_dir}}
    - user: {{buildcfg.build_runas}}
    - group: {{buildcfg.build_runas}}
    - dir_mode: 755
    - file_mode: 644
    - recurse:
        - user
        - group
        - mode
