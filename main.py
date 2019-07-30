import numpy as np
import bidict  # https://bidict.readthedocs.io/en/latest/basic-usage.html

key2camelot = bidict.bidict()  # A: minor, B: major
key2camelot.update([('Abm', '1A'), ('B', '1B'), ('Ebm', '2A'), ('F#', '2B'),
          ('Bbm', '3A'), ('Db', '3B'), ('F', '4A'), ('Ab', '4B'),
          ('Cm', '5A'), ('Ebm', '5B'), ('Gm', '6A'), ('Bb', '6B'),
          ('Dm', '7A'), ('F', '7B'), ('Am', '8A'), ('C', '8B'),
          ('Em', '9A'), ('G', '9B'), ('Bm', '10A'), ('D', '10B'),
          ('F#m', '11A'), ('A', '11B'), ('Dbm', '12A'), ('E', '12B')])

camelot2kint = bidict.bidict()  # modulo 120
camelot2kint.update([('1A', 10), ('1B', 15), ('2A', 20), ('2B', 25),
          ('3A', 30), ('3B', 35), ('4A', 40), ('4B', 45),
          ('5A', 50), ('5B', 55), ('6A', 60), ('6B', 65),
          ('7A', 70), ('7B', 75), ('8A', 80), ('8B', 85),
          ('9A', 90), ('9B', 95), ('10A', 100), ('10B', 105),
          ('11A', 110), ('11B', 115), ('12A', 0), ('12B', 5)])

def squash(x):
    # Sigmoidal: Cannot have f(0) = 0 exactly because this means that
    # an exact match in key or bpm alone would be sufficient.
    sigmoidtight = 3.
    return 1. / (1. + np.exp(sigmoidtight - 2. * sigmoidtight * x))

def bpm_diff(firstbpm, nextbpm, slowestbpm, fastestbpm):
    slowpenalty = 2.
    if nextbpm >= firstbpm:
        return squash((nextbpm - firstbpm) / (fastestbpm - slowestbpm))
    else:  # penalise reductions in bpm
        return squash(slowpenalty * (firstbpm - nextbpm) / (fastestbpm - slowestbpm))

def key_diff(firstkey, nextkey):
    firstkint = camelot2kint[firstkey]
    nextkint = camelot2kint[nextkey]
    diffkint = np.mod(nextkint - firstkint, 120)
    energypenalty = 0.025  # penalise drop in energy level associated with pitch drops
    if diffkint == 0:
        return squash(0.)
    elif (diffkint == 10 | diffkint == -110):
        return squash(0.1)
    elif (diffkint == -10 | diffkint == 110):
        return squash(0.1 + energypenalty)
    elif (diffkint == 5 | diffkint == -115) & (firstkey // 10 == nextkey // 10):
        return squash(0.2)
    elif (diffkint == -5 | diffkint == 115) & (firstkey // 10 == nextkey // 10):
        return squash(0.2 + energypenalty)
    elif (diffkint == 5 | diffkint == -115) & (firstkey // 10 != nextkey // 10):
        return squash(0.25)
    elif (diffkint == -5 | diffkint == 115) & (firstkey // 10 != nextkey // 10):
        return squash(0.25 + energypenalty)
    elif (diffkint == 15 | diffkint == -105):
        return squash(0.3)
    elif (diffkint == -15 | diffkint == 105):
        return squash(0.3 + energypenalty)
    elif (diffkint == 20 | diffkint == -100):
        return squash(0.3)
    elif (diffkint == 35 | diffkint == -85) & (firstkey % 10 == 0):
        return squash(0.4)
    elif (diffkint == -30 | diffkint == 90) & (firstkey % 10 == 0):
        return squash(0.425 + energypenalty)
    elif (diffkint == 70 | diffkint == -50):
        return squash(0.5)
    else:
        return squash(1.)

def score(track1, track2):
    return 1.