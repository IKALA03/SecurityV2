from base64 import b64decode
from Crypto.Cipher import AES
from secrets import token_bytes


def pkcs7_pad(plaintext, blocksize):
    """Appends the plaintext with n bytes,
    making it an even multiple of blocksize.
    Byte used for appending is byteform of n.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be appended
    blocksize : int
        blocksize to conform to

    Returns
    -------
    plaintext : bytes
        plaintext appended with n bytes
    """

    # Determine how many bytes to append
    n = blocksize - len(plaintext)%blocksize
    # Append n*(byteform of n) to plaintext
    # n is in a list as bytes() expects iterable
    plaintext += (n*bytes([n]))
    return plaintext

def ECB_oracle(plaintext,    key):
    """Appends a top-secret identifier to the plaintext
    and encrypts it under AES-ECB using the provided key.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be encrypted
    key : bytes
        16-byte key to be used in decryption

    Returns
    -------
    ciphertext : bytes
        encrypted plaintext
    """
    plaintext += b64decode('U2F5IG5hIG5hIG5hCk9uIGEgZGFyayBkZXNlcnRlZCB3YXksIHNheSBuYSBuYSBuYQpUaGVyZSdzIGEgbGlnaHQgZm9yIHlvdSB0aGF0IHdhaXRzLCBpdCdzIG5hIG5hIG5hClNheSBuYSBuYSBuYSwgc2F5IG5hIG5hIG5hCllvdSdyZSBub3QgYWxvbmUsIHNvIHN0YW5kIHVwLCBuYSBuYSBuYQpCZSBhIGhlcm8sIGJlIHRoZSByYWluYm93LCBhbmQgc2luZyBuYSBuYSBuYQpTYXkgbmEgbmEgbmE=')
    plaintext = pkcs7_pad(plaintext, len(key))
    cipher = cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

# Genereer een willekeurige key
key = token_bytes(16)

#####################################
###  schrijf hieronder jouw code  ###
### verander code hierboven niet! ###
#####################################

def find_block_length():
    """Finds the block length used by the ECB oracle.

    Returns
    -------
    blocksize : integer
        blocksize used by ECB oracle
    """

    # Start met een plaintext karakter (1 lang)
    plaintext = b"A"
    # blijf encrypten totdat de lengte verandert
    previous_length = len(ECB_oracle(plaintext, key))
    while True: 
        plaintext += b"A" # voeg weer 1 karakter toe aan plaintekst
        new_length = len(ECB_oracle(plaintext, key)) 
        if new_length != previous_length: # als de lengte verandert, return het verschil in lengte
            return new_length - previous_length
        previous_length = new_length # update de lengte

def find_secret_text_length():
    """Finds the length of the secret text added by the ECB oracle.

    Returns
    -------
    secret_text_length : integer
        length of secret text added by ECB oracle
    """

    blocksize = find_block_length() # blocksize van de oracle

    # iterate door de blocksize
    for i in range(blocksize): # neem i = 2, blocksize = 16
        plaintext = bytes("X"*(blocksize-1-i), 'utf-8') # "X"*16-1-i(2) = "X"*14
        ciphertext1 = ECB_oracle(plaintext, key) 
        ciphertext2 = ECB_oracle(plaintext + bytes([0]), key) 
        if ciphertext1[:i+blocksize] == ciphertext2[:i+blocksize]: # als beide cipherteksten vanaf i + de blocksize gelijk zijn ...
            return len(ciphertext1) - i - blocksize # ... return de lengte van de cipertekst - i - de blocksize om zo de totale lengte van de tekst te returnen

    raise Exception("No length found!")

def find_secret_text(blocksize):
    """Finds the secret text used by the ECB oracle.

    Parameters
    ----------
    blocksize : int
        blocksize used by the ECB oracle

    Returns
    -------
    secret_text : bytes
        secret text used by the ECB oracle
    """

    empty_ciphertext_len = len(ECB_oracle(b"", key)) 
    secret_text_len = 0
    secret_text = b'' # secret text aanmaken

    while True:
        plaintext = b"X" * (blocksize - 1 - (secret_text_len % blocksize))
        ciphertext = ECB_oracle(plaintext, key)
        for byte in range(256):
            test_plaintext = plaintext + secret_text + bytes([byte])
            test_ciphertext = ECB_oracle(test_plaintext, key)

            if test_ciphertext[:blocksize] == ciphertext[:blocksize]:
                secret_text += bytes([byte])
                secret_text_len += 1
                if len(secret_text) == empty_ciphertext_len:
                    return secret_text.decode("utf-8") # convert naar utf8
                break


print(find_secret_text(find_block_length()))