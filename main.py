import pandas as pd
import numpy as np
import random

import music as ms
import tspga as tg
import weight as wt

library_df = pd.read_excel('./excel/library.xlsx', sheet_name=0)
print(library_df)
tracklist = []

slowestbpm = min(library_df.iloc[:, 2])
fastestbpm = max(library_df.iloc[:, 2])

for j in range(0, len(library_df)):  # standardise key
    library_df.iat[j, 3] = ms.standardise_key(library_df.iat[j, 3])
    tracklist.append(tg.Track(id=library_df.iat[j, 0], bpm=library_df.iat[j, 2],
                           kint=ms.camelot2kint(ms.standkey2camelot(library_df.iat[j, 3])),
                           freq=ms.n2freq(ms.root2n(ms.standkey2root(library_df.iat[j, 3]))),
                              slowestbpm=slowestbpm, fastestbpm=fastestbpm,
                              name=library_df.iat[j, 1], key=library_df.iat[j, 3]))

tg.geneticAlgorithm(population=tracklist, popSize=100, eliteSize=20, mutationRate=0.01, generations=200)