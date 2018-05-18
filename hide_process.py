import pykd


if __name__ == "__main__":

	if not pykd.isWindbgExt():
		print("Script cannot be launched outside Windbg")
		quit(0)

	if len(sys.argv) < 2:
		print("Expecting process name as argument")
		quit(0)
		
	targetProcessName = sys.argv[1]
	pykd.dprintln("Target: " + targetProcessName)
	
	processList = pykd.typedVarList(pykd.module("nt").PsActiveProcessHead, "nt!_EPROCESS", "ActiveProcessLinks" )

	for i, process in enumerate(processList):
		if pykd.loadCStr(process.ImageFileName) == targetProcessName:
			targetProcessList = pykd.module("nt").typedVar("_LIST_ENTRY", process.ActiveProcessLinks)
			print("ActiveProcessLinks: 0x%08x" %process.ActiveProcessLinks)
			print(targetProcessList)
			#prevFlink = module("nt").typedVar("_LIST_ENTRY",targetProcessList.Blink)
			#nextBlink = module("nt").typedVar("_LIST_ENTRY",targetProcessList.Flink)

			print("prevFlink: 0x%08x" %pykd.ptrQWord(targetProcessList.Blink))
			print("nextBlink: 0x%08x" %pykd.ptrQWord(targetProcessList.Flink+8))
			targetProcessBlink = targetProcessList.Blink
			pykd.writeQWords(targetProcessList.Blink, [targetProcessList.Flink])
			pykd.writeQWords(targetProcessList.Flink, [targetProcessBlink])
			pykd.writeQWords(process.ActiveProcessLinks, [process.ActiveProcessLinks+8])
			pykd.writeQWords(process.ActiveProcessLinks+8, [process.ActiveProcessLinks])
			print("ActiveProcessLinks: 0x%08x" %process.ActiveProcessLinks)
			print(targetProcessList)
			print("prevFlink: 0x%08x" %pykd.ptrQWord(targetProcessList.Blink))
			print("nextBlink: 0x%08x" %pykd.ptrQWord(targetProcessList.Flink+8))
			#created loop
	