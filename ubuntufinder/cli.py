#coding:utf-8
from __future__ import print_function

import sys
import argparse

from ubuntufinder.actions import LATEST, find_image
from ubuntufinder.exceptions import ImageNotFound


def main():
    parser = argparse.ArgumentParser("ubuntufinder", description="An utility tool to find the latest Ubuntu EC2 AMI IDs")
    parser.add_argument("region", help="AWS Region to return an image ID for.")
    parser.add_argument("-r", "--release", default=LATEST, help="Release codename. Defaults to the latest release.")
    parser.add_argument("-a", "--architecture", default="amd64", help="Architecture. `amd64` or `i386`. Defauts to `amd64`.")
    parser.add_argument("-i", "--image-type", default="ebs", help="AWS image type. `ebs` or `instance-store`. Defaults to `ebs`.")
    parser.add_argument("-v", "--virtualization", default="paravirtual", help="Virtualization type. `paravirtual` or `hvm`. Defaults to `paravirtual`.")
    parser.add_argument('--instance-type')  # Legacy argument name

    args = parser.parse_args()

    # Legacy argument handling
    if args.instance_type is not None:
        print("WARNING: `--instance-type` is deprecated. Use `--image-type` instead", file=sys.stderr)
        image_type = args.instance_type
    else:
        image_type = args.image_type

    # Actual image location
    try:
        image = find_image(args.region, args.release, args.architecture, image_type, args.virtualization)
    except ImageNotFound:
        print("ERROR: No image found!", file=sys.stderr)
        sys.exit(1)

    print(image.ami_id)

if __name__ == "__main__":
    main()
