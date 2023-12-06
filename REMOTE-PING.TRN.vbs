' **************************************************************************************************************:
' ************************************************** PING TRAINER **********************************************:
' **************************************************************************************************************:
' Author: 	JBallard (JEB)																						:
' Date:		2015.80.28																							:
' Script:	SYSTEM-TRN.NETWORK.MAP.vbs																			:
' Purpose:	A VBScript to ping all Pipeline Trainer hosts														:
' Version:	1.0																									:
' **************************************************************************************************************:
' **************************************************************************************************************:
'
' **************************************************: 
' DEFINE PARAMETERS	& CONFIGURATION PATHS			:
' **************************************************:
Const HARD_DISK = 3

'strMachines = "PPMDB1-PCC;PPMDB1-PCC;10.65.1.3;10.65.3.1;EXPTRN1;EXPTRN2;EXPTRESSR1;EXPLDBTSR4;EXPLDBTSR4-THM;EXPTRNWS1;"
strMachines = "PPMDB1-PCC;"
aMachines = split(strMachines, ";")
 
For Each machine in aMachines
    Set objPing = GetObject("winmgmts:{impersonationLevel=impersonate}")._
        ExecQuery("select * from Win32_PingStatus where address = '" & machine & "'")		
    For Each objStatus in objPing
        If IsNull(objStatus.StatusCode) or objStatus.StatusCode<>0 Then 
            WScript.Echo("Computer " & machine & " Unreachable") 
        Else
			WScript.Echo("Computer " & machine & " Received Reply")
			
			Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & machine & "\root\cimv2")			
			Set colDisks = objWMIService.ExecQuery("SELECT * FROM Win32_LogicalDisk WHERE DriveType = " & HARD_DISK & "")					
			For Each objDisk in colDisks
				Wscript.Echo "\\" & machine & "\" & " DeviceID: " & " "	& objDisk.DeviceID & " - " & "Free Disk Space: " & objDisk.FreeSpace / 1024 ^ 3    
			Next			
			
        End If
    Next
Next

' **********************************:
' END OF SCRIPT						:
' **********************************: