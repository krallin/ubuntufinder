#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import requests

from ubuntufinder.actions import _find_latest_release, _list_images, _find_image, find_image
from ubuntufinder.exceptions import LatestReleaseNotFound, ServiceUnavailable


class MockSession(object):
    def __init__(self, get):
        self.get = get

class MockResponse(object):
    def __init__(self, text):
        self.text = text


class FindLatestReleaseTestCase(unittest.TestCase):
    def test_url(self):
        def get(url):
            self.assertEqual("https://cloud-images.ubuntu.com/query/released.latest.txt", url)
            return MockResponse("raring	server	release	20130824")
        _find_latest_release(MockSession(get))

    def test_error_condition(self):
        get = lambda url: MockResponse("")
        self.assertRaises(LatestReleaseNotFound, _find_latest_release, MockSession(get))

    def test_finds_latest_release(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "releases.txt")) as f:
            data = f.read()
            get = lambda url: MockResponse(data)
        self.assertEqual("raring", _find_latest_release(MockSession(get)))


class ListImagesTestCase(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raring.txt")) as f:
            self.data = f.read()

    def test_url(self):
        def get(url):
            self.assertEqual("https://cloud-images.ubuntu.com/query/raring/server/released.current.txt", url)
            return MockResponse(self.data)
        _list_images("raring", MockSession(get))

    def test_entries(self):
        images = _list_images("raring", MockSession(lambda url: MockResponse(self.data)))

        self.assertEqual("raring", images[0].release)
        self.assertEqual("server", images[1].platform)
        self.assertEqual("release", images[2].stability)
        self.assertEqual(2013, images[3].date.year)
        self.assertEqual(8, images[3].date.month)
        self.assertEqual(24, images[3].date.day)
        self.assertEqual("ebs", images[4].instance_type)
        self.assertEqual("i386", images[5].architecture)
        self.assertEqual("ap-southeast-1", images[6].region)
        self.assertEqual("ami-ecf4bcbe", images[7].ami_id)
        self.assertEqual("aki-31990e0b", images[8].aki_id)
        self.assertEqual("paravirtual", images[9].virtualization)
        self.assertEqual("hvm", images[12].virtualization)

    def test_find_image(self):
        self.assertEqual("ami-cfd4cfbb", _find_image("eu-west-1", "raring", "i386", "ebs", "paravirtual",
                                                     MockSession(lambda url: MockResponse(self.data))).ami_id)

    def test_find_latest_image(self):
        def get(url):
            if "raring" in url:
                return MockResponse(self.data)
            else:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "releases.txt")) as f:
                    return MockResponse(f.read())

        self.assertEqual("ami-7d317314", find_image("us-east-1", _session=MockSession(get)).ami_id)


class ServiceUnavailableTestCase(unittest.TestCase):
    def test_service_unavailable(self):
        def get(url):
            raise requests.RequestException()

        self.assertRaises(ServiceUnavailable, find_image, "us-east-1", _session=MockSession(get))


if __name__ == '__main__':
    unittest.main()
