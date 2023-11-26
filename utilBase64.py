import base64


def encodingBase64(str):
    bytes = str.encode('UTF-8')
    result = base64.b64encode(bytes)
    # result_str = result.decode('ascii')
    print("  .base64 encoding success")
    return result


def decodingBase64(str):
    # bytes = str.encode('UTF-8')
    # result = base64.b64encode(bytes)
    result_str = str.decode('ascii')
    print("  .base64 decoding success")
    return result_str
