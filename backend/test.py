import re


cases = ["",
         "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
         "/////",
         ":/aaa////",
         "a.png",
         "..",
         "0",
         "abcde",
         "Aa0_",
         "0123456789____",
         "あ",
         "a\na"]
for txt in cases:
    x = re.search("^[a-zA-Z0-9_]{1,20}$", txt)
    print(x)
