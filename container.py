import pykd

if __name__ == "__main__":

	if not pykd.isWindbgExt():
		print("Script is launch out of WinDBG")
		quit(0)

	pActiveProcessList = pykd.getOffset("nt!PsActiveProcessHead")
	#pActiveProcessList = pykd.module("nt").PsActiveProcessHead
	processList = pykd.typedVarList(pActiveProcessList, "nt!_EPROCESS", "ActiveProcessLinks" )

	j = 1

	for process in processList:
		pykd.dprint("Process " + str(j)+":")
		name=pykd.loadChars(process.ImageFileName, 16)
		print(name)
		j +=1