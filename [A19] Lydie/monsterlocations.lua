function scriptfunction1()
    sleep(100)
	file = io.open('D:/Projects/cheatengine/[A19] Lydie/monsterlocations.txt', 'a+')

	nameAddr = 0x36CFF6F0
	locAddr1 = 0x36CFFF90
	locAddr2 = 0x36CFFFE0
	locAddr3 = 0x36D00030
	locAddr4 = 0x36D00080
	locAddr5 = 0x36D000D0

	name = readString(nameAddr)
	loc1 = readString(locAddr1)

	--print(name .. "\t" .. loc1 .. "\n")
    file:write(name .. "\t" .. loc1 .. "\n")
end

function scriptfunction2()
    sleep(100)
	file = io.open('D:/Projects/cheatengine/[A19] Lydie/monsterlocations.txt', 'a+')

	nameAddr = 0x36CFF6F0
	locAddr1 = 0x36CFFF90
	locAddr2 = 0x36CFFFE0
	locAddr3 = 0x36D00030
	locAddr4 = 0x36D00080
	locAddr5 = 0x36D000D0

	name = readString(nameAddr)
	loc1 = readString(locAddr1)
	loc2 = readString(locAddr2)

	--print(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\n")
    file:write(name .. "\t" .. loc1 .. "\t" .. loc2  .. "\n")
end

function scriptfunction3()
    sleep(100)
	file = io.open('D:/Projects/cheatengine/[A19] Lydie/monsterlocations.txt', 'a+')

	nameAddr = 0x36CFF6F0
	locAddr1 = 0x36CFFF90
	locAddr2 = 0x36CFFFE0
	locAddr3 = 0x36D00030
	locAddr4 = 0x36D00080
	locAddr5 = 0x36D000D0

	name = readString(nameAddr)
	loc1 = readString(locAddr1)
	loc2 = readString(locAddr2)
	loc3 = readString(locAddr3)

	--print(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\t" .. loc3 .. "\n")
    file:write(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\t" .. loc3 .. "\n")
end

function scriptfunction4()
    sleep(100)
	file = io.open('D:/Projects/cheatengine/[A19] Lydie/monsterlocations.txt', 'a+')

	nameAddr = 0x36CFF6F0
	locAddr1 = 0x36CFFF90
	locAddr2 = 0x36CFFFE0
	locAddr3 = 0x36D00030
	locAddr4 = 0x36D00080
	locAddr5 = 0x36D000D0

	name = readString(nameAddr)
	loc1 = readString(locAddr1)
	loc2 = readString(locAddr2)
	loc3 = readString(locAddr3)
	loc4 = readString(locAddr4)

	--print(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\t" .. loc3 .. "\t" .. loc4 .. "\n")
    file:write(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\t" .. loc3 .. "\t" .. loc4 .. "\n")
end

function scriptfunction5()
    sleep(100)
	file = io.open('D:/Projects/cheatengine/[A19] Lydie/monsterlocations.txt', 'a+')

	nameAddr = 0x36CFF6F0
	locAddr1 = 0x36CFFF90
	locAddr2 = 0x36CFFFE0
	locAddr3 = 0x36D00030
	locAddr4 = 0x36D00080
	locAddr5 = 0x36D000D0

	name = readString(nameAddr)
	loc1 = readString(locAddr1)
	loc2 = readString(locAddr2)
	loc3 = readString(locAddr3)
	loc4 = readString(locAddr4)
	loc5 = readString(locAddr5)

	--print(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\t" .. loc3 .. "\t" .. loc4 .. "\t" .. loc5 .. "\n")
    file:write(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\t" .. loc3 .. "\t" .. loc4 .. "\t" .. loc5 .. "\n")
end

createHotkey(function() scriptfunction1() end, VK_1)
createHotkey(function() scriptfunction2() end, VK_2)
createHotkey(function() scriptfunction3() end, VK_3)
createHotkey(function() scriptfunction4() end, VK_4)
createHotkey(function() scriptfunction5() end, VK_5)