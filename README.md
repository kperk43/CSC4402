# Greek Mythology Library Enterprise
## Usage/Installation
1. Run the connect.py file
2. Install faker library if necessary with "pip install faker" executed in terminal 
3. Run the data_population.py file
4. Run the gui.py file
## Test Queries
1. SELECT * FROM Deity; Fetches all deities
2. SELECT * FROM Hero; Fetches all heroes
3. DELETE FROM Deity WHERE moniker = 'Zeus'; Deletes Zeus deity from the database
4. INSERT INTO Hero (moniker, origin, parents, legacy) VALUES ('Achilles', 'Pthia', 'Peleus/Thetis', 'The Trojan War'); Adds Achilles to the database
5. UPDATE Deity SET domain = 'Sky and Thunder' WHERE moniker = 'Zeus'; Updates Zeus deity's domain with "Sky and Thunder"