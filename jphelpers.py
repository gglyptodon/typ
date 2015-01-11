import tinysegmenter
SEGMENTER = tinysegmenter.TinySegmenter()


class KanjiVocab():
    def __init__(self, kanji=None, kana=None, meaning=None):
        self.kanji = kanji
        self.kana = kana
        self.meaning = meaning
        self.romaji = Kana.toRomaji(self.kana)


class KanjiImporter():
    @staticmethod
    def parseInfile(file):
        with open(file, 'r') as infile:
            for l in infile:
                if l.startswith("#"):
                    continue
                #todo clean up meaning
                kanji, kana, meaning = l.strip().split(" ")[0], l.strip().split(" ")[1], "".join(l.strip().split(" ")[2:])
                yield kanji, kana, meaning


class JapaneseSentence():
    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = SEGMENTER.tokenize(sentence)

    def print_tokens(self):
        print('--'.join(self.tokens))


class JapaneseText():
    def __init__(self, path):
        with open(path, 'r') as infile:
            txt = infile.read().strip()
        self.sentences = txt.split(u"。")
        self.tokenized = [JapaneseSentence(s).tokens for s in self.sentences]


def testJP(path):
    print(JapaneseText(path).tokenized)




class Kana():
    #table
    hiragana = list(u"あいうえおかきくけこがぎぐげごさしすせそざじずぜぞ" \
                    u"たちつてとだぢづでどなにぬねのはひふへほ" \
                    u"ばびぶべぼぱぴぷぺぽ" \
                    u"まみむめもやゆよらりるれろわゐゑをん")

    hiragana += [u"きゃ", u"きゅ", u"きょ"]
    hiragana += [u"ぎゃ", u"ぎゅ", u"ぎょ"]
    hiragana += [u"しゃ", u"しゅ", u"しょ"]
    hiragana += [u"じゃ", u"じゅ", u"じょ"]
    hiragana += [u"ぴゃ", u"ぴゅ", u"ぴょ"]
    hiragana += [u"びゃ", u"びゅ", u"びょ"]

    katakana = list(u"アイウエオカキクケコガギグゲゴサシスセソザジズセゾ" \
                    u"タチツテトダヂヅデドナニヌネノハヒフヘホ" \
                    u"バビブベボパピプペポ" \
                    u"マミムメモヤユヨラリルレロワヰヱヲン")
    katakana += [u"きャ", u"きュ", u"きョ"]
    katakana += [u"ギャ", u"ギュ", u"ギョ"]
    katakana += [u"シャ", u"シュ", u"ショ"]
    katakana += [u"ジャ", u"ジュ", u"ジョ"]
    katakana += [u"ピャ", u"ピュ", u"ピョ"]
    katakana += [u"ビャ", u"ビュ", u"ビョ"]

    romaji = "a,i,u,e,o," \
             "ka,ki,ku,ke,ko," \
             "ga,gi,gu,ge,go," \
             "sa,shi,su,se,so," \
             "za,ji,zu,ze,zo," \
             "ta,chi,tsu,te,to," \
             "da,di,du,de,do," \
             "na,ni,nu,ne,no," \
             "ha,hi,fu,he,ho," \
             "ba,bi,bu,be,bo," \
             "pa,pi,pu,pe,po," \
             "ma,mi,mu,me,mo," \
             "ya,yu,yo," \
             "ra,ri,ru,re,ro," \
             "wa,wi,we,wo,n, " \
             "kya,kyu,kyo," \
             "gya,gyu,gyo," \
             "sha,shu,sho," \
             "ja,ju,jo," \
             "hya,hyu,hyo," \
             "pya,pyu,pyo,"\
             "bya,byu,byo".split(",")

    hiragana2romaji = {}
    katakana2romaji = {}

    for i, h in enumerate(hiragana):
        print(i, h, romaji[i])
        hiragana2romaji[h] = romaji[i]
    for i, k in enumerate(katakana):
        katakana2romaji[k] = romaji[i]


    @staticmethod
    def toRomaji(txt):
        res = ""
        tmp = ""
        for i, c in enumerate(txt):
            if c in [u"っ", u"ッ"]: #double following romaji consonant
                try:
                    tmp = Kana.toRomaji(txt[i+1])[0]
                except IndexError:
                    pass

            if c in [u"ャ", u"ュ", u"ョ", u"ゃ", u"ゅ", u"ょ"]:
                continue
            if c in [u"き", u"ぎ",
                     u"し", u"じ",
                     u"ひ", u"び",
                     u"ぴ",
                     u"キ", u"ぎ",
                     u"シ", u"ジ",
                     u"ヒ", u"ビ",
                     u"ぴ"]:#hya, bya...
                try:
                    if txt[i+1] in [u"ャ", u"ュ", u"ョ", u"ゃ", u"ゅ", u"ょ"]:
                        c += txt[i+1]

                except IndexError:
                    pass
            print(c, "c")
            if c in Kana.katakana2romaji:
                res += tmp+Kana.katakana2romaji[c]
                tmp=""
            elif c in Kana.hiragana2romaji:
                res += tmp+Kana.hiragana2romaji[c]
                tmp=""
        return res


def main():
    inputfile = "renshuu_export.txt"
    kanjilist = []
    for kanji in KanjiImporter.parseInfile(inputfile):
        kanjilist.append(KanjiVocab(kanji[0], kanji[1], kanji[2]))

    kana = [k.kana for k in kanjilist]
    print(kana)
    romaji = [k.romaji for k in kanjilist]
    print(romaji)

if __name__ == "__main__":
    main()