import pykd


if __name__ == "__main__":

	if not pykd.isWindbgExt():
		print("Script is launch out of WinDBG")
		quit(0)

	pActiveProcessHead = pykd.getOffset("nt!PsActiveProcessHead")
	# or like this:
	#pActiveProcessList = pykd.module("nt").PsActiveProcessHead
	
	dprintln("PsActiveProcessHead is @ 0x%08x"%pActiveProcessHead)
	
	# the boring way would start like this:
	# processList = pykd.typedVarList(pActiveProcessList, "nt!_EPROCESS", "ActiveProcessLinks" )
	
	process_list_head = pykd.typedVar("_TABLE_ENTRY", pActiveProcessList)

	ep_link_offset = pykd.dbgCommand("@@(#FIELD_OFFSET(nt!_EPROCESS,ActiveProcessLinks))")
	
	flink = process_list_head.InLoadOrderLinks.Flink
    first_entry = flink
    # walk forward
    while (flink != 0x0):
        list_entry = typedVar("_LIST_ENTRY", flink)
        dump_module(list_entry)
        flink = list_entry.Flink
        if (first_entry == flink):
            # seen it.
            break
	
	j = 1

	for process in processList:
		pykd.dprint("Process " + str(j)+":")
		name=pykd.loadChars(process.ImageFileName, 16)
		print(name)
		j +=1