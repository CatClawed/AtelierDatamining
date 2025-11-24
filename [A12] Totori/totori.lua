-- this was in the shallie folder but I think it is indeed some of my totori code

object_destroy(t)
object_destroy(t1)
-- names
prev = readString(0x12E752C8, 50, false)

function readValueTimer(t)
   name = readString(0x12E752C8, 50, false)
   if name ~= prev then
      file = io.open('E:/Projects/cheatengine/[A16] Shallie/file.txt', 'a+')
	  file:write(name .. "\n")
	  prev=name
	  io.close(file)
   end
end

t1=createTimer(nil)
timer_setInterval(t1,200)
timer_onTimer(t1,readValueTimer)
-- eff/trait
-- names
prev = readString(0x36AD4FD0, 50, false)

function readValueTimer(t)
   name  = readString(0x36AD4FD0, 50, false)
   name2 = readString(0x36AD6140, 50, false)
   name3 = readString(0x131F2938, 50, false)
   name4 = readString(0x36AD51C0, 50, false)
   if name ~= prev then
      file = io.open('E:/Projects/cheatengine/[A16] Shallie/file.txt', 'a+')
	  file:write(name  .. "\n")
	  file:write(name2 .. "\n")
	  file:write(name3 .. "\n")
	  file:write(name4 .. "\n")
	  prev=name
	  io.close(file)
   end
end

t1=createTimer(nil)
timer_setInterval(t1,500) --check every 1/100th second if the value has changed
timer_onTimer(t1,readValueTimer)