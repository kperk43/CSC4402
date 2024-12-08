import sqlite3
import os

db_path = "greek_mythology.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    with open("greek_schema.sql", "r") as schema_file:
        schema = schema_file.read()
    cursor.executescript(schema)
    print("Schema executed successfully.")
except Exception as e:
    print(f"Error executing schema: {e}")

deities = [
    ("Zeus", "Sky", "Cronus/Rhea", "Lightning Bolt"),
    ("Hades", "Underworld", "Cronus/Rhea", "Cerberus"),
    ("Poseidon", "Sea", "Cronus/Rhea", "Trident")
]

heroes = [
    ("Heracles", "Thebes", "Zeus/Alcmene", "12 Labors"),
    ("Perseus", "Argos", "Zeus/Danae", "Slayed Medusa"),
    ("Theseus", "Athens", "Aegeus/Poseidon/Aethra", "Slayed Minotaur")
]

try:
    cursor.executemany(
        "INSERT INTO Deity (moniker, domain, parents, symbol) VALUES (?, ?, ?, ?)", deities
    )
    cursor.executemany(
        "INSERT INTO Hero (moniker, origin, parents, legacy) VALUES (?, ?, ?, ?)", heroes
    )
    print("Sample data inserted successfully.")
except Exception as e:
    print(f"Error inserting data: {e}")

conn.commit()
conn.close()
