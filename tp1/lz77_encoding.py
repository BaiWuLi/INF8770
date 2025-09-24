def lz77_encode(data, window_size=2056, lookahead_size=2056):
    i = 0
    output = []

    while i < len(data):
        match_len, match_dist = 0, 0
        start = max(0, i - window_size)

        # Search for longest match in the sliding window
        for j in range(start, i):
            length = 0
            while (length < lookahead_size and
                   i + length < len(data) and
                   data[j + length] == data[i + length]):
                length += 1
            if length > match_len:
                match_len = length
                match_dist = i - j

        if match_len > 0:
            # (distance, length, next symbol)
            next_char = data[i + match_len] if i + match_len < len(data) else ""
            output.append((match_dist, match_len, next_char))
            i += match_len + 1
        else:
            # No match → just output (0,0,char)
            output.append((0, 0, data[i]))
            i += 1

    return output

def lz77_decode(encoded):
    decoded = []
    for dist, length, char in encoded:
        if dist == 0 and length == 0:
            decoded.append(char)
        else:
            start = len(decoded) - dist
            for i in range(length):
                decoded.append(decoded[start + i])
            if char:
                decoded.append(char)
    return "".join(decoded)