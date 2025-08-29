def segment(text, segs):
        words = []
        last = 0
        for i in range(len(segs)):
            if segs[i] == '1':
                words.append(text[last:i+1])
                last = i+1
        words.append(text[last:])
        return words
text = "doyouseethekittyseethedoggydoyoulikethekittylikethedoggy"
seg1 = "0000000000000001000000000010000000000000000100000000000"
seg2 = "0100100100100001001001000010100100010010000100010010000"
print(segment(text, seg2))