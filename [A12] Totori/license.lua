createHotKey(scriptfunction, VK_S)

scriptfunction = function()
	file = io.open('E:/Projects/cheatengine/[A12] Totori/license.txt', 'a+')
	
	titleAddr = 0x13DBBB58
	descAddr = 0x13DC5F08
	pointAddr = 0x3E90FF60
	bonusAddr = 0x13A23398
	
	title = readString(titleAddr)
	desc = readString(descAddr)
	point = readInteger(pointAddr)
	bonus = readString(bonusAddr)
	
	file:write(title .. "\t" .. desc .. "\t" .. point .. "\t" .. bonus .. "\n")
end