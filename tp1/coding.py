import collections
import heapq

# -----------------------------
# 1. Huffman coding
# -----------------------------
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encode(text):
    freq = collections.Counter(text)
    heap = [HuffmanNode(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = HuffmanNode(None, n1.freq + n2.freq)
        merged.left, merged.right = n1, n2
        heapq.heappush(heap, merged)

    codes = {}
    def generate_codes(node, current=""):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current
        generate_codes(node.left, current + "0")
        generate_codes(node.right, current + "1")
    generate_codes(heap[0])

    encoded = "".join(codes[ch] for ch in text)
    return encoded, codes

# -----------------------------
# 2. Byte Pair Encoding (BPE)
# -----------------------------
def bpe_encode(text, num_merges=50):
    text = list(text)
    for _ in range(num_merges):
        # count pairs
        pairs = collections.Counter(zip(text, text[1:]))
        if not pairs:
            break
        best_pair = max(pairs, key=pairs.get)
        new_symbol = "".join(best_pair)

        # replace pair
        new_text = []
        i = 0
        while i < len(text):
            if i < len(text) - 1 and (text[i], text[i+1]) == best_pair:
                new_text.append(new_symbol)
                i += 2
            else:
                new_text.append(text[i])
                i += 1
        text = new_text
    return text

# -----------------------------
# 3. LZW compression
# -----------------------------
def lzw_encode(text):
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in text:
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

# -----------------------------
# Main comparison
# -----------------------------
if __name__ == "__main__":
    with open('tp1/data/text_code/code1.py') as f:
        text = f.read()

    print("Taille originale :", len(text), "caractères")
    # Huffman
    huff_encoded, huff_codes = huffman_encode(text)
    print("Huffman :", len(huff_encoded) // 8, "octets environ")
  
    # BPE
    bpe_encoded = bpe_encode(text, num_merges=100)
    print("BPE :", len(bpe_encoded), "symboles (vs", len(text), "caractères)")

    # LZW
    lzw_encoded = lzw_encode(text)
    print("LZW :", len(lzw_encoded), "entiers")
