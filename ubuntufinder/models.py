#coding:utf-8
import datetime


class BaseImage(object):
    """
    A base image model, as can be searched for.

    :ivar release: The Ubuntu release codename for this Image.
    :ivar platform: Set to server for Cloud Images.
    :ivar instance_type: The instance type supported by this Image (ebs or instance-store).
    :ivar architecture: The architecture for this Image (i386 or amd64)
    :ivar region: The region for this Image (us-east-1, etc.)
    :ivar virtualization: The virtualization technology for this Image (paravirtual of hvm)
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
        """
        Checks whether an image matches this search image.

        :param image: The Image to compare to the SearchImage
        :type image: BaseImage

        :returns: Whether the Image matches
        :rtype: bool
        """
        for attr in ["release", "platform", "instance_type", "architecture", "region", "virtualization"]:
            if getattr(self, attr) != getattr(image, attr):
                return False
        return True


class Image(BaseImage):
    """
    An image as presented in CloudImages.

    :ivar date: The date this Image was released
    :ivar stability: The stability of this Image (release or devel)
    :ivar ami_id: The AMI ID for this Image
    :ivar aki_id: The AKI ID for this Image
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