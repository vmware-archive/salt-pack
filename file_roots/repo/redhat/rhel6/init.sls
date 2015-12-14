{% import "setup/redhat/map.jinja" as buildcfg %}

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
    - order: last
