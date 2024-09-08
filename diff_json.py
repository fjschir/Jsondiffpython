import json
import math

# Funktion, um festzustellen, ob zwei Zahlen ähnlich sind


def sind_zahlen_ähnlich(val1, val2):
    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        return math.isclose(float(val1), float(val2), rel_tol=1e-9)
    return False

# Funktion, um die Unterschiede zwischen zwei JSON-Objekten zu vergleichen


def finde_unterschiede(datei1, datei2):
    unterschiede = []

    objekte1 = {obj['ObjektNr']: obj for obj in datei1}
    objekte2 = {obj['ObjektNr']: obj for obj in datei2}

    # Vergleich der Objekte in datei1
    for objekt_nr, objekt1 in objekte1.items():
        if objekt_nr in objekte2:
            objekt2 = objekte2[objekt_nr]

            for key in objekt1:
                if key in objekt2:
                    val1 = objekt1[key]
                    val2 = objekt2[key]

                    if not (sind_zahlen_ähnlich(val1, val2) or val1 == val2):
                        unterschiede.append({
                            "ObjektNr": objekt_nr,
                            "Key": key,
                            "Value1": val1,
                            "Value2": val2
                        })
                else:
                    unterschiede.append({
                        "ObjektNr": objekt_nr,
                        "Key": key,
                        "Value1": objekt1[key],
                        "Value2": None
                    })
        else:
            unterschiede.append({
                "ObjektNr": objekt_nr,
                "Key": "Alle",
                "Value1": objekt1,
                "Value2": None
            })

    # Vergleich der Objekte in datei2, die nicht in datei1 sind
    for objekt_nr, objekt2 in objekte2.items():
        if objekt_nr not in objekte1:
            unterschiede.append({
                "ObjektNr": objekt_nr,
                "Key": "Alle",
                "Value1": None,
                "Value2": objekt2
            })

    return unterschiede


# Einlesen der JSON-Dateien
with open('datei1.json', 'r', encoding='utf-8') as file1:
    datei1 = json.load(file1)

with open('datei2.json', 'r', encoding='utf-8') as file2:
    datei2 = json.load(file2)

# Finde die Unterschiede (jetzt wird direkt die Liste verwendet)
unterschiede = finde_unterschiede(datei1, datei2)

# Schreibe die Unterschiede in unterschiede.json
with open('unterschiede.json', 'w', encoding='utf-8') as out_file:
    json.dump(unterschiede, out_file, ensure_ascii=False, indent=4)

print("Die Unterschiede wurden erfolgreich in 'unterschiede.json' gespeichert.")
