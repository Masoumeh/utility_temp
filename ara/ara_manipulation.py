
# Functions to deal with Arabic texts
import re


# noiseChar = "[\|#\*+\$%.,:;\(\)\[\]\{\}]|@[a-zA-Z]+@"

# normalizeArabic(text) - normalizes Arabic by simplifying complex characters
def normalizeArabic(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("(ؤ)", "و", text)
    text = re.sub("(ئ)", "ي", text)
    text = re.sub("(ة)", "ه", text)
    return (text)


# normalizeArabicHeavy(text) - normalizes Arabic by simplifying complex characters
def normalizeArabicHeavy(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("(ؤ)", "و", text)
    text = re.sub("(ئ)", "ي", text)
    text = re.sub("ء", "", text)
    text = re.sub("(ة)", "ه", text)
    return (text)


# normalizeArabicLight(text) - fixing only Alifs, AlifMaqsuras; replacing hamzas on carriers with standalone hamzas
def normalizeArabicLight(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("[يى]ء", "ئ", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("(ؤ)", "ء", text)
    text = re.sub("(ئ)", "ء", text)
    # text = re.sub("(ء)", "", text)
    # text = re.sub("(ة)", "ه", text)
    return (text)

def textCleaner(text):
    text = normalizeArabicLight(text)
    text = re.sub("\W|\d|[A-z]", " ", text)
    text = re.sub(" +", " ", text)
    return (text)