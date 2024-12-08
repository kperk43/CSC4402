import sqlite3
from faker import Faker
import random

faker = Faker()

conn = sqlite3.connect("greek_mythology.db")
cursor = conn.cursor()

def generate_deities(n=10):
    deities = []
    for _ in range(n):
        name = faker.first_name()
        domain = random.choice(["Sky", "Sea", "Underworld", "Olympus", "Tartarus", "Greece"])
        parents = f"{faker.first_name()}/{faker.first_name()}"
        symbol = faker.word()
        deities.append((name, domain, parents, symbol))
    return deities

def generate_heroes(n=10):
    heroes = []
    for _ in range(n):
        name = faker.first_name()
        origin = faker.city()
        parents = f"{faker.first_name()}/{faker.first_name()}"
        legacy = faker.sentence(nb_words=6)
        heroes.append((name, origin, parents, legacy))
    return heroes

def generate_legends(n=5):
    legends = []
    for _ in range(n):
        title = faker.catch_phrase()
        summary = faker.text(max_nb_chars=200)
        time_period = random.choice(["Ancient Greece", "Myth Era"])
        legends.append((title, summary, time_period))
    return legends

def populate_database():
    try:
        deities = generate_deities()
        heroes = generate_heroes()
        legends = generate_legends()

        cursor.executemany(
            "INSERT INTO Deity (moniker, domain, parents, symbol) VALUES (?, ?, ?, ?)", deities
        )
        cursor.executemany(
            "INSERT INTO Hero (moniker, origin, parents, legacy) VALUES (?, ?, ?, ?)", heroes
        )
        cursor.executemany(
            "INSERT INTO Legend (title, summary, time_period) VALUES (?, ?, ?)", legends
        )

        deity_ids = [row[0] for row in cursor.execute("SELECT id FROM Deity").fetchall()]
        hero_ids = [row[0] for row in cursor.execute("SELECT id FROM Hero").fetchall()]
        legend_ids = [row[0] for row in cursor.execute("SELECT id FROM Legend").fetchall()]

        deity_hero_rels = [(random.choice(deity_ids), random.choice(hero_ids), "Parent") for _ in range(10)]
        hero_legend_rels = [(random.choice(hero_ids), random.choice(legend_ids)) for _ in range(10)]
        deity_legend_rels = [(random.choice(deity_ids), random.choice(legend_ids)) for _ in range(10)]

        cursor.executemany(
            "INSERT INTO DeityHero (deity_id, hero_id, relationship_type) VALUES (?, ?, ?)", deity_hero_rels
        )
        cursor.executemany(
            "INSERT INTO HeroLegend (hero_id, legend_id) VALUES (?, ?)", hero_legend_rels
        )
        cursor.executemany(
            "INSERT INTO DeityLegend (deity_id, legend_id) VALUES (?, ?)", deity_legend_rels
        )

        conn.commit()
        print("Database populated successfully")
    except Exception as e:
        print(f"Error populating database: {e}")
    finally:
        conn.close()

populate_database()
