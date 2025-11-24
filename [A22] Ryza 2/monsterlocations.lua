function scriptfunction1()
    sleep(100)
	file = io.open('E:/Projects/cheatengine/[A22] Ryza 2/monsterlocations.txt', 'a+')

	nameAddr = 0x370EBEC0
	locAddr1 = 0x370ED4E0

	name = readString(nameAddr)
	loc1 = readString(locAddr1)

	print(name .. "\t" .. loc1 .. "\n")
    file:write(name .. "\t" .. loc1 .. "\n")
end

function scriptfunction2()
    sleep(100)
	file = io.open('E:/Projects/cheatengine/[A22] Ryza 2/monsterlocations.txt', 'a+')

	nameAddr = 0x370EBEC0
	locAddr1 = 0x370ED4E0
	locAddr2 = 0x370ED570

	name = readString(nameAddr)
	loc1 = readString(locAddr1)
	loc2 = readString(locAddr2)

	print(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\n")
    file:write(name .. "\t" .. loc1 .. "\t" .. loc2  .. "\n")
end

function scriptfunction3()
    sleep(100)
	file = io.open('E:/Projects/cheatengine/[A22] Ryza 2/monsterlocations.txt', 'a+')

	nameAddr = 0x370EBEC0
	locAddr1 = 0x370ED4E0
	locAddr2 = 0x370ED570
	locAddr3 = 0x370ED600

	name = readString(nameAddr)
	loc1 = readString(locAddr1)
	loc2 = readString(locAddr2)
	loc3 = readString(locAddr3)

	print(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\t" .. loc3 .. "\n")
    file:write(name .. "\t" .. loc1 .. "\t" .. loc2 .. "\t" .. loc3 .. "\n")
end

hk1=createHotkey(function() scriptfunction1() end, VK_1)
hk2=createHotkey(function() scriptfunction2() end, VK_2)
hk3=createHotkey(function() scriptfunction3() end, VK_3)