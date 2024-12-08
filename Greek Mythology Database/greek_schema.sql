CREATE TABLE Deity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moniker TEXT NOT NULL,
    domain TEXT,
    parents TEXT,
    symbol TEXT
);

CREATE TABLE Hero (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moniker TEXT NOT NULL,
    origin TEXT,
    parents TEXT,
    legacy TEXT
);

CREATE TABLE Legend (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    summary TEXT,
    time_period TEXT
);

CREATE TABLE DeityHero (
    deity_id INTEGER,
    hero_id INTEGER,
    relationship_type TEXT,
    FOREIGN KEY (deity_id) REFERENCES Deity(id),
    FOREIGN KEY (hero_id) REFERENCES Hero(id)
);

CREATE TABLE HeroLegend (
    hero_id INTEGER,
    legend_id INTEGER,
    FOREIGN KEY (hero_id) REFERENCES Hero(id),
    FOREIGN KEY (legend_id) REFERENCES Legend(id)
);

CREATE TABLE DeityLegend (
    deity_id INTEGER,
    legend_id INTEGER,
    FOREIGN KEY (deity_id) REFERENCES Deity(id),
    FOREIGN KEY (legend_id) REFERENCES Legend(id)
);
