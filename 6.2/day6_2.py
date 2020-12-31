class Planet(object):
    def __init__(self, name, parentPlanet):
        self.name = name
        self.parentPlanet = parentPlanet
        self.childPlanets = set()

class OrbitMap(object):
    def __init__(self):
        self.root = Planet("COM", None)
        self.allPlanets = {}
        self.allPlanets.update({"COM": self.root})

def contructMapTrie(planetTuples):
    orbitMap = OrbitMap()
    for planetTuple in planetTuples:
        parentName = planetTuple[0]
        childName = planetTuple[1]
        planetNames = orbitMap.allPlanets.keys()
        if parentName not in planetNames and childName not in planetNames:
            parentPlanet = Planet(parentName, None)
            childPlanet = Planet(childName, parentPlanet)
            parentPlanet.childPlanets.add(childPlanet)
            childPlanet.parentPlanet = parentPlanet

            orbitMap.allPlanets.update({parentName: parentPlanet})
            orbitMap.allPlanets.update({childName: childPlanet})
        elif parentName in planetNames and childName not in planetNames:
            parentPlanet = orbitMap.allPlanets.get(parentName)
            childPlanet = Planet(childName, parentPlanet)
            parentPlanet.childPlanets.add(childPlanet)
            childPlanet.parentPlanet = parentPlanet

            orbitMap.allPlanets.update({childName: childPlanet})
        elif parentName not in planetNames and childName in planetNames:
            parentPlanet = Planet(parentName, None)
            childPlanet = orbitMap.allPlanets.get(childName)
            parentPlanet.childPlanets.add(childPlanet)
            childPlanet.parentPlanet = parentPlanet

            orbitMap.allPlanets.update({parentName: parentPlanet})
        else: #both parent and child already on the map
            parentPlanet = orbitMap.allPlanets.get(parentName)
            childPlanet = orbitMap.allPlanets.get(childName)
            parentPlanet.childPlanets.add(childPlanet)
            childPlanet.parentPlanet = parentPlanet
    return orbitMap

def getMinDist(orbitMap, start, end):
    startPlanet = orbitMap.allPlanets.get(start).parentPlanet
    startLine = [startPlanet]

    endPlanet = orbitMap.allPlanets.get(end).parentPlanet
    endLine = [endPlanet]

    while len(set(startLine).intersection(set(endLine))) == 0:
        highestAncestor = startLine[-1]
        startLine.append(highestAncestor.parentPlanet)

        highestAncestor = endLine[-1]
        endLine.append(highestAncestor.parentPlanet)

    commonAncestor = list(set(startLine).intersection(set(endLine)))[0]
    startDist = startLine.index(commonAncestor)
    endDist = endLine.index(commonAncestor)

    return startDist + endDist


def getNeighbors(planet):
    return planet.childPlanets.union(planet.parentPlanet)

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()
        lines = input.split('\n')
        planetTuples = [tuple(planets.split(')')) for planets in lines]
    orbitMap = contructMapTrie(planetTuples)
    minDist = getMinDist(orbitMap, "YOU", "SAN")
    print(minDist)