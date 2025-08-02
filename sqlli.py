import getter


def selectAll(Type, needAll=False):
    rec = getter.getRec()
    L = []
    for key in rec.keys():
        if rec[key]['type'] == Type and (rec[key]['active'] or needAll):
            L.append(key)
    return L