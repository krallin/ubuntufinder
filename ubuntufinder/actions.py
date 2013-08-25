#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import StringIO

import requests

from ubuntufinder.exceptions import ImageNotFound, ReleaseNotFound, ServiceUnavailable
from ubuntufinder.models import SearchImage, Image


CLOUD_IMAGES_SERVER = "https://cloud-images.ubuntu.com/query" # The server that serves the Cloud Images
CLOUD_IMAGES_LIST_FILE = "released.current.txt"
CLOUD_IMAGES_RELEASES_FILE = "released.latest.txt"
CLOUD_IMAGES_CSV_SEPARATOR = "\t"

LATEST = "latest"  # Code to search for the latest release


def _open_csv_from_url(url, _session=None):
    """
    :param url: The URL to open

    :returns: A CSV reader from the data at URL
    :rtype: :class:`csv.reader`
    """

    session = _session or requests.Session()
    try:
        res = session.get(url)
    except requests.RequestException as e:
        raise ServiceUnavailable(e)
    return csv.reader(StringIO.StringIO(res.text), delimiter=CLOUD_IMAGES_CSV_SEPARATOR)


def _find_latest_release(_session):
    """
    :returns: The latest stable (non-devel) Ubuntu release
    :rtype: str
    """

    url = "/".join([CLOUD_IMAGES_SERVER, CLOUD_IMAGES_RELEASES_FILE])
    reader = _open_csv_from_url(url, _session)

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

    url = "/".join([CLOUD_IMAGES_SERVER, release, "server", CLOUD_IMAGES_LIST_FILE])
    reader = _open_csv_from_url(url, _session)
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
    :type region: :class:`str`

    :param release: The codename of the Ubuntu Release to locate. Defaults to the latest release
    :type release: :class:`str`

    :param architecture: The CPU Architecture to find the image for. Defaults to amd64
    :type architecture: :class:`str`

    :param instance_type: The Instance type to find the image for (ebs or instance-store). Defaults to ebs.
    :type instance_type: :class:`str`

    :param virtualization: The virtualization technology to find the image for (paravirtual or hvm).
    :type virtualization: :class:`str`

    :returns: An Image corresponding to your search
    :rtype: :class:`ubuntufinder.models.Image`

    :raises: :class:`ubuntufinder.exceptions.ImageNotFound` if no match is found.
    :raises: :class:`ubuntufinder.exceptions.ServiceUnavailable` if Cloud Images can't be accessed.
    """

    if release == LATEST:
        release = _find_latest_release(_session)

    return _find_image(region, release, architecture, instance_type, virtualization, _session)
