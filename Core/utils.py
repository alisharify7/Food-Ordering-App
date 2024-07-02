
import uuid
import pickle
import pathlib
import datetime
import os.path
import string
import random
from urllib.parse import urlparse as url_parse

import khayyam
from PIL import Image, UnidentifiedImageError
from celery import Celery, Task
from celery import shared_task
from flask import Flask, current_app, request, session
from werkzeug.utils import secure_filename as werkzeug_secure_filename

SysRandom = random.SystemRandom()


def generate_random_string(length: int = 6, punctuation: bool = True) -> str:
    """generate random strings

     params:
        length: int  = length of random string - default is 6
        punctuation: bool = punctuation in random string or not

     return:
        str: string: random string
     """
    letters = string.ascii_letters
    if punctuation:
        letters += string.punctuation
    random_string = SysRandom.choices(letters, k=length)

    return "".join(random_string)


def get_next_page(fall_back_url: str = '') -> str:
    """
    use this method for validating next params in url
    validate http url args next=some url
    """
    next_page = request.args.get("next", False)
    if not next_page or url_parse(next_page).netloc != "":
        next_page = fall_back_url

    return next_page


def userLocalSelector():
    """
        this function select user local base on session
    """
    try:
        return session.get("language", "fa")
    except:
        return "en"



def make_file_name_secure(name: str, round:int=3):
    """This function make sure a file name is secure
    remove dangerous characters and add  uuid to first of file name
    """
    name = name.replace(" ", "")
    name = werkzeug_secure_filename(name)
    return f"{''.join([uuid.uuid4().hex for _ in range(round)])}-{datetime.datetime.utcnow().date()}-{name}"


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        """Every time a task is added to queue
         __call__ ...
        """

        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def compress_image(image, quality: int = 50):
    """
    compress image size
    Args:
    """
    if not os.path.exists(image):
        return False
    image = Image.open(image)
    image.save(image, optimize=True, quality=quality)
    return True

@shared_task(store_result=True)
def add_watermark(logo_full_path: str, filename, outputname: str, position="bottomleft", scale: int = 15,
                  padding: int = 5):
    """
    github: repo https://github.com/theitrain/watermark
    Add a watermark to images in the specified directory.

    Args:
    - directory (str): The directory containing images to be watermarked.
    - logo_path (str): Path to the watermark logo.
    - position (str): Position of the watermark on the image.
    - new_directory (str): Directory to save watermarked images.
    - padding (int): Padding around the logo in pixels.
    - outputname (str) : name of the out put file
    """

    def back(v):
        return pickle.dumps(v)

    try:
        original_logo = Image.open(logo_full_path)
    except UnidentifiedImageError:
        print(f"Failed to read logo from {logo_full_path}. Ensure it's a valid image format.")
        return back(False)
    except Exception as e:
        print(f"An error occurred: {e}")
        return back(False)

    # Check if the logo has an alpha channel
    if original_logo.mode == 'RGBA':
        logo_mask_original = original_logo.split()[3]
    else:
        logo_mask_original = None

    filename = pathlib.Path(filename)
    compress_image(image=filename)
    if filename.suffix.lower() not in current_app.config.get("IMAGE_EXT_SAVE", []):
        print("invalid image extension")
        return back(False)

    try:
        image = Image.open(filename)
    except UnidentifiedImageError:
        print(f"Skipped {filename}. Unsupported image format.")
        return back(False)
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}")
        return back(False)

    image = Image.open(filename)
    imageWidth, imageHeight = image.size

    shorter_side = min(imageWidth, imageHeight)
    new_logo_width = int(shorter_side * scale / 100)
    logo_aspect_ratio = original_logo.width / original_logo.height
    new_logo_height = int(new_logo_width / logo_aspect_ratio)

    # Resize the logo and its mask
    logo = original_logo.resize((new_logo_width, new_logo_height))
    if logo_mask_original:
        logo_mask = logo_mask_original.resize((new_logo_width, new_logo_height))
    else:
        logo_mask = None

    paste_x, paste_y = 0, 0

    if position == 'topleft':
        paste_x, paste_y = padding, padding
    elif position == 'topright':
        paste_x, paste_y = imageWidth - new_logo_width - padding, padding
    elif position == 'bottomleft':
        paste_x, paste_y = padding, imageHeight - new_logo_height - padding
    elif position == 'bottomright':
        paste_x, paste_y = imageWidth - new_logo_width - padding, imageHeight - new_logo_height - padding
    elif position == 'center':
        paste_x, paste_y = (imageWidth - new_logo_width) // 2, (imageHeight - new_logo_height) // 2

    try:
        image.paste(logo, (paste_x, paste_y), logo_mask)
    except Exception as e:
        print(f"An error occurred: {e}")
        return back(False)

    # Check if the image mode is 'RGBA' and convert it to 'RGB'
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    filenames = []
    IMAGEquality = 95
    uniqueCode = uuid.uuid4().hex + uuid.uuid4().hex
    for h, w in [[128, 64], [256, 128], [480, 256], [640, 480], [720, 640], [1080, 720], [1920, 1080], [3000, 2000]]:
        new_image = image.resize((h, w))
        name = f'{w}x{h}-{outputname}'
        save_path = current_app.config.get("PRODUCT_IMAGE_STORAGE") / name
        new_image.save(save_path, optimize=True, quality=IMAGEquality)
        IMAGEquality -= 5
        filenames.append(name)

    original_logo.close()
    image.close()

    return pickle.dumps(filenames)

class TimeStamp:
    """
        a base class for working with time&times in app
        ~!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!~
        #todo :
            add some utils for calculate and some stuff like that on date and times
    """

    __now_gregorian = None
    __now_jalali = None
    __now_timestamp = None
    __now_time = None

    def __init__(self):
        # constructor method
        self.__now_jalali = self.now_jalali()
        self.__now_gregorian = self.now_gregorian()
        self.__now_timestamp = self.now_unixtime()
        self.__now_time = self.now_time()

    @property
    def time(self):
        """Return time That Object created"""
        return self.__now_time

    @property
    def gregorian(self):
        """Return Gregorian time That Object created"""
        return self.__now_gregorian

    @property
    def jalali(self):
        """Return Jalali time That Object created"""
        return self.__now_jalali

    @property
    def timestamp(self):
        """Return timestamp time That Object created"""
        return self.__now_timestamp

    @staticmethod
    def now_time():
        """this method return now time"""
        return datetime.datetime.now().time()

    @staticmethod
    def now_unixtime():
        """this method return now time in unix time"""
        return int(datetime.datetime.now().timestamp())

    @staticmethod
    def now_gregorian():
        """this method return now time in gregorian time"""
        return datetime.date.today()

    @staticmethod
    def now_jalali():
        """this method return now time in jalali format"""
        return khayyam.JalaliDate.today()

    @staticmethod
    def is_persian_date(date: str) -> bool:
        """
            This function take a  date in format of string
            and check its valid jalali persian date or not
        """
        date = date.split("/")
        if len(date) == 3:
            try:
                khayyam.JalaliDate(year=date[0], month=date[1], day=date[2])
            except Exception as e:
                return False
            else:
                return True

        return False

    def convert_jlj2_georgian_d(self, value: khayyam.JalaliDate):
        """
            this method get a khayyam date<jalali> and convert it to gregorian object datetime.date
        """
        if not isinstance(value, khayyam.JalaliDate):
            raise ValueError(f"input {value} must be a khayyam.JalaliDate instance")
        year, month, day = value.year, value.month, value.day
        date = self._jalali_to_gregorian(year, month, day)
        return datetime.date(year=date[0], month=date[1], day=date[2])

    def convert_grg2_jalali_d(self, value: datetime.date):
        """
            this method get a datetime.date object and convert it o khayyam object
        """
        if not isinstance(value, datetime.date):
            raise ValueError(f"input {value} - {type(value)} must be a Datetime.Date instance")

        year, month, day = value.year, value.month, value.day
        date = self._gregorian_to_jalali(year, month, day)
        return khayyam.JalaliDate(year=date[0], month=date[1], day=date[2])

    def convert_jlj2_georgian_dt(self, value: khayyam.JalaliDatetime):
        """
            this method get a khayyam date<jalali> and convert it to gregorian object datetime.datetime
        """
        if not isinstance(value, khayyam.JalaliDatetime):
            raise ValueError("input must be a khayyam.JalaliDatetime instance")

        year, month, day, hour, minute, second, microsecond = value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond
        date = self._jalali_to_gregorian(year, month, day)
        return datetime.datetime(year=date[0], month=date[1], day=date[2], hour=hour, minute=minute, second=second,
                                 microsecond=microsecond)

    def convert_grg2_jalali_dt(self, value: datetime.datetime):
        """
            this method get a datetime.date object and convert it o khayyam.KhayyamDatetime object
        """
        year, month, day, hour, minute, second, microsecond = value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond
        date = self._gregorian_to_jalali(year, month, day)
        return khayyam.JalaliDatetime(year=date[0], month=date[1], day=date[2], hour=hour, minute=minute, second=second,
                                      microsecond=microsecond)

    def _gregorian_to_jalali(self, gy, gm, gd):
        """
            this method convert a Gregorian to a Jalali date
            https://jdf.scr.ir/
        """
        g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        if (gm > 2):
            gy2 = gy + 1
        else:
            gy2 = gy
        days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
        jy = -1595 + (33 * (days // 12053))
        days %= 12053
        jy += 4 * (days // 1461)
        days %= 1461
        if (days > 365):
            jy += (days - 1) // 365
            days = (days - 1) % 365
        if (days < 186):
            jm = 1 + (days // 31)
            jd = 1 + (days % 31)
        else:
            jm = 7 + ((days - 186) // 30)
            jd = 1 + ((days - 186) % 30)
        return [jy, jm, jd]

    def _jalali_to_gregorian(self, jy, jm, jd):
        """
            this method convert a Jalali time to a Gregorian time
            https://jdf.scr.ir/
        """
        jy += 1595
        days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
        if (jm < 7):
            days += (jm - 1) * 31
        else:
            days += ((jm - 7) * 30) + 186
        gy = 400 * (days // 146097)
        days %= 146097
        if (days > 36524):
            days -= 1
            gy += 100 * (days // 36524)
            days %= 36524
            if (days >= 365):
                days += 1
        gy += 4 * (days // 1461)
        days %= 1461
        if (days > 365):
            gy += ((days - 1) // 365)
            days = (days - 1) % 365
        gd = days + 1
        if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
            kab = 29
        else:
            kab = 28
        sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gm = 0
        while (gm < 13 and gd > sal_a[gm]):
            gd -= sal_a[gm]
            gm += 1
        return [gy, gm, gd]

    def convert_string_jalali2_dateD(self, value: str) -> datetime.date:
        """
            this Method converts a string (Persian Date) to datetime.date object
        """
        if not self.is_persian_date(value):
            raise ValueError("Input is not a valid date format YYYY/MM/DD")

        value = value.split("/")
        jDate = khayyam.JalaliDate(year=value[0], month=value[1], day=value[2])
        return self.convert_jlj2_georgian_d(jDate)

    def bigger_date(self, date1, date2):
        """
           this method takes two dates and returns the biggest date
            :params: date1, date2
            - if both dates are equal return True
            - if date1 is biggest return date1
            - if date2 is biggest return date2
        """
        if date1 > date2:
            return date1
        elif date2 > date1:
            return date2
        else:
            return True

    def smaller_date(self, date1, date2):
        """
            this method takes two dates and returns the smallest date
            :params: date1, date2
            - if both dates are equal return True
            - if date1 is smallest return date1
            - if date2 is smallest return date2
        """
        if date1 < date2:
            return date1
        elif date2 < date1:
            return date2
        else:
            return True