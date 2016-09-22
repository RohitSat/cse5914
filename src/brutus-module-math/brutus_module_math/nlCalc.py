def calculate(string):
    string=convertToNumbers(string)
    #print(string)
    string=convertToSymbols(string)
    #print(string)
    string=stripWords(string)
    #print(string)
    result=evaluate(string)
    resultstring= string + ' is ' + str(result)
    return resultstring
    
def convertToNumbers(string):
    oldarr=string.split()
    newarr=[]
        
    for word in oldarr:
        try:
            newarr.append(convertWordToNumber(word))
        except:
            newarr.append(word)

    i=0
    while(i<len(newarr)-1):
        #print i
        #print newarr[i]
        if(all(char.isdigit() for char in newarr[i])) and (all(char.isdigit() for char in newarr[i+1])):
            cur=int(newarr[i])+int(newarr[i+1])
            newarr.pop(i+1)
            newarr[i]=str(cur)
        else:
            i=i+1
        
    return ' '.join(newarr)

def convertWordToNumber(string):
    numwords={}
    units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    scales = ["hundred", "thousand", "million", "billion", "trillion"]
    
    for idx, word in enumerate(units):    numwords[word] = (1, idx)
    for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
    for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)
    
    current=result=0
    for word in string.split("-"):
        if word not in numwords:
            raise ValueError()
        scale, increment = numwords[word]
        current=current*scale+increment
        if scale>100:
            result += current
            current=0
        
    return str(result+current)
    

def convertToSymbols(string):
    strarray=string.split()
    for i in range(len(strarray)):
        word=strarray[i]        
        if word.lower()=="plus":
            word="+"
        if word.lower()=="minus":
            word="-"
        if word.lower()=="multiplied":
            word="*"
        if word.lower()=="times":
            word="*"
        if word.lower()=="divided":
            word="/"
        if word.lower()=="over":
            word="/"
        
        strarray[i]=word
    
    return ' '.join(strarray)
            
            


def stripWords(string):
    strarray=string.split()
    acceptablewords=['+', '-', '/', '*']
    i = 0
    while(i<len(strarray)):
        word=strarray[i]
        if word not in acceptablewords and not (all(char.isdigit() for char in word)):
            strarray.pop(i)
        else:    
            i=i+1
    return ' '.join(strarray)

def evaluate(string):
    return eval(string)



