#!/usr/bin/env bash

set -euo pipefail

usage()
{
  echo "usage: $0 SOURCE.cc [OUTPUT]" >&2
  echo "configure optional dependency roots with A60_*_PREFIX variables" >&2
}

if (( $# < 1 || $# > 2 )); then
  usage
  exit 2
fi

script_dir=$(cd "$(dirname "$0")" && pwd)
repo_dir=$(cd "$script_dir/.." && pwd)
source_file=$1
output_file=${2:-${source_file%.cc}.exe}
compiler=${CXX:-g++}
geo_mode=${A60_GEO_MODE:-6}
rapidjson_include=${A60_RAPIDJSON_INCLUDE:-/usr/include/rapidjson}

# Local dependency roots formerly supplied by a60-build.sh. An explicit
# A60_* variable always wins, including an explicit empty value; otherwise
# fall back to the local root when it exists so hosts without the optional
# dependencies are left untouched.
resolve_dependency_root()
{
  local var_name=$1
  local default_path=$2
  local value=
  if [[ -v "$var_name" ]]; then
    value=${!var_name}
  elif [[ -d "$default_path" ]]; then
    value=$default_path
  fi
  printf '%s\n' "$value"
}

libtorrent_prefix=$(resolve_dependency_root A60_LIBTORRENT_PREFIX "$HOME/bin/H-libtorrent")
geolite2pp_prefix=$(resolve_dependency_root A60_GEOLITE2PP_PREFIX "$HOME/bin/H-geolite2pp")
izzi_include=$(resolve_dependency_root A60_IZZI_INCLUDE "$HOME/src/izzi/src")
cartofreako_projections_include=$(resolve_dependency_root A60_CARTOFREAKO_PROJECTIONS_INCLUDE "$HOME/src/cartofreako/src.projections")

compile_flags=(
  -std=gnu++20 -pthread -O2 -g -march=native
  -Wall -Wextra -Werror -Wno-unused-local-typedefs
  -D"a60_USE_GEO=$geo_mode"
  -I"$repo_dir/src"
  -I"$rapidjson_include"
)
link_flags=(-pthread -lssl -lcrypto)

add_prefix()
{
  local prefix=$1
  if [[ -n "$prefix" ]]; then
    compile_flags+=(-I"$prefix/include")
    if [[ -d "$prefix/lib64" ]]; then
      link_flags+=(-L"$prefix/lib64")
    else
      link_flags+=(-L"$prefix/lib")
    fi
  fi
}

add_prefix "$libtorrent_prefix"
add_prefix "$geolite2pp_prefix"

if [[ -n "$izzi_include" ]]; then
  compile_flags+=(-I"$izzi_include")
fi
if [[ -n "$cartofreako_projections_include" ]]; then
  compile_flags+=(-I"$cartofreako_projections_include")
fi

if [[ -n "$libtorrent_prefix" ]]; then
  link_flags+=(-ltorrent-rasterbar)
fi
case "$geo_mode" in
  0)
    ;;
  1)
    link_flags+=(-lGeoIP -lh3)
    ;;
  2|3|4|5|6)
    link_flags+=(-lgeolite2++ -lmaxminddb -lh3)
    ;;
  *)
    echo "unsupported A60_GEO_MODE: $geo_mode" >&2
    exit 2
    ;;
esac

"$compiler" "${compile_flags[@]}" "$source_file" -o "$output_file" \
  "${link_flags[@]}"
