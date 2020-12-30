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

def getTotalPaths(orbitMap):
    currentLevel = 0
    levelPlanets = [orbitMap.root]
    numOrbits = 0

    while len(levelPlanets) != 0:
        currentLevel += 1
        lvlCopy = levelPlanets.copy()
        for planet in lvlCopy:
            levelPlanets.remove(planet)
            for child in planet.childPlanets:
                levelPlanets.append(child)
        numOrbits += currentLevel * len(levelPlanets)
    return numOrbits

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()
        lines = input.split('\n')
        planetTuples = [tuple(planets.split(')')) for planets in lines]
    orbitMap = contructMapTrie(planetTuples)
    numOrbits = getTotalPaths(orbitMap)
    print(numOrbits)