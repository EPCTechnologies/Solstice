import pandas as pd
import numpy as np

import music as ms
import tspga as tg
import weight as wt

library_df = pd.read_excel('./excel/library.xlsx', sheet_name=0)

print(wt.key_diff("C", "C"))
print(wt.key_diff("C", "Db"))
print(wt.key_diff("C", "D"))
print(wt.key_diff("C", "Eb"))
print(wt.key_diff("C", "E"))
print(wt.key_diff("C", "F"))
print(wt.key_diff("C", "F#"))
print(wt.key_diff("C", "G"))
print(wt.key_diff("C", "Ab"))
print(wt.key_diff("C", "A"))
print(wt.key_diff("C", "Bb"))
print(wt.key_diff("C", "B"))
print(wt.key_diff("C", "Cm"))
print(wt.key_diff("C", "Dbm"))
print(wt.key_diff("C", "Dm"))
print(wt.key_diff("C", "Ebm"))
print(wt.key_diff("C", "Em"))
print(wt.key_diff("C", "Fm"))
print(wt.key_diff("C", "F#m"))
print(wt.key_diff("C", "Gm"))
print(wt.key_diff("C", "Abm"))
print(wt.key_diff("C", "Am"))
print(wt.key_diff("C", "Bbm"))
print(wt.key_diff("C", "Bm"))