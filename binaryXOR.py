from base64 import b64encode

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

# Laat deze asserts onaangetast!
assert type(fixed_length_xor(b'foo',b'bar')) == bytes
assert b64encode(fixed_length_xor(b'foo',b'bar')) == b'BA4d'

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

    if len(key) != len(text):
        extended_key = key * (len(text) // len(key) + 1)
        extended_key = extended_key[:len(text)] 
    
    # Voer een XOR-operatie uit tussen de text en de extended_key.
    xor_output = fixed_length_xor(text, extended_key)
    
    return xor_output


# Laat deze asserts onaangetast!
assert type(repeating_key_xor(b'all too many words',b'bar')) == bytes
assert b64encode(repeating_key_xor(b'all too many words',b'bar'))\
   == b'Aw0eQhUdDUEfAw8LQhYdEAUB'
