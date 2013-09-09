#coding:utf-8
from __future__ import print_function

import argparse

from ubuntufinder.actions import LATEST, find_image


def main():
    parser = argparse.ArgumentParser("ubuntufinder",
                                     description="An utility tool to find the latest Ubuntu EC2 AMI IDs")
    parser.add_argument("region")
    parser.add_argument("-r", "--release", default=LATEST)
    parser.add_argument("-a", "--architecture", default="amd64")
    parser.add_argument("-i", "--instance-type", default="ebs")
    parser.add_argument("-v", "--virtualization", default="paravirtual")

    args = parser.parse_args()

    image = find_image(args.region, args.release, args.architecture, args.instance_type, args.virtualization)

    print(image.ami_id)



if __name__ == "__main__":
    main()
