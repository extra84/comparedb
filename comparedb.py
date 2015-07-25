# Usage : python dbcompare.py SourceServer path\to\database.nsf TargetServer
# Use "" for local
# Result is unpredictable if target server contains multiple replicas with the same ReplicaID

# This script needs pywin32

import sys
from win32com.client import Dispatch

step=0

# Return UNID list of all the documents in the provided collection
def getids(coll):
	ids=[]
	doc=coll.getfirstdocument() 
	while doc !=None:
		ids.append(doc.universalid)
		if not doc.isValid :
			print ("Invalid document")
		doc=coll.getnextdocument(doc)
	return ids


s=Dispatch("Lotus.NotesSession")
s.initialize()

srvsrc = sys.argv[1]
srvtgt =sys.argv[3]

# Open source db
dbdir=s.getDbDirectory(srvtgt)
dbsrc=s.getdatabase(srvsrc,sys.argv[2])

# Open target db
dbtgt=dbdir.OpenDatabaseByReplicaID(dbsrc.ReplicaId)

# retrieve a list of all documents in the database
step=step + 1
print ("%d - Retrieving documents" % step)
docsrc=dbsrc.AllDocuments
doctgt=dbtgt.AllDocuments

# make a list of UNID for each db 
step=step + 1
print ("%d - Retrieving UNIDs" % step)
idsrc=getids(docsrc)
idtgt=getids(doctgt)


# Printing missing documents
missing=False
step=step + 1
print ("%d - Report :\n" %step)

# Id of documents present in source database and missing in target database
for id in idsrc:
	if not id in idtgt:
		conflict=""
		form=dbsrc.getdocumentbyunid(id).getitemvalue("form")[0]
		if dbsrc.getdocumentbyunid(id).hasitem("$conflict"):
			conflict="conflit" 
		print ("document %s (%s) missing from target db on server '%s' /!\ %s" % (id,form,srvtgt,conflict ))
		missing=True

# Id of documents present in target database and missing in source database
for id in idtgt:
	if not id in idsrc:
		conflict=""
		form=dbtgt.getdocumentbyunid(id).getitemvalue("form")[0]
		if dbtgt.getdocumentbyunid(id).hasitem("$conflict"):
			conflict="conflit" 
		print ("document %s (%s) missing from source db on server '%s' /!\ %s" % (id,form,srvsrc,conflict))
		missing=True

if not missing:
	print ("Replicas are synchronized\n")
	
		