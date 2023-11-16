import time 

from xml.sax import parse
from xml_handler import XMLHandler


def getUniqueAttributes(inputFilename, outputFilename):
    """
    This function 
    """
    uniqAttrs = set()
    with open(inputFilename, "r") as f:
        for line in f:
            attrs = line.split()

            for attr in attrs:
                if attr not in uniqAttrs:
                    uniqAttrs.add(attr)

    # Write content of set to uniqEventAttributes.txt
    with open(outputFilename, "a") as f:
        f.write(" ".join(list(uniqAttrs)))

    return len(uniqAttrs)

# print(getUniqueAttributes("eventAttributes.txt", "uniqEventAttributes.txt"))

if __name__ == "__main__":
    start = time.time()
    parse("network.xml", XMLHandler())
    end = time.time()
    print ("Total time: ", end - start)