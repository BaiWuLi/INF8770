import heapq
from collections import Counter, namedtuple

class Node(namedtuple("Node", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, f, None, None) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, prefix="", codebook={}):
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(text):
    tree = build_huffman_tree(text)
    codes = build_codes(tree)
    encoded = "".join(codes[ch] for ch in text)
    return encoded, codes, tree

def huffman_decode(encoded, tree):
    decoded, node = [], tree
    for bit in encoded:
        node = node.left if bit == "0" else node.right
        if node.char:
            decoded.append(node.char)
            node = tree
    return "".join(decoded)