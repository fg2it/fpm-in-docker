#!/usr/bin/env python3
import argparse
import datetime
import os
import subprocess
import sys
import yaml

cfg_file='version.yml'
DOCKERPWD = os.getenv('DOCKERPWD')

def docker_tag(version, iteration):
    docker_tag=version
    if iteration:
        docker_tag+='-{}'.format(iteration)
    return docker_tag

def build(version, iteration):
    build_date = datetime.datetime.utcnow().isoformat('T')+'Z'
    vcs_ref = subprocess.getoutput('git rev-parse --short HEAD')

    subprocess.call(
        ["docker", "build",
         "--pull",
         "--build-arg", "FPM_VERSION={}".format(version),
         "--build-arg", "BUILD_DATE={}".format(build_date),
         "--build-arg", "VCS_REF={}".format(vcs_ref),
         "--tag", "fg2it/fpm:{}".format(docker_tag(version, iteration)),
         "."
        ],
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=0
    )

def push(version, iteration):
    subprocess.call(
        ["docker", "login",
         "-u", "fg2it",
         "-p", DOCKERPWD
        ],
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=0
    )

    subprocess.call(
        ["docker", "push",
         "fg2it/fpm:{}".format(docker_tag(version, iteration))
        ],
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=0
    )

if __name__ == "__main__" :
    cfg = yaml.load( open(cfg_file ) )
    cfg['docker-iteration'] = cfg.get('docker-iteration', '')

    parser = argparse.ArgumentParser(description="Build/push fpm docker image")
    parser.add_argument("-b",
                        help="Build",
                        default=False,
                        action='store_true'
    )
    parser.add_argument("-p",
                        help="Push",
                        default=False,
                        action='store_true'
    )
    parser.add_argument("-d",
                        help="print setting from config file ({})".format(cfg_file),
                        action='store_true',
    )
    parser.add_argument("-f","--fpm-version",
                        help="fpm version to build",
                        default=cfg['fpm-version']
    )
    parser.add_argument("-i","--docker-iteration",
                        help="docker iteration",
                        default=cfg['docker-iteration']
    )

    args = parser.parse_args()

    if(args.d):
        print("{}:\n"
              "   fpm version:       {}\n"
              "   docker itertation: {}\n"
              "effective:\n"
              "   fpm version:       {}\n"
              "   docker itertation: {}"
              .format(cfg_file, cfg['fpm-version'], cfg['docker-iteration'],
                      args.fpm_version, args.docker_iteration)
        )
        sys.exit(0)

    if(args.b):
        build(args.fpm_version, args.docker_iteration)

    if(args.p):
        if not DOCKERPWD:
            print('No credential to push to dockerhub\n'
                  'Try DOCKERPWD=<pwd> {} ...'.format(sys.argv[0])
            )
            sys.exit(1)
        push(args.fpm_version, args.docker_iteration)