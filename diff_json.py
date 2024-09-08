import json

# Funktion, um festzustellen, ob zwei Werte (einschließlich Zahlen) gleich sind


def sind_werte_gleich(val1, val2):
    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        return val1 == val2
    return val1 == val2

# Funktion, um die Unterschiede zwischen zwei JSON-Dateien zu finden


def finde_unterschiede(datei1, datei2):
    unterschiede = []
    unterschiedliche_objektnr = set()

    # Erstellen eines eindeutigen Schlüssels für jedes Objekt basierend auf ObjektNr und Key
    objekte1 = {(obj['ObjektNr'], obj['Key']): obj['Value'] for obj in datei1}
    objekte2 = {(obj['ObjektNr'], obj['Key']): obj['Value'] for obj in datei2}

    # Vergleich der Objekte in datei1 mit datei2
    for key, value1 in objekte1.items():
        if key in objekte2:
            value2 = objekte2[key]
            if not sind_werte_gleich(value1, value2):
                unterschiede.append({
                    "ObjektNr": key[0],
                    "Key": key[1],
                    "Value1": value1,
                    "Value2": value2
                })
                unterschiedliche_objektnr.add(key[0])
        else:
            unterschiede.append({
                "ObjektNr": key[0],
                "Key": key[1],
                "Value1": value1,
                "Value2": None
            })
            unterschiedliche_objektnr.add(key[0])

    # Vergleich der Objekte in datei2, die nicht in datei1 sind
    for key, value2 in objekte2.items():
        if key not in objekte1:
            unterschiede.append({
                "ObjektNr": key[0],
                "Key": key[1],
                "Value1": None,
                "Value2": value2
            })
            unterschiedliche_objektnr.add(key[0])

    return unterschiede, list(unterschiedliche_objektnr)


# Einlesen der JSON-Dateien
with open('datei1.json', 'r', encoding='utf-8') as file1:
    datei1 = json.load(file1)

with open('datei2.json', 'r', encoding='utf-8') as file2:
    datei2 = json.load(file2)

# Finde die Unterschiede und die ObjektNrs
unterschiede, unterschiedliche_objektnr = finde_unterschiede(datei1, datei2)

# Überprüfen, ob es Unterschiede gibt und speichere sie in unterschiede.json
if unterschiede:
    with open('unterschiede.json', 'w', encoding='utf-8') as out_file:
        json.dump(unterschiede, out_file, ensure_ascii=False, indent=4)
    print("Es gibt Unterschiede. Die Unterschiede wurden in 'unterschiede.json' gespeichert.")
    print(f"Die folgenden ObjektNrs weisen Unterschiede auf: {
          unterschiedliche_objektnr}")
else:
    print("Es gibt keine Unterschiede zwischen den beiden Dateien.")
