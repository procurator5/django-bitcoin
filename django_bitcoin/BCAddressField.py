#
# Django field type for a Bitcoin Address
#
from django import forms
from django.forms.utils import ValidationError
import hashlib
import re

class BCAddressField(forms.CharField):
    default_error_messages = {
        'invalid': 'Invalid Bitcoin address.',
        }

    def __init__(self, *args, **kwargs):
        super(BCAddressField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and not self.required:
            return None

        if not value.startswith(u"1") and not value.startswith(u"3"):
            raise ValidationError(self.error_messages['invalid'])
        value = value.strip()

        if "\n" in value:
            raise ValidationError(u"Multiple lines in the bitcoin address")

        if " " in value:
            raise ValidationError(u"Spaces in the bitcoin address")

        if re.match(r"[a-zA-Z1-9]{27,35}$", value) is None:
            raise ValidationError(self.error_messages['invalid'])
        version = get_bcaddress_version(value)
        if version is None:
            raise ValidationError(self.error_messages['invalid'])
        return value

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

 
def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + __b58chars.index(char)
    return n.to_bytes(length, 'big')

def is_valid_btc_address(bc):
    try:
        bcbytes = decode_base58(bc, 25)
        return bcbytes[-4:] == hashlib.sha256(hashlib.sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False


def b58encode(v):
    """ encode v, which is a string of bytes, to base58.
    """

    long_value = 0
    for (i, c) in enumerate(v[::-1]):
        long_value += (256**i) * ord(c)

    result = ''
    while long_value >= __b58base:
        div, mod = divmod(long_value, __b58base)
        result = __b58chars[mod] + result
        long_value = div
    result = __b58chars[long_value] + result

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == '\0': nPad += 1
        else: break

    return (__b58chars[0]*nPad) + result

def b36encode(number, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, (int, long)):
        long_value = 0
        for (i, c) in enumerate(number[::-1]):
            long_value += (256**i) * ord(c)
        number = long_value

    base36 = '' if number != 0 else '0'
    sign = ''
    if number < 0:
        sign = '-'
        number = -number

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def b36decode(number):
    return int(number, 36)

