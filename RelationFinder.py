import argparse
import ItemRelationsCsvReader
from collections import defaultdict
from CompressedFileType import CompressedFileType

def computeTable(generator):
    table = {}
    for entity, claims in generator:
        for pid, value in claims:
            if not entity in table:
                table[entity] = set()
            table[entity].add((pid, value))
    return table

def computeIntersection(table, setList):
    #todo: Compute in database!?!
    intersection = setList[0].intersection(*setList[1:])
    return intersection

def rankTuples(tupleSet):
    result = []
    for t in tupleSet:
        i = 0
        for item in table:
            if t in table[item]:
                i+=1
        result.append((t[0],t[1],i))
    result = sorted(result, key=lambda t: t[2])
    return result



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="this program finds relations between a list of wikidata-items")
    parser.add_argument("input", help="The CSV input file (wikidata triple)", type=CompressedFileType("r"))
    parser.add_argument("itemList", help="Comma seperated list of items to find relations for - example: 'Q937,Q35149,Q192112' ")
    args = parser.parse_args()
    print "computing table..."
    table = computeTable(ItemRelationsCsvReader.read_csv(args.input))
    itemList = args.itemList.split(",")
    setList = []
    print "finding relations..."
    for item in itemList:
        setList.append(set(table[item]))
    result = computeIntersection(table, setList)
    print "ranking relations..."
    result = rankTuples(result)
    print result
    if len(itemList)==2:
        pass
    

