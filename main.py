import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import music as ms
import tspga as tg

# Import library data
library_df = pd.read_excel('./excel/library4.xlsx', sheet_name=0)# print(library_df)
print("Library Details:")
print(library_df)
tracklist = []

# Set up Track objects
slowestbpm = min(library_df.iloc[:, 2])
fastestbpm = max(library_df.iloc[:, 2])

numtracks = len(library_df)

for j in range(0, numtracks):  # standardise key
    library_df.iat[j, 3] = ms.standardise_key(library_df.iat[j, 3])
    tracklist.append(tg.Track(id=library_df.iat[j, 0], bpm=library_df.iat[j, 2],
                           kint=ms.camelot2kint(ms.standkey2camelot(library_df.iat[j, 3])),
                           freq=ms.n2freq(ms.root2n(ms.standkey2root(library_df.iat[j, 3]))),
                              slowestbpm=slowestbpm, fastestbpm=fastestbpm,
                              name=library_df.iat[j, 1], key=library_df.iat[j, 3]))

# Generate adjacency matrix for easier lookup
adjacencymatrix = np.zeros((numtracks, numtracks))
for a in range(0, numtracks):  # row, from
    for b in range(0, numtracks):  # column, to
        firsttrack = tracklist[a]
        nexttrack = tracklist[b]
        adjacencymatrix[a, b] = firsttrack.distance(nexttrack)

with pd.ExcelWriter('./excel/adjacency.xlsx', mode='w') as writer:  # doctest: +SKIP
    adjmat_df = pd.DataFrame(adjacencymatrix)
    adjmat_df.to_excel(writer, sheet_name="adjacency", startrow=0, startcol=0)

# Asymmetric Travelling Salesman Problem via Genetic Algorithm
initRoute, bestRoute, progress = \
    tg.geneticAlgorithm(population=tracklist, popSize=100, eliteSize=20,
                        mutationRate=min(0.008, 0.125/numtracks), generations=max(1500, numtracks*50))

# Retrieve initial random-generated route and best route obtained
initRouteIds = [track.id for track in initRoute]
bestRouteIds = [track.id for track in bestRoute]
initRouteWeight = []
bestRouteWeight = []
for i in range(0, numtracks - 1):
    initRoute_firsttrack = initRouteIds[i]
    initRoute_nexttrack = initRouteIds[i+1]
    initRouteWeight.append(adjacencymatrix[initRoute_firsttrack - 1, initRoute_nexttrack - 1])
    bestRoute_firsttrack = bestRouteIds[i]
    bestRoute_nexttrack = bestRouteIds[i+1]
    bestRouteWeight.append(adjacencymatrix[bestRoute_firsttrack - 1, bestRoute_nexttrack - 1])

# Output results
print("Initial Route Details:")
print(initRoute)
print(initRouteIds)
print(initRouteWeight)
print("Best Route Details:")
print(bestRoute)
print(bestRouteIds)
print(bestRouteWeight)

plt.plot(progress)
plt.ylabel('Distance')
plt.xlabel('Generation')
plt.savefig('./output/progress4.png', format="png")
#plt.show()