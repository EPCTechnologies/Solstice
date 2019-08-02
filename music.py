import bidict as bd # https://bidict.readthedocs.io/en/latest/basic-usage.html

standkey_camelot = bd.bidict()  # A: minor, B: major
standkey_camelot.update([('Abm', '1A'), ('B', '1B'), ('Ebm', '2A'), ('F#', '2B'),
                    ('Bbm', '3A'), ('Db', '3B'), ('Fm', '4A'), ('Ab', '4B'),
                    ('Cm', '5A'), ('Eb', '5B'), ('Gm', '6A'), ('Bb', '6B'),
                    ('Dm', '7A'), ('F', '7B'), ('Am', '8A'), ('C', '8B'),
                    ('Em', '9A'), ('G', '9B'), ('Bm', '10A'), ('D', '10B'),
                    ('F#m', '11A'), ('A', '11B'), ('Dbm', '12A'), ('E', '12B')])

camelot_kint = bd.bidict()  # modulo 120
camelot_kint.update([('1A', 10), ('1B', 15), ('2A', 20), ('2B', 25),
                    ('3A', 30), ('3B', 35), ('4A', 40), ('4B', 45),
                    ('5A', 50), ('5B', 55), ('6A', 60), ('6B', 65),
                    ('7A', 70), ('7B', 75), ('8A', 80), ('8B', 85),
                    ('9A', 90), ('9B', 95), ('10A', 100), ('10B', 105),
                    ('11A', 110), ('11B', 115), ('12A', 0), ('12B', 5)])

root_n = bd.bidict() # middle A = 440
root_n.update([('A', 49), ('Bb', 50), ('B', 51), ('C', 52),
               ('Db', 53), ('D', 54), ('Eb', 55), ('E', 56),
               ('F', 57), ('F#', 58), ('G', 59), ('Ab', 60)])

def standardise_key(key):  # account for sharp-flat equivalence, standardise using Camelot notation
    if "G#" in key:
        standkey = key.replace("G#", "Ab")
    elif "D#" in key:
        standkey = key.replace("D#", "Eb")
    elif "Gb" in key:
        standkey = key.replace("Gb", "F#")
    elif "A#" in key:
        standkey = key.replace("A#", "Bb")
    elif "C#" in key:
        standkey = key.replace("C#", "Db")
    else:
        standkey = key
    return standkey

def standkey2root(standkey):
    if standkey.endswith("m"):
        root = standkey[:-1]  # remove 'm' from the minor key (text strings)
    else:
        root = standkey
    return root

def root2n(root):
    n = root_n[root]
    return n

def n2root(n):
    root = root_n.inverse[n]
    return root

def n2freq(n):
    freq = 2 ** ((n - 49) / 12.) * 440.
    return freq

def standkey2camelot(standkey):
    camelot = standkey_camelot[standkey]
    return camelot

def camelot2standkey(camelot):
    standkey = standkey_camelot.inverse[camelot]
    return standkey

def camelot2kint(camelot):
    kint = camelot_kint[camelot]
    return kint

def kint2camelot(kint):
    camelot = camelot_kint.inverse[kint]
    return camelot