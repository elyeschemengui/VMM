<h1>VMM ( Virtual Machine Manager)</h1>
<h2>Virtual Machine hosted on ESXI :</h2>

This python will help you to manage an ESXI and to manage the virtual machine hosted on it by giving you an SSH access and the possibility to execute a shell commands on it.

<h2> Requirement </h2>
PS : you need to install paramiko !!
<ul>
  <li> Command : pip install paramiko</li>
</ul>
<h2>Other usefull commands </h2>
<ul>
  <li> Status of a VM : vim-cmd vmsvc/power.getstate </li>
  <li> Power off a VM : vim-cmd vmsvc/power.off </li>
  <li> Power on a VM : vim-cmd vmsvc/power.on </li>
  <li> Reboot a VM : vim-cmd vmsvc/power.reboot </li>
  <li> Reset a VM : vim-cmd vmsvc/power.reset </li>
</ul>  
