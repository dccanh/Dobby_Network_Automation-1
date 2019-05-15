import base64


def base64encode(input_string):
    initial_data = input_string
    byte_string = initial_data.encode('utf-8')
    encoded_data = base64.b64encode(byte_string)
    return encoded_data.decode('ascii')
