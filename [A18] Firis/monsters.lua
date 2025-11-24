function scriptfunction1(t)
   name = readString(0x37143DA0, 50, false)
   race = readString(0x37143E90, 50, false)
   level= readString(0x37143DF0, 50, false)
   expr = readString(0x37144360, 50, false)
   cole = readString(0x371443B0, 50, false)
   hp   = readString(0x37144090, 50, false)
   atk  = readString(0x37144130, 50, false)
   def  = readString(0x371441D0, 50, false)
   spd  = readString(0x37144270, 50, false)
   file = io.open('D:/Projects/cheatengine/[A18] Firis/monsters.txt', 'a+')
   file:write(name .. "\t" .. race .. "\t" .. level .. "\t" .. expr .. "\t" .. cole .. "\t" .. hp .. "\t" .. atk .. "\t" .. def .. "\t" .. spd .. "\n")
   io.close(file)
end


createHotkey(function() scriptfunction1() end, VK_1)