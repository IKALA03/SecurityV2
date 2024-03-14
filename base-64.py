import base64

def string_to_b64(asciiString) -> bytes:
    """
    Converts a given ASCII-string to its b64-encoded equivalent.

    Parameters
    ----------
    asciiString : string
        string to be converted

    Returns
    -------
    bytes
        b64-encoded bytes-object representing the original string
    """
    b64Bytes = base64.b64encode(asciiString.encode('utf-8'))
    return b64Bytes

# Laat deze asserts onaangetast!
assert type(string_to_b64("foo")) == bytes
assert string_to_b64("Hello World") == b'SGVsbG8gV29ybGQ='

def b64_to_string(b64String) -> str:
    """
    Converts a given b64-string to its ASCII equivalent.

    Parameters
    ----------
    b64String : bytes
        b64-encoded bytesobject to be converted

    Returns
    -------
    string
        ASCII string
    """
    asciiString = base64.b64decode(b64String).decode('utf-8')
    return asciiString

# Laat deze asserts onaangetast!
assert type(b64_to_string("SGVsbG8gV29ybGQ=")) == str
assert b64_to_string("SGVsbG8gV29ybGQ=") == "Hello World"


def bonus_base64encode(asciiString):
    """
    Een functie die de stappen van base64-encodering implementeert.

    Parameters
    ----------
    asciiString : string
        De string die geëncodeerd moet worden.

    Returns
    -------
    string
        Base64-geëncodeerde string.
    """

    # De base64 karakterset.
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    # De ASCII-string wordt omgezet naar bytes.
    bytes_to_encode = asciiString.encode('utf-8')

    # De bytes worden geconverteerd naar een binair string.
    binary_string = ''.join(format(byte, '08b') for byte in bytes_to_encode)

    # De binaire string wordt opgevuld met nullen totdat deze een veelvoud van 6 wordt.
    while len(binary_string) % 6 != 0:
        binary_string += '0'

    # De binaire string wordt opgedeeld in blokken van 6 karakters.
    blocks = [binary_string[i:i+6] for i in range(0, len(binary_string), 6)]

    # De base64-geëncodeerde string.
    encoded_string = ''

    # Voor elk blok van 6 karakters, wordt het overeenkomstige base64-karakter toegevoegd aan de geëncodeerde string.
    for block in blocks:
        encoded_string += charset[int(block, 2)]

    # Als het aantal blokken niet deelbaar is door 4, worden er nullen toegevoegd.
    while len(encoded_string) % 4 != 0:
        encoded_string += '='

    return encoded_string

