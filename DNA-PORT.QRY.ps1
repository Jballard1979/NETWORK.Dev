#-- ************************************************************************************************************:
#-- ********************************************* QUERY DNA PORTS **********************************************:
#-- ************************************************************************************************************:
#-- Author:   JBallard (JEB)                                                                                    :
#-- Date:     2020.4.01                                                                                         :
#-- Script:   DNA-PORT.QRY.ps1                                                                                  :
#-- Purpose:  A PowerShell script that listens for open ports & verifies they are accessable                    :
#-- Example:  Portqry.exe -n 10.165.3.112 -e 80                                                                 :
#-- Version:  1.0                                                                                               :
#-- ************************************************************************************************************:
#-- ************************************************************************************************************:
#--
#-- ********************************************************:
#-- DEFINE PARAMETERS & CONFIGURATION PATHS                 :
#-- ********************************************************:
Param([string]$Server)
#--
#-- STATUS ARRAY OF PORTS:
workflow Check-Port
{
	param ([string[]]$RPCServer,[array]$ArrayRPCPorts)
	$System = hostname
	ForEach -parallel ($RPCPort in $ArrayRPCPorts)
	{
		$BolResult = InlineScript{Test-NetConnection -ComputerName $Using:RPCServer -port $Using:RPCPort _
		-InformationLevel Quiet}
		If ($BolResult)
		{
			Write-Output "$RPCPort ON $RPCServer WAS SUCCESSFULLY REACHED:"
		}
		Else
		{
			Write-Output "$RPCPort ON $RPCServer WAS NOT ACCESSABLE:"
		}
	}
}
#--
#-- RPC PORT & BINARY PATH:
$StrRPCPort = "135"
$StrPortQryPath = "C:\Program Files\PortQry"
If (Test-Path "$StrPortQryPath\PortQry.exe")
{
	$StrPortQryCmd = "$StrPortQryPath\PortQry.exe -e $StrRPCPort -n $Server"
}
Else
{
	Write-Output "ERROR - FAILED TO LOAD PORT QRY EXECUTABLE @ PATH - $StrPortQryPath"
	Exit
}
#--
#-- BUILD EMPTY ARRAY TO STORE RETURNED PORTS:
$ArrayPorts = @()
$ArrayQryResult = Invoke-Expression $StrPortQryCmd
ForEach ($StrResult in $ArrayQryResult)
{
	If ($StrResult.Contains("ip_tcp"))
	{
		$ArraySplt = $StrResult.Split("[")
		$StrPort = $ArraySplt[1]
		$StrPort = $StrPort.Replace("]","")
		$ArrayPorts += $StrPort
	}
}
#--
#-- DUPLICAT PORTS & CHECK WORKFLOW:
$ArrayPorts = $ArrayPorts | Sort-Object |Select-Object -Unique
Check-Port -RPCServer $Server -ArrayRPCPorts $ArrayPorts
#--
#-- ********************************************************:
#--	END OF SCRIPT                                           :
#-- ********************************************************: