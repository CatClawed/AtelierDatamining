-- effects and traits
nameAddr1 = 0x88B50280
nameAddr2 = 0x88AAE0C0
nameAddr3 = 0x88AAE2A0
nameAddr4 = 0x88AAE480
descAddr1 = 0x88AA5CE0
descAddr2 = 0x88AAEF80
descAddr3 = 0x88AAE700
descAddr4 = 0x88AAEEA0

prev = readString(nameAddr1, 30, false)
file = io.open('E:/Projects/cheatengine/[A15] Escha/6_traitEN.txt', 'a+')

function readValueTimer(t)
  name1=readString(nameAddr1, 30, false)
  name2=readString(nameAddr2, 30, false)
  name3=readString(nameAddr3, 30, false)
  name4=readString(nameAddr4, 30, false)
  if name1 ~= prev then --value changed
    file = io.open('E:/Projects/cheatengine/[A15] Escha/6_traitEN.txt', 'a+')
    desc1 = readString(descAddr1, 300, false)
	desc2 = readString(descAddr2, 300, false)
	desc3 = readString(descAddr3, 300, false)
	desc4 = readString(descAddr4, 300, false)
	file:write(name1 .. "\t" .. desc1 .. "\n")
	file:write(name2 .. "\t" .. desc2 .. "\n")
	file:write(name3 .. "\t" .. desc3 .. "\n")
	file:write(name4 .. "\t" .. desc4 .. "\n")
    prev=name1
	io.close(file)
  end
end

t1=createTimer(nil)
timer_setInterval(t1,100) --check every 1/100th second if the value has changed
timer_onTimer(t1,readValueTimer)
--
nameAddr = 0x88AAF800
descAddr = 0x88B50360
prev = readString(nameAddr, 30, false)

function readValueTimer(t)
  name=readString(nameAddr, 30, false)
  if name ~= prev then --value changed
    file = io.open('E:/Projects/cheatengine/[A15] Escha/7_booksEN.txt', 'a+')
    desc = readString(descAddr, 300, false)
	file:write(name .. "\t" .. desc .. "\n")
    prev=name
	io.close(file)
  end
end

t1=createTimer(nil)
timer_setInterval(t1,100) --check every 1/100th second if the value has changed
timer_onTimer(t1,readValueTimer)
--monster
nameAddr = 0x88AB2F80
descAddr = 0x88B50780
specAddr = 0x88AB42E0
prev = readString(nameAddr, 30, false)

function readValueTimer(t)
  name=readString(nameAddr, 30, false)
  if name ~= prev then --value changed
    file = io.open('E:/Projects/cheatengine/[A15] Escha/8_monsterEN.txt', 'a+')
    desc = readString(descAddr, 300, false)
    spec=readString(specAddr, 30, false)
	file:write(name .. "\t" .. desc .. "\t" .. spec .. "\n")
    prev=name
	io.close(file)
  end
end

t1=createTimer(nil)
timer_setInterval(t1,100) --check every 1/100th second if the value has changed
timer_onTimer(t1,readValueTimer)
-- more monster
nameAddr = 0x88AB2F80
hpAddr = 0x806FC35C
atkAddr = 0x806FD09C
defAddr = 0x806FDF7C
spdAddr = 0x806A351C
fireAddr = 0x806A429C
waterAddr = 0x806A515C
windAddr = 0x806A5E9C
earthAddr = 0x806A6D7C
levelAddr = 0x80716D5C
expAddr = 0x806D355C
coleAddr = 0x806E9F1C
prev = readString(nameAddr, 30, false)

function readValueTimer(t)
  name=readString(nameAddr, 30, false)
  if name ~= prev then --value changed
    file = io.open('E:/Projects/cheatengine/[A15] Escha/monexp.txt', 'a+')
    exp=readString(expAddr, 30, false)
    cole=readString(coleAddr, 30, false)
    level=readString(levelAddr, 30, false)
	file:write(name .. "\t" .. level .. "\t" .. exp .. "\t" .. cole .. "\n")
    prev=name
	io.close(file)
  end
end

t1=createTimer(nil)
timer_setInterval(t1,100) --check every 1/100th second if the value has changed
timer_onTimer(t1,readValueTimer)
-- button press stuff
function scriptfunction1()

    sleep(50)
	file = io.open('E:/Projects/cheatengine/[A15] Escha/materialEN.txt', 'a+')

	nameAddr = 0x88AC4140
	descAddr = 0x88B13800

	ogname = readString(nameAddr, 30, false)
	desc = readString(descAddr, 300, false)
	--print(ogname .. "\t" .. desc .. "\n")
    file:write(ogname .. "\t" .. desc .. "\n")
	sleep(100)
	doKeyPress(0x28)
	sleep(100)
	name = readString(nameAddr, 30, false)
	desc = readString(descAddr, 300, false)

	while(name ~= ogname)
	do
		--print(name .. "\t" .. desc .. "\n")
        file:write(name .. "\t" .. desc .. "\n")
		doKeyPress(0x28)
		sleep(100)
	    name = readString(nameAddr, 30, false)
	    desc = readString(descAddr, 300, false)
	end

end

hk1=createHotkey(function() scriptfunction1() end, VK_1)