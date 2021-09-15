import random
import time

from pyinsect.collector.NGramGraphCollector import NGramGraphCollector

if __name__ == "__main__":

    def getRandomText(iSize):
        # lCands = list("abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper() + "1234567890!@#$%^&*()")
        lCands = list("abcdef")
        sRes = "".join([random.choice(lCands) for i in range(1, iSize)])
        return sRes

    # Start test
    print("Initializing texts...")
    lTexts = list()
    for iCnt in range(0, 50):
        # Select text size
        iSize = random.randint(1000, 2000)
        sText = getRandomText(iSize)
        # Add to list
        lTexts.append(sText)
    print("Initializing texts... Done.")

    print("Starting shallow...")
    cNoDeep = NGramGraphCollector()
    start = time.time()
    lastStep = start
    # No deep
    iCnt = 0
    for sText in lTexts:
        cNoDeep.add(sText)
        iCnt += 1
        if time.time() - lastStep > 1:
            print("..." + str(iCnt))
            lastStep = time.time()

    end = time.time()
    print((end - start))
    print("End shallow.")

    # print "Starting deep..."
    # cDeep = NGramGraphCollector()
    # start = time.time()
    # # Deep
    # for sText in lTexts:
    #     cDeep.add(sText, True)
    #     if (time.time() - lastStep > 1):
    #         print "."
    #         lastStep = time.time()
    # end = time.time()
    # print(end - start)
    # print "End deep."
