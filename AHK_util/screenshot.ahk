#MaxThreadsPerHotkey 2
F12::
	toggle:=!toggle
	While toggle{
	  Send {Down down}
	  Sleep 10
	  Send {Down up}
	  Send {F1 down}
	  Sleep 10
	  Send {F1 up}
	  Sleep 900
	}
Return