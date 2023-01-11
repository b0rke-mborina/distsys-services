struct Record:
	id: int128
	username: String[50]
	ghlink: String[200]
	filename: String[50]

records: HashMap[int128, Record]

recordCount: public(int128)

@external
def addRecord(_username: String[50], _ghlink: String[200], _filename: String[50]):
	assert len(_username) != 0 and len(_ghlink) != 0 and len(_filename) != 0
	self.records[self.recordCount] = Record({id: self.recordCount, username: _username, ghlink: _ghlink, filename : _filename})
	self.recordCount += 1

@external
def getRecord(id: int128) -> Record:
	return self.records[id]
