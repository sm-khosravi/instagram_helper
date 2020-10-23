# In The Name Of Allah
#
# Jalali date converter
# Example Usage:
#
#  >>> from app_07_utils.helper_functions.hf_12_date_converter import Gregorian, Persian
#
#  >>> Persian('1393-1-11').gregorian_string()
#  '2014-3-31'
#  >>> Persian(1393, 1, 11).gregorian_datetime()
#  datetime.date(2014, 3, 31)
#  >>> Persian('1393/1/11').gregorian_string("{}/{}/{}")
#  '2014/3/31'
#  >>> Persian((1393, 1, 11)).gregorian_tuple()
#  (2014, 3, 31)
#
#  >>> Gregorian('2014-3-31').persian_string()
#  '1393-1-11'
#  >>> Gregorian('2014,03,31').persian_tuple()
#  (1393, 1, 11)
#  >>> Gregorian(2014, 3, 31).persian_year
#  1393


# print(date_office.find(","))
# if date_office.find("/") > 0:
#     result = date_office.split("/")
# elif date_office.find(",") > 0:
#     result = date_office.split(",")
# elif date_office.find("_") > 0:
#     result = date_office.split("_")
# else:
#     return Response("date format invalid")
#
# date_office = "{0}-{1}-{2}".format(result[0], result[1], result[2])


import datetime
import re

# class ExceptionDateFormatInvalid(APIException):
#     status_code = 404
#     default_detail = u"فرمت تاریخ نامعتبر است"
# class ExceptionDateInvalid(APIException):
#     status_code = 404
#     default_detail = u"تاریخ وارد شده نامعتبر است"


class Gregorian:

    def __init__(self, *date):
        self.none_flag = False
        # Parse date
        if len(date) == 1:
            date = date[0]
            if type(date) is str:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', date)
                if m:
                    [year, month, day] = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
                else:
                    # raise ExceptionDateFormatInvalid()
                    raise Exception(u"فرمت تاریخ نامعتبر است")

            elif type(date) is datetime.date:
                [year, month, day] = [date.year, date.month, date.day]
            elif type(date) is tuple:
                year, month, day = date
                year = int(year)
                month = int(month)
                day = int(day)
            else:
                self.none_flag = True
                return
        elif len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        else:
            # raise ExceptionDateFormatInvalid()
            raise Exception(u"فرمت تاریخ نامعتبر است")

        # Check the validity of input date
        try:
            datetime.datetime(year, month, day)
        except:
            # raise ExceptionDateFormatInvalid()
            raise Exception(u"فرمت تاریخ نامعتبر است")

        self.gregorian_year = year
        self.gregorian_month = month
        self.gregorian_day = day

        # Convert date to Jalali
        d_4 = year % 4
        g_a = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        doy_g = g_a[month] + day
        if d_4 == 0 and month > 2:
            doy_g += 1
        d_33 = int(((year - 16) % 132) * .0305)
        a = 286 if (d_33 == 3 or d_33 < (d_4 - 1) or d_4 == 0) else 287
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 10) / 63) == 30:
            a -= 1
            b += 1
        if doy_g > b:
            jy = year - 621
            doy_j = doy_g - b
        else:
            jy = year - 622
            doy_j = doy_g + a
        if doy_j < 187:
            jm = int((doy_j - 1) / 31)
            jd = doy_j - (31 * jm)
            jm += 1
        else:
            jm = int((doy_j - 187) / 30)
            jd = doy_j - 186 - (jm * 30)
            jm += 7
        self.persian_year = jy
        self.persian_month = jm
        self.persian_day = jd

    def persian_tuple(self):
        if self.none_flag:
            return None
        return self.persian_year, self.persian_month, self.persian_day

    def persian_string(self, date_format="{}-{}-{}"):
        if self.none_flag:
            return None
        return date_format.format(self.persian_year, self.persian_month, self.persian_day)


class Persian:

    def __init__(self, *date):
        self.none_flag = False
        # Parse date
        if len(date) == 1:
            date = date[0]
            if type(date) is str:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', date)
                if m:
                    [year, month, day] = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
                else:
                    # raise ExceptionDateFormatInvalid()
                    raise Exception(u"فرمت تاریخ نامعتبر است")

            elif type(date) is tuple:
                year, month, day = date
                year = int(year)
                month = int(month)
                day = int(day)
            else:
                self.none_flag = True
                return
        elif len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        else:
            # raise ExceptionDateFormatInvalid()
            raise Exception(u"فرمت تاریخ نامعتبر است")

        # Check validity of date. TODO better check (leap years)
        if year < 1 or month < 1 or month > 12 or day < 1 or day > 31 or (month > 6 and day == 31):
            # raise ExceptionDateInvalid()
            raise Exception("تاریخ وارد شده نامعتبر است")

        self.persian_year = year
        self.persian_month = month
        self.persian_day = day

        # Convert date
        d_4 = (year + 1) % 4
        if month < 7:
            doy_j = ((month - 1) * 31) + day
        else:
            doy_j = ((month - 7) * 30) + day + 186
        d_33 = int(((year - 55) % 132) * .0305)
        a = 287 if (d_33 != 3 and d_4 <= d_33) else 286
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 19) / 63) == 20:
            a -= 1
            b += 1
        if doy_j <= a:
            gy = year + 621
            gd = doy_j + b
        else:
            gy = year + 622
            gd = doy_j - a
        for gm, v in enumerate([0, 31, 29 if (gy % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
            if gd <= v:
                break
            gd -= v

        self.gregorian_year = gy
        self.gregorian_month = gm
        self.gregorian_day = gd

    def gregorian_tuple(self):
        if self.none_flag:
            return None
        gregorian_month = str(self.gregorian_month)
        if len(gregorian_month) == 1:
            self.gregorian_month = '0' + gregorian_month
        gregorian_day = str(self.gregorian_day)
        if len(gregorian_day) == 1:
            self.gregorian_day = '0' + gregorian_day
        return self.gregorian_year, self.gregorian_month, self.gregorian_day

    def gregorian_string(self, date_format="{}-{}-{}"):
        if self.none_flag:
            return None
        gregorian_month = str(self.gregorian_month)
        if len(gregorian_month) == 1:
            self.gregorian_month = '0' + gregorian_month
        gregorian_day = str(self.gregorian_day)
        if len(gregorian_day) == 1:
            self.gregorian_day = '0' + gregorian_day
        return date_format.format(self.gregorian_year, self.gregorian_month, self.gregorian_day)

    def gregorian_datetime(self):
        if self.none_flag:
            return None
        gregorian_month = str(self.gregorian_month)
        if len(gregorian_month) == 1:
            self.gregorian_month = '0' + gregorian_month
        gregorian_day = str(self.gregorian_day)
        if len(gregorian_day) == 1:
            self.gregorian_day = '0' + gregorian_day
        return datetime.date(self.gregorian_year, self.gregorian_month, self.gregorian_day)
