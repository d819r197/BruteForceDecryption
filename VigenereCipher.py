import time
import itertools

def charToInt(cIn):
    cLower = cIn.lower()
    return(ord(cLower)-97)

def intToChar(iIn):
    return(chr(iIn+97))

def encrypt(plainText, key):
    keyLen = len(key)
    keyIndex = 0
    #print("Encryting PlainText: " + plainText)
    cypherText = ""
    for c in plainText:
        cypherLetter = intToChar((charToInt(c) + charToInt(key[keyIndex])) % 26)
        cypherText += cypherLetter
        keyIndex += 1
        if keyIndex == keyLen:
            keyIndex = 0
    return cypherText

def decrypt(cypherText, key):
    keyLen = len(key)
    keyIndex = 0
    #print("Decrypting CypherText: " + cypherText)
    plainText = ""
    for c in cypherText:
        letter = intToChar((charToInt(c) - charToInt(key[keyIndex])) % 26)
        plainText += letter
        keyIndex += 1
        if keyIndex == keyLen:
            keyIndex = 0
    return plainText

def importDict(path, size):
    dict = []
    file = open(path, "r")
    fileLines = file.readlines()

    for line in fileLines:
        #print("Adding Key: "+ line[0:len(line)-1] +" of Size: " + str(len(line)-1))
        if len(line)-1 == size:
            dict.append(str(line[0:len(line)-1]).lower())
    return dict

def exportCypher(cypherText, plainText, execTime, key):
    file = open("CypherOutput.txt", "a", newline="\n")
    file.write("The encoded word: " + cypherText + " is the decoded word: " + plainText + "\n")
    file.write("Cypher complete using key: " + str(key) + " in " + str(execTime) + " seconds.\n\n")
    file.close()

def menu():
    print("Choose an option: ")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Brute Force")
    print("4. Quit")

    choice = input("Choice: ")

    if choice == "1":
        pt = input("Enter PlainText: ")
        key = input("Enter Key: ")
        cypherText = encrypt(pt, key)
        print("Resulting CypherText: " + cypherText)
    elif choice == "2":
        ct = input("Enter CypherText: ")
        key = input("Enter Key: ")
        plainText = decrypt(ct, key)
        print("Resulting PlainText: " + plainText)
    elif choice == "3":
        dictPath = "dict.txt"

        ct = input("Enter CypherText: ")
        keyLen = int(input("Enter Key Length: "))
        fwLen = int(input("Enter First Word Length: "))
        dict = importDict(dictPath, int(fwLen))
        brokenCT = [ct[i:i+fwLen] for i in range(0, len(ct), fwLen)]

        #Start Function Timer
        startTime = time.time()
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        alphabetCombos = [alphabet] * keyLen
        possibleKeys = list(itertools.product(*alphabetCombos))
        firstCypher = brokenCT[0]
        foundDecryptions = []
        for key in possibleKeys:
            pt = decrypt(firstCypher, key)
            print("Checking FWPT: " + pt)
            if pt in dict:
                print("FWPT: " + pt + " is in dict" )
                fullPT = decrypt(ct, key)
                foundDecryptions.append(fullPT)
                currTime = time.time()
                elapsedTime = currTime - startTime
                exportCypher(ct, fullPT, elapsedTime, key)

        print("\nPossible Decryption for given encrypted text: " + str(foundDecryptions))
        #End Function Timer
        endTime = time.time()
        duration = endTime - startTime
        print("Total Execution Time: "+str(duration)+" Seconds\n")
    elif choice == "4":
        print("Exiting Program")
        return True

def main():
    exit = False
    while(not exit):
        exit = menu()

if __name__ == "__main__":
    main()
