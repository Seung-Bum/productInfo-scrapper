import base64


def encodingBase64(str):
    bytes = str.encode('UTF-8')
    result = base64.b64encode(bytes)
    # result_str = result.decode('ascii')
    print("  .base64 encoding success")
    return result


def decodingBase64(code):
    code_bytes = code.encode('ascii')
    decoded = base64.b64decode(code_bytes)
    str = decoded.decode('UTF-8')
    return str
