#coding:utf-8
import datetime


class BaseImage(object):
    """
    A base image model, as can be searched for.
    """
    def __init__(self, release, platform, instance_type, architecture, region, virtualization):
        self.release = release
        self.platform = platform
        self.instance_type = instance_type
        self.architecture = architecture
        self.region = region
        self.virtualization = virtualization

    def __str__(self):
        return "{0}@{1} ({2} {3} {4})".format(self.release, self.region, self.architecture, self.instance_type,
                                              self.virtualization)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self)


class SearchImage(BaseImage):
    """
    An Image used to search for other images.
    """
    def matches(self, image):
        for attr in ["release", "platform", "instance_type", "architecture", "region", "virtualization"]:
            if getattr(self, attr) != getattr(image, attr):
                return False
        return True


class Image(BaseImage):
    """
    An image as presented in CloudImages.
    """
    def __init__(self, release, platform, stability, date, instance_type, architecture, region, ami_id, aki_id,
                 _, virtualization):

        super(Image, self).__init__(release, platform, instance_type, architecture, region, virtualization)

        self.date = datetime.datetime.strptime(date, "%Y%m%d")
        self.stability = stability
        self.ami_id = ami_id
        self.aki_id = aki_id
        self._ = _

    def __str__(self):
        return "{0}@{1}: {2} ({3} {4} {5})".format(self.release, self.region, self.date, self.architecture,
                                               self.instance_type, self.virtualization)