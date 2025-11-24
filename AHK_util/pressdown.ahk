#MaxThreadsPerHotkey 2
F12::
	toggle:=!toggle
	While toggle{
	  Send {Down down}
	  Sleep 10
	  Send {Down up}
	  Sleep 400
	}
Return