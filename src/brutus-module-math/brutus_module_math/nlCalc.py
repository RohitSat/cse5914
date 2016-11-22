units = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen"
]
tens = [
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety"
]
scales = [
    "hundred",
    "thousand",
    "million",
    "billion",
    "trillion"
]


def calculate(string):
    """ Calculates the string """
    string = fixSpecialCases(string)
    string = convertToNumbers(string)
    string = convertToSymbols(string)
    string = stripWords(string)
    result = evaluate(string)
    resultstring = string + ' is ' + str(result)
    return resultstring


def fixSpecialCases(string):
    """ Fixes Special Cases """
    string = aFollowedByScale(string)
    string = removePunctuation(string)
    return string


def aFollowedByScale(string):
    """ Fixes a followed by a scale """
    strarr = string.split()
    newstrarr = []
    for idx in range(len(strarr)):
        if strarr[idx].lower() == "a":
            if (idx + 1 < len(strarr)) and (strarr[idx + 1].lower() in scales):
                newstrarr.append("1")
            else:
                newstrarr.append(strarr[idx])
        else:
            newstrarr.append(strarr[idx])

    return ' '.join(newstrarr)


def removePunctuation(string):
    """ Removes Punctuation """
    punctuationToRemove = ['?', ',', '"', "!", "'"]
    for punc in punctuationToRemove:
        string = string.replace(punc, '')
    return string


def convertToNumbers(string):
    """ Converts the numbers in the string to digits """
    numwords = {}
    for idx, word in enumerate(units):
        numwords[word] = (1, idx)
    for idx, word in enumerate(tens):
        numwords[word] = (1, idx * 10)
    for idx, word in enumerate(scales):
        numwords[word] = (10 ** (idx * 3 or 2), 0)

    oldarr = string.split()
    newarr = []
    idx = 0
    while(idx < len(oldarr)):
        word = oldarr[idx].lower()

        if isNumber(word.lower(), numwords):
            idx += 1
            while(idx < len(oldarr) and
                    isNumber(oldarr[idx].lower(), numwords)):
                word = word + ' ' + oldarr[idx].lower()
                idx += 1
            result = convertWordToNumber(word, numwords)
            newarr.append(result)
        else:
            idx += 1
            newarr.append(word)

    return ' '.join(newarr)


def convertWordToNumber(string, numwords):
    """ Convert Words To Numbers """
    current = 0
    result = 0
    for word in string.split(" "):
        if word in numwords:  # if the word is a word
            scale, increment = numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
        elif word.isdigit():  # if the word is digits... assumes no scales...
            scale = 1
            increment = int(word)
            current = current * 1 + increment  # Scale is assumed to be 1
        else:
            if not isNumber(word, numwords):  # Should Not happen
                return word
            raise ValueError("Word is neither digit nor digit")
    result = result + current
    return str(result)


def isNumber(string, numwords):
    """ checks if a number is a number """
    if string in numwords:
        return True
    elif string.isdigit():
        return True
    else:
        return False


def convertToSymbols(string):
    """ Converts to symbols """
    strarray = string.split()
    for i in range(len(strarray)):
        word = strarray[i]
        if word.lower() == "plus":
            word = "+"
        if word.lower() == "minus":
            word = "-"
        if word.lower() == "multiplied":
            word = "*"
        if word.lower() == "times":
            word = "*"
        if word.lower() == "divided":
            word = "/"
        if word.lower() == "over":
            word = "/"

        strarray[i] = word

    return ' '.join(strarray)


def stripWords(string):
    """ Strips all words that are not digits """
    strarray = string.split()
    acceptablewords = ['+', '-', '/', '*']
    i = 0
    while(i < len(strarray)):
        word = strarray[i]
        if word not in acceptablewords and not word.isdigit():
            strarray.pop(i)
        else:
            i = i + 1
    return ' '.join(strarray)


def evaluate(string):
    """ Evaluates the string """
    return eval(string)
