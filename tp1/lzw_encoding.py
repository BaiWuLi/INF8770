def lzw_encode(data):
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(dict_size)}
    w = b""
    result = []

    for b in data:
        c = bytes([b])
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result

def lzw_decode(codes):
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(dict_size)}

    w = dictionary[codes[0]]
    result = bytearray(w)

    for k in codes[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:  # special case
            entry = w + w[:1]
        else:
            raise ValueError("Bad LZW code: %s" % k)

        result.extend(entry)

        dictionary[dict_size] = w + entry[:1]
        dict_size += 1
        w = entry

    return bytes(result)
