import pykd

# Parsing the ProcessList with pykd

if __name__ == "__main__":

	if not pykd.isWindbgExt():
		print("Script cannot be launched outside Windbg")
		quit(0)

	pActiveProcessList = pykd.getOffset("nt!PsActiveProcessHead")
	#pActiveProcessList = pykd.module("nt").PsActiveProcessHead
	processList = pykd.typedVarList(pActiveProcessList, "nt!_EPROCESS", "ActiveProcessLinks" )

	for i, process in enumerate(processList):
		pykd.dprint("Process " + str(i)+":")
		name=pykd.loadCStr(process.ImageFileName)
		print(name)