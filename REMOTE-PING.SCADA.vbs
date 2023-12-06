' **************************************************************************************************************:
' *************************************************** PING SCADA ***********************************************:
' **************************************************************************************************************:
' Author: 	JBallard (JEB)																						:
' Date:		2015.8.28																							:
' Script:	SYSTEM-PING.SCADA.vbs																				:
' Purpose:	A VBScript to ping all Production SCADA hosts														:
' Version:	1.0																									:
' **************************************************************************************************************:
' **************************************************************************************************************:
'
' **************************************************: 
' DEFINE PARAMETERS	& CONFIGURATION PATHS			:
' **************************************************:
Const HARD_DISK = 3
'
StringSystems = "EXPCMX1;EXPXIS1;EXPENG1;EXPXOS1;EXPXOS2;EXPXOS3;EXPXOS4;EXPXOS5;EXPXOS6;EXPUTLSVR1;EXPFILSVR1;"
SplitSystems = split(StringSystems, ";")
'
For Each machine in SplitSystems
    Set ObjPing = GetObject("winmgmts:{impersonationLevel=impersonate}")._
        ExecQuery("SELECT * FROM Win32_PingStatus WHERE address = '" & machine & "'")
    For Each ObjStatus in ObjPing
        If IsNull(ObjStatus.StatusCode) or ObjStatus.StatusCode<>0 Then
            WScript.Echo("SYSTEM " & machine & " IS UNREACHABLE")
        Else
			WScript.Echo("SYSTEM " & machine & " RECEIVED REPLY")
			Set ObjWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & machine & "\root\cimv2")
			Set CountDrives = ObjWMIService.ExecQuery("SELECT * FROM Win32_LogicalDisk WHERE DriveType = " & HARD_DISK & "")
			For Each ObjDisk in CountDrives
				Wscript.Echo "\\" & machine & "\" & " DeviceID: " & " "	& ObjDisk.DeviceID & " - " & _
					"FREE DISK SPACE: " & ObjDisk.FreeSpace / 1024 ^ 3
			Next
        End If
    Next
Next
'
' **********************************:
' END OF SCRIPT						:
' **********************************: