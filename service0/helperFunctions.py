import aiosqlite
import numpy as np
import pandas as pd


# retrieves random rows from database
async def fetchRandomRows(connection):
	# get total number of rows in the database table and generate random indices for selection
	cursor = await connection.cursor()
	await cursor.execute("SELECT COUNT(*) FROM datatable")
	(numberOfRows, ) = await cursor.fetchone()
	randomRowIndices = np.random.randint(0, numberOfRows, size = 100)

	# fetch and return the rows with the randomly selected indices
	rows = []
	for rowIndex in randomRowIndices:
		await cursor.execute("SELECT * FROM datatable LIMIT 1 OFFSET %s"%(rowIndex))
		rows.append(await cursor.fetchone())
	# print(rows[1], "\n\n =========", rows[2])
	# print(len(rows))
	return rows

# reads json file with data and stores said data to database
async def addDataToDatabase():
	try:
		dataframe = pd.read_json("data/dataset.json", lines = True)
		async with aiosqlite.connect("distsys-services-database.db") as db:
			for index, row in dataframe.head(1000).iterrows(): # 10000
				# print("ROW", index + 1)
				# print(row.get("repo_name"))
				# print(row.get("repo_name").split("/")[0])
				# print("https://github.com/%s"%(row.get("repo_name")))
				# print(row.get("path"))
				# print(row.get("path").split("/")[-1])
				# print(row.get("content"))
				await db.execute(
					"INSERT INTO datatable (username, ghlink, filename, content) VALUES (?, ?, ?, ?)",
					(
						row.get("repo_name").split("/")[0],
						"https://github.com/%s"%(row.get("repo_name")),
						row.get("path").split("/")[-1],
						row.get("content")
					)
				)
				await db.commit()
		print("Added data to database successfuly.")
	except Exception as e:
		print("Error occured while adding data to database from dataset:", e)
	pass
