# romaji_map.py
romaji_dict = {
    "あ": ["a"], "い": ["i"], "う": ["u"], "え": ["e"], "お": ["o"],
    "か": ["ka"], "き": ["ki"], "く": ["ku"], "け": ["ke"], "こ": ["ko"],
    "さ": ["sa"], "し": ["si"], "す": ["su"], "せ": ["se"], "そ": ["so"],
    "た": ["ta"], "ち": ["ti"], "つ": ["tu"], "て": ["te"], "と": ["to"],
    "な": ["na"], "に": ["ni"], "ぬ": ["nu"], "ね": ["ne"], "の": ["no"],
    "は": ["ha"], "ひ": ["hi"], "ふ": ["hu"], "へ": ["he"], "ほ": ["ho"],
    "ま": ["ma"], "み": ["mi"], "む": ["mu"], "め": ["me"], "も": ["mo"],
    "や": ["ya"], "ゆ": ["yu"], "よ": ["yo"],
    "ら": ["ra"], "り": ["ri"], "る": ["ru"], "れ": ["re"], "ろ": ["ro"],
    "わ": ["wa"], "を": ["wo"], "ん": ["n"],
    "が": ["ga"], "ぎ": ["gi"], "ぐ": ["gu"], "げ": ["ge"], "ご": ["go"],
    "ざ": ["za"], "じ": ["zi"], "ず": ["zu"], "ぜ": ["ze"], "ぞ": ["zo"],
    "だ": ["da"], "ぢ": ["di"], "づ": ["du"], "で": ["de"], "ど": ["do"],
    "ば": ["ba"], "び": ["bi"], "ぶ": ["bu"], "べ": ["be"], "ぼ": ["bo"],
    "ぱ": ["pa"], "ぴ": ["pi"], "ぷ": ["pu"], "ぺ": ["pe"], "ぽ": ["po"],
    "きゃ": ["kya"], "きゅ": ["kyu"], "きょ": ["kyo"],
    "しゃ": ["sya"], "しゅ": ["syu"], "しょ": ["syo"],
    "ちゃ": ["tya"], "ちゅ": ["tyu"], "ちょ": ["tyo"],
    "にゃ": ["nya"], "にゅ": ["nyu"], "にょ": ["nyo"],
    "ひゃ": ["hya"], "ひゅ": ["hyu"], "ひょ": ["hyo"],
    "みゃ": ["mya"], "みゅ": ["myu"], "みょ": ["myo"],
    "りゃ": ["rya"], "りゅ": ["ryu"], "りょ": ["ryo"],
    "ぎゃ": ["gya"], "ぎゅ": ["gyu"], "ぎょ": ["gyo"],
    "じゃ": ["ja"], "じゅ": ["ju"], "じょ": ["jo"],
    "びゃ": ["bya"], "びゅ": ["byu"], "びょ": ["byo"],
    "ぴゃ": ["pya"], "ぴゅ": ["pyu"], "ぴょ": ["pyo"],
}

def kana_to_romaji(kana_text):
    result = ""
    i = 0
    while i < len(kana_text):
        # 促音の処理
        if kana_text[i] == "っ" and i + 1 < len(kana_text):
            next_char = None
            # 拗音優先
            if i + 2 < len(kana_text) and kana_text[i+1:i+3] in romaji_dict:
                next_char = kana_text[i+1:i+3]
            elif kana_text[i+1] in romaji_dict:
                next_char = kana_text[i+1]
            
            if next_char:
                # 最初のローマ字候補の先頭子音を重ねる
                romaji_next = romaji_dict[next_char][0]
                if romaji_next[0] in "bcdfghjklmnpqrstvwxyz":
                    result += romaji_next[0]
                    i += 1
                    continue

        # 拗音（2文字）チェック
        if i + 1 < len(kana_text) and kana_text[i:i+2] in romaji_dict:
            # 最初の候補を採用
            result += romaji_dict[kana_text[i:i+2]][0]
            i += 2
        elif kana_text[i] in romaji_dict:
            # 最初の候補を採用
            result += romaji_dict[kana_text[i]][0]
            i += 1
        else:
            result += kana_text[i]
            i += 1
    return result
