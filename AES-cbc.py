from base64 import b64decode
from Crypto.Cipher import AES


def fixed_length_xor(text, key) -> bytes:
    """
    Performs a binary XOR of two equal-length strings. 
    
    Parameters
    ----------
    text : bytes
        bytes-object to be xor'd w/ key
    key : bytes
        bytes-object to be xor'd w/ text
        
    Returns
    -------
    bytes
        binary XOR of text & key
    """

    output = b''
    
    for i in range(len(text)):
        output += bytes([text[i] ^ key[i]])

    return output


def repeating_key_xor(text, key) -> bytes:
    """Takes two bytestrings and XORs them, returning a bytestring.
    Extends the key to match the text length.
    
    Parameters
    ----------
    text : bytes
        bytes-object to be xor'd w/ key
    key : bytes
        bytes-object to be xor'd w/ text
        
    Returns
    -------
    bytes
        binary XOR of text & key
    """

    
    extended_key = key * (len(text) // len(key) + 1)
    extended_key = extended_key[:len(text)] 
    
    # Voer een XOR-operatie uit tussen de text en de extended_key.
    xor_output = fixed_length_xor(text, extended_key)
    
    return xor_output



def CBC_decrypt(ciphertext, key, IV):
    """Decrypts a given plaintext in CBC mode.
    First splits the ciphertext into keylength-size blocks,
    then decrypts them individually w/ ECB-mode AES
    and XOR's each result with either the IV
    or the previous ciphertext block.
    Appends decrypted blocks together for the output.

    Parameters
    ----------
    ciphertext : bytes
        ciphertext to be decrypted
    key : bytes
        Key to be used in decryption
    IV : bytes
        IV to be used for XOR in first block

    Returns
    -------
    bytes
        Decrypted plaintext
    """

    # Initialize AES cipher in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Split the ciphertext into keylength-size blocks
    blocks = [ciphertext[i:i+len(key)] for i in range(0, len(ciphertext), len(key))]

    # Initialize plaintext and previous block
    plaintext = b''
    prev_block = IV

    # Iterate over each block
    for block in blocks:
        # Decrypt the block with ECB-mode AES
        decrypted_block = cipher.decrypt(block)

        # XOR the decrypted block with the previous ciphertext block or IV
        xor_output = repeating_key_xor(decrypted_block, prev_block)

        # Add the XOR output to the plaintext
        plaintext += xor_output

        # Set the previous block to the current ciphertext block
        prev_block = block

    # Return the decrypted plaintext
    return plaintext


# Laat dit blok code onaangetast & onderaan je code!
a_ciphertext = b64decode('e8Fa/QnddxdVd4dsL7pHbnuZvRa4OwkGXKUvLPoc8ew=')
a_key = b'SECRETSAREHIDDEN'
a_IV = b'WE KNOW THE GAME'
assert CBC_decrypt(a_ciphertext, a_key, a_IV)[:18] == \
    b64decode('eW91IGtub3cgdGhlIHJ1bGVz')
