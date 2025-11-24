object_destroy(t)
object_destroy(t1)
-- monsters en
prev = readString(0x891486A0, 50, false)

function readValueTimer(t)
   name = readString(0x891486A0, 50, false)
   desc = readString(0x89159410, 500, false)
   race = readString(0x891511F0, 50, false)
   level= readString(0x890E2080, 50, false)
   expr = readString(0x890EDAA0, 50, false)
   cole = readString(0x890EE110, 50, false)
   hp   = readString(0x890EF460, 50, false)
   atk  = readString(0x890F0140, 50, false)
   def  = readString(0x890F0E20, 50, false)
   spd  = readString(0x890F1B00, 50, false)
   if name ~= prev then
      file = io.open('E:/Projects/cheatengine/[A16] Shallie/monsters.txt', 'a+')
	  file:write(name .. "\t" .. desc .. "\t" .. race .. "\t" .. level .. "\t" .. expr .. "\t" .. cole .. "\t" .. hp .. "\t" .. atk .. "\t" .. def .. "\t" .. spd .. "\n")
	  prev=name
	  io.close(file)
   end
end

t1=createTimer(nil)
timer_setInterval(t1,100) --check every 1/100th second if the value has changed
timer_onTimer(t1,readValueTimer)
--items en
prev = readString(0x8914E5F0, 50, false)

function readValueTimer(t)
   name = readString(0x8914E5F0, 50, false)
   desc = readString(0x8914F3E0, 500, false)
   if name ~= prev then
      file = io.open('E:/Projects/cheatengine/[A16] Shallie/file.txt', 'a+')
	  file:write(name .. "\t" .. desc .. "\n")
	  prev=name
	  io.close(file)
   end
end

t1=createTimer(nil)
timer_setInterval(t1,150)
timer_onTimer(t1,readValueTimer)
-- synth props en
prev = readString(0x891DA9A0, 50, false)

function readValueTimer(t)
   name = readString(0x891DA9A0, 50, false)
   desc = readString(0x891DB790, 500, false)
   pr1 = readString(0x89244650, 50, false)
   pr2 = readString(0x89244D90, 50, false)
   pr3 = readString(0x892454D0, 50, false)
   if name ~= prev then
      file = io.open('E:/Projects/cheatengine/[A16] Shallie/items.txt', 'a+')
	  file:write(name .. "\t" .. desc .. "\t" .. pr1 .. "\t" .. pr2  .. "\t" .. pr3 .. "\n")
	  prev=name
	  io.close(file)
   end
end

t1=createTimer(nil)
timer_setInterval(t1,100) --check every 1/100th second if the value has changed
timer_onTimer(t1,readValueTimer)
--eff/prop
prev = readString(0x8914E2B0, 50, false)

function readValueTimer(t)
   name1 = readString(0x8914E2B0, 50, false)
   name2 = readString(0x8914E300, 50, false)
   name3 = readString(0x8915E170, 50, false)
   name4 = readString(0x8915EF80, 50, false)
   desc1 = readString(0x8915D2C0, 500, false)
   desc2 = readString(0x8915E080, 500, false)
   desc3 = readString(0x8915EE90, 500, false)
   desc4 = readString(0x8915FCA0, 500, false)
   if name1 ~= prev then
      file = io.open('E:/Projects/cheatengine/[A16] Shallie/file.txt', 'a+')
	  file:write(name1 .. "\t" .. desc1 .. "\n")
	  file:write(name2 .. "\t" .. desc2 .. "\n")
	  file:write(name3 .. "\t" .. desc3 .. "\n")
	  file:write(name4 .. "\t" .. desc4 .. "\n")
	  prev=name1
	  io.close(file)
   end
end

t1=createTimer(nil)
timer_setInterval(t1,150)
timer_onTimer(t1,readValueTimer)
-- eff numbers
prev = readString(0x89121E10, 50, false)

function readValueTimer(t)
   Sleep(50)
   name   = readString(0x 89121E10, 50, false)
   one    = readString(0x 8912AB90, 10, false)
   two    = readString(0x 8912B870, 10, false)
   three  = readString(0x 8912C550, 10, false)
   four   = readString(0x 8912D8A0, 10, false)
   five   = readString(0x 8912E580, 10, false)
   six    = readString(0x 8912F260, 10, false)
   seven  = readString(0x 89130DE0, 10, false)
   eight  = readString(0x 89131AC0, 10, false)
   nine   = readString(0x 891327A0, 10, false)
   ten    = readString(0x 89133AF0, 10, false)
   eleven = readString(0x 891347D0, 10, false)
   twelve = readString(0x 891354B0, 10, false)
   if name ~= prev then
      file = io.open('E:/Projects/cheatengine/[A16] Shallie/effs.txt', 'a+')
	  file:write(name .. "\t" .. one .. "\t" .. two .. "\t" .. three .. "\n")
	  file:write(name .. "\t" .. four .. "\t" .. five .. "\t" .. six .. "\n")
	  file:write(name .. "\t" .. seven .. "\t" .. eight .. "\t" .. nine .. "\n")
	  file:write(name .. "\t" .. ten .. "\t" .. eleven .. "\t" .. twelve .. "\n")
	  prev=name
	  io.close(file)
   end
end

t1=createTimer(nil)
timer_setInterval(t1,100)
timer_onTimer(t1,readValueTimer)
-- wep eff
-- eff numbers
prev = readString(0x89296EA0, 50, false)

function readValueTimer(t)
   Sleep(50)
   name   = readString(0x89296EA0, 50, false)
   one    = readString(0x892A5E70, 10, false)
   two    = readString(0x892A6B50, 10, false)
   if name ~= prev then
      file = io.open('E:/Projects/cheatengine/[A16] Shallie/effs.txt', 'a+')
	  file:write(name .. "\t" .. one .. "\t" .. two .. "\n")
	  file:write(name .. "\t" .. one .. "\t" .. two .. "\n")
	  file:write(name .. "\t" .. one .. "\t" .. two .. "\n")
	  file:write(name .. "\t" .. one .. "\t" .. two .. "\n")
	  prev=name
	  io.close(file)
   end
end

t1=createTimer(nil)
timer_setInterval(t1,100)
timer_onTimer(t1,readValueTimer)