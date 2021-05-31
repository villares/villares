# -*- coding: UTF-8 -*-

# From https://github.com/villares/villares/blob/main/s/ubuntu_jogl_fix.py

from java.lang import System 
System.setProperty("jogl.disable.openglcore", "false") 
