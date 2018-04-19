import pykd

# 
def firstNumberInString(string):
	# meant to get the middle number out of Windbgs: "Evaluate expression: 1104 = 00000000`00000450"
	return [int(s) for s in string.split() if s.isdigit()][0]

if __name__ == "__main__":

	if not pykd.isWindbgExt():
		print("Script cannot be launched outside Windbg")
		quit(0)

	# Get PsActiveProcessHead
	pActiveProcessHead = pykd.getOffset("nt!PsActiveProcessHead")
	
	# Dereference PsActiveProcessHead == Forward link to first process 
	initial_flink = pykd.ptrPtr(pActiveProcessHead)
	pykd.dprintln("Initial Flink: @ 0x%08x"%initial_flink)
	
	# Get structure offsets
	s = pykd.dbgCommand("? @@(#FIELD_OFFSET(nt!_EPROCESS,ActiveProcessLinks))")
	offset_eprocess_activeProcesslinks = firstNumberInString(s)
	pykd.dprintln("Offset EPROCESS-ActiveProcessLinks: " + str(offset_eprocess_activeProcesslinks))
	s = pykd.dbgCommand("? @@(#FIELD_OFFSET(nt!_EPROCESS, ImageFileName))")
	offset_eprocess_imageName = firstNumberInString(s)
	pykd.dprintln("Offset EPROCESS-ImageName: " + str(offset_eprocess_imageName))
	
	# go through process list and print ImageNames
	currentEntry  = pykd.ptrPtr(pActiveProcessHead)
	while (currentEntry != pActiveProcessHead):
		pykd.dprintln("Current Flink:  @ 0x%08x"%currentEntry)
		pCurrentEProcessObject = currentEntry - offset_eprocess_activeProcesslinks
		pykd.dprintln("Current EPROCESS address: @ 0x%08x"%pCurrentEProcessObject)
		currentImageName = pykd.loadCStr( pCurrentEProcessObject + offset_eprocess_imageName )
		pykd.dprintln("Current ImageName: "  + currentImageName)
		
		currentEntry = pykd.ptrPtr(pCurrentEProcessObject + offset_eprocess_activeProcesslinks)
		
	pykd.dprintln("Done")