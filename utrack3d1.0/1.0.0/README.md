# How to Run

This software has a GUI, which in Docker is a bit trickier to run than a simple CLI.  Below are our instructions based on [this site](https://cuneyt.aliustaoglu.biz/en/running-gui-applications-in-docker-on-windows-linux-mac-hosts/)

## Windows

Running this container on Windows requires PowerShell, and now WSL.  As a result, the container will not be able to see your file system natively.

### Third-Party Applications

Because Windows does not natively support X11 functionality, you will require a third-party program to launch the GUI.  As stated in the article above, we used [VcXsrv](https://sourceforge.net/projects/vcxsrv/), which required minimal setup to work in our environment.

If you are using the same program, once installed, launch XLaunch, and configure it as seen in the site:

![XLaunch settings](https://cuneyt.aliustaoglu.biz/en/content/images/2018/11/xlaunch.png)

, souced from the above site.  This program must be running, which it does in the background, for the GUI to work.

### File System

Since Windows is not a Unix-based system, the container will not be able to see the file system natively, like it can on Mac or Linux operating systems.  Therefore, you will need to add a mount flag to it, which we will show below.  One quirk is that, becuase Windows allows spaces in the directory names, we found it much simpler to save the directory we wanted as a variable to pass to Docker.

Example:

``` powershell
$imageDir="C:\Users\User Name\My Images"
```

### IP Address

You will also require your local IP address, which is easy enough to obtain with the `ipconfig` command.  As above, we would recommend saving this to a variable, so it does not show up in logs, but this is not as necessary.

### Run Command

Finally, we are ready to run the program.  Assuming you ahve set things up like above, the basic command to run it is:

``` powershell
docker run -ti --rm -v ${readFile}:/src/temp -e DISPLAY=${ipAddress}:0.0 bicf/utrack3d1.0:1.0.0 bash /execute/utrack3d/run_utrack3D.sh /opt/mcr/v98
```

## Mac OS

This is a bit simpler than Windows, however, still requires one piece of external software to function.

### xQuartz

As stated in the article, this can be installed either using the command line:

``` sh
brew cask install xQuartz
```

or by downloading the DMG file [here](https://www.xquartz.org/).  Once installed, you will need to open the settings, go to the 'Security' section, and ensure it is setup like this:

![xQuartz Settings](https://cuneyt.aliustaoglu.biz/en/content/images/2018/11/image-2.png)

As with VcXsrv, this program must be running in the background before you can launch the GUI.

### IP Address

Again, as with Windows, you will require your local IP Address, obtained with the command `ifconfig`.  Once you have that, you must add it to the xhost list:

``` sh
xhost + 192.168.X.X
```

As before, we would also recommend saving it into a varible to prevent it from being logged when you run the command.

### Run Command
Because Mac is a Unix-style OS, the image should be able to directly access your file system without further issue.  If you are having trouble, a setup similar to the Windows file system setup might be required.  Otherwise, the run command is very similar:

``` sh
docker run -ti --rm -e DISPLAY=${ipAddress}:0.0 bicf/utrack3d1.0:1.0.0 bash /execute/utrack3d/run_utrack3D.sh /opt/mcr/v98
```

## Linux

This is the container's native environment, so no other setup is really required for most distributions (we have tested specifically on CentOS and Ubuntu style distributions).

``` sh
docker run -ti --rm bicf/utrack3d1.0:1.0.0 bash /execute/utrack3d/run_utrack3D.sh /opt/mcr/v98
```
