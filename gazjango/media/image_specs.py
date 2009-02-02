from imagekit       import processors
from imagekit.specs import ImageSpec

# TODO: hook this up to a JS cropper

# =============================
# = Custom Resizing Processor =
# =============================

def _resize(image, obj=None, width=None, height=None, crop=False, upscale=False):
    return type('RegularResize', (processors.Resize,), {
        'width': width,
        'height': height,
        'crop': crop,
        'upscale': upscale,
    }).process(image, obj)

class ProcessorImproperlyConfigured(Exception):
    pass

class FuzzyRatioResize(processors.Resize):
    """
    Has one "set" dimension and one "fuzzy" dimension:
        width = 350
        height_range = [130, 200]
    If a rescale would put us in that range, just do that; otherwise,
    we crop so that we lie within said range.
    """
    width = None
    height = None
    width_range = None
    height_range = None
    upscale = False
    
    @classmethod
    def process(cls, image, obj=None):
        cur_width, cur_height = image.size
        if cls.width:
            if cls.width_range or cls.height or not cls.height_range:
                raise ProcessorImproperlyConfigured
            
            ratio = float(cls.width) / cur_width
            min_height, max_height = cls.height_range
            desired_height = max(min(ratio * cur_height, max_height), min_height)
            
            return _resize(image, obj,
                width=cls.width,
                height=desired_height,
                crop=True,
                upscale=cls.upscale
            )
        elif cls.height:
            if cls.height_range or cls.width or not cls.width_range:
                raise ProcessorImproperlyConfigured
            
            ratio = float(cls.height) / cur_height
            min_width, max_width = cls.width_range
            desired_width = max(min(ratio * cur_width, max_width), min_width)
            
            return _resize(image, obj,
                width=desired_width,
                height=cls.height,
                crop=True,
                uspcale=cls.upscale
            )
        else:
            raise ProcessorImproperlyConfigured
    

# ======================
# = Story Front Images =
# ======================

class ResizeTopWideFront(FuzzyRatioResize):
    width = 350
    height_range = [120, 190]

class TopWideFront(ImageSpec):
    processors = [ResizeTopWideFront]


class ResizeTopTallFront(FuzzyRatioResize):
    width_range = [190, 250]
    height = 320

class TopTallFront(ImageSpec):
    processors = [ResizeTopWideFront]


class ResizeMidWideFront(FuzzyRatioResize):
    width = 280
    height_range = [100, 150]

class MidWideFront(ImageSpec):
    processors = [ResizeMidWideFront]


class ResizeMidTallFront(FuzzyRatioResize):
    width = 90
    height_range = [145, 185]

class MidTallFront(ImageSpec):
    processors = [ResizeMidTallFront]


# ======================
# = Other Story Images =
# ======================

class ResizeIssue(processors.Resize):
    height = 192
    width = 192
    # crop = True # TODO: not sure whether we want issue images cropped

class IssueImage(ImageSpec):
    processors = [ResizeIssue]


# class ResizeSpecial(processors.Resize):
#     height = 180
#     width = 180
#     crop = True
# 
# class SpecialImage(ImageSpec):
#     access_as = 'special'
#     processors = [ResizeIssue, ResizeSpecial]
# 

class ResizeThumb(processors.Resize):
    height = 80
    width = 50
    crop = True

class EnhanceThumb(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1

class Thumbnail(ImageSpec):
    processors = [ResizeThumb, EnhanceThumb]


class ResizeAdminThumb(processors.Resize):
    height = 100
    width = 200

class AdminThumb(ImageSpec):
    processors = [ResizeAdminThumb]

# ================
# = Other Images =
# ================
class ResizeProfile(processors.Resize):
    height = 175

class ProfilePic(ImageSpec):
    processors = [ResizeProfile]


# class ResizeAthleticsIcon(processors.Resize):
#     width = 70
#     height = 35
# 
# class AthleticsIcon(ImageSpec):
#     processors = [ResizeAthleticsIcon]
#

class ResizePhotospreadImage(processors.Resize):
    # bigger than the real size, so that lightbox does something
    height = 850
    width = 650
    crop = False
    upscale = False

class PhotospreadImage(ImageSpec):
    processors = [ResizePhotospreadImage]