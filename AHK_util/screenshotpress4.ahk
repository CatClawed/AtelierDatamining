#MaxThreadsPerHotkey 2
F12::
	toggle:=!toggle
	While toggle{
      Send {F1 down}
	  Sleep 10
	  Send {F1 up}
	  Send {Down down}
	  Sleep 10
	  Send {Down up}
	  Sleep 400
	  Send {Down down}
	  Sleep 10
	  Send {Down up}
	  Sleep 400
	  Send {Down down}
	  Sleep 10
	  Send {Down up}
	  Sleep 400
	  Send {Down down}
	  Sleep 10
	  Send {Down up}
	  Sleep 400
	}
Return