class Planet(object):
    def __init__(self, name, parentPlanet):
        self.name = name
        self.parentPlanetName = parentPlanet
        self.childPlanets = set()

class OrbitMap(object):
    def __init__(self):
        self.root = Planet("COM", None)
        self.allPlanetNames = set("COM")
        self.allTreeRoots = set(self.root)

    def findPlanet(self, planetName):
        for tree in self.allTreeRoots:
            planet = self.searchPlanetTree(tree, planetName)
            if planet is not None:
                return planet
        raise ValueError("Planet not found!")

    def searchPlanetTree(self, tree, planetName):
        #TODO finish this function
        return 0

def contructMapTrie(planetTuples):
    orbitMap = OrbitMap()
    for planetTuple in planetTuples:
        parentName = planetTuple[0]
        childName = planetTuple[1]
        if parentName not in orbitMap.allPlanetNames and childName not in orbitMap.allPlanetNames:
            parentPlanet = Planet(parentName, None)
            childPlanet = Planet(childName, parentPlanet)
            parentPlanet.childPlanets.add(childPlanet)

            orbitMap.allPlanetNames.add(parentName)
            orbitMap.allPlanetNames.add((childName))
            orbitMap.allTreeRoots.add(parentPlanet)
        elif parentName in orbitMap.allPlanetNames and childName not in orbitMap.allPlanetNames:

        elif parentName not in orbitMap.allPlanetNames and childName in orbitMap.allPlanetNames:

        else: #both parent and child already on the map

    return orbitMap

def getTotalPaths(orbitMap):
    return 0

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()
        lines = input.split('\n')
        planetTuples = [tuple(planets.split(')')) for planets in lines]
    orbitMap = contructMapTrie(planetTuples)
    numOrbits = getTotalPaths(orbitMap)
    print(numOrbits)