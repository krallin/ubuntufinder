#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import StringIO

import requests

from ubuntufinder.exceptions import ImageNotFound, ReleaseNotFound
from ubuntufinder.models import SearchImage, Image


CLOUD_IMAGES_SERVER = "https://cloud-images.ubuntu.com/query" # The server that serves the Cloud Images
CLOUD_IMAGES_LIST_FILE = "released.current.txt"
CLOUD_IMAGES_RELEASES_FILE = "released.latest.txt"

LATEST = "latest"  # Code to search for the latest release


def _find_latest_release(_session=None):
    """
    :returns: The latest stable (non-devel) Ubuntu release
    :rtype: str
    """
    session = _session or requests.Session()


    url = "/".join([CLOUD_IMAGES_SERVER, CLOUD_IMAGES_RELEASES_FILE])
    res = session.get(url) #TODO: If error!
    reader = csv.reader(StringIO.StringIO(res.text), delimiter="\t")

    latest_release = None
    for release, platform, status, date in reader:
        if status == "release":
            latest_release = release

    if latest_release is None:
        raise ReleaseNotFound()

    return latest_release


def _list_images(release, _session=None):
    """
    :rtype: list of ubuntufinder.models.Image
    """
    session = _session or requests.Session()

    url = "/".join([CLOUD_IMAGES_SERVER, release, "server", CLOUD_IMAGES_LIST_FILE])
    res = session.get(url) #TODO: If error!
    reader = csv.reader(StringIO.StringIO(res.text), delimiter="\t")

    return [Image(*entry) for entry in reader]


def _find_image(region, release, architecture, instance_type, virtualization, _session=None):
    """
    :rtype: ubuntufinder.models.Image
    """
    search_image = SearchImage(release, "server", instance_type, architecture, region, virtualization)

    for image in _list_images(release, _session):
        if search_image.matches(image):
            return image

    raise ImageNotFound()


def find_image(region, release=LATEST, architecture="amd64", instance_type="ebs", virtualization="paravirtual",
               _session=None):
    """
    Return a full image specification according to the query parameters

    :param region: The AWS region code to locate the Image in
    :type region: str

    :param release: The codename of the Ubuntu Release to locate. Defaults to the latest release
    :type release: str

    :param architecture: The CPU Architecture to find the image for. Defaults to amd64
    :type architecture: str

    :param instance_type: The Instance type to find the image for (ebs or instance-store). Defaults to ebs.
    :type instance_type: str

    :param virtualization: The virtualization technology to find the image for (paravirtual or hvm).
    :type virtualization: str
    """
    if release == LATEST:
        release = _find_latest_release(_session)

    return _find_image(region, release, architecture, instance_type, virtualization, _session)
