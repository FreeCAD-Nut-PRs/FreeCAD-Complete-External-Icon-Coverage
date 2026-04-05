/*

install.nsh

Installation of program files, dictionaries and external components

*/

#--------------------------------
# Program files

Section -ProgramFiles SecProgramFiles

  # if the $INSTDIR does not contain "FreeCAD" we must add a subfolder to avoid that FreeCAD will e.g.
  # be installed directly to C:\programs - the uninstaller will then delete the whole
  # C:\programs directory
  StrCpy $String $INSTDIR
  StrCpy $Search ${APP_NAME}
  Call StrPoint # function from Utils.nsh
  ${if} $Pointer == "-1"
   StrCpy $INSTDIR "$INSTDIR\${APP_DIR}"
  ${endif}
  
  # turn on logging
  # Note that this can first be done here since the log file is written to $INSTDIR
  # to $INSTDIR must have a valid path before logging can be turned on
  ; LogSet on  ; disabled because the installed NSIS build does not define NSIS_CONFIG_LOG

  # Install and register the core FreeCAD files
  
  # Initializes the plug-ins dir ($PLUGINSDIR) if not already initialized.
  # $PLUGINSDIR is automatically deleted when the installer exits.
  InitPluginsDir
  
  # Binaries
  SetOutPath "$INSTDIR\bin"
  # recursively copy all files under bin
  File /r "${FILES_FREECAD}\bin\*.*"
  
  # MSVC redistributable DLLs
  IfFileExists "${FILES_DEPS}\*.*" 0 +3
    SetOutPath "$INSTDIR\bin"
    File "${FILES_DEPS}\*.*"
  
  # Others
  IfFileExists "${FILES_FREECAD}\data\*.*" 0 +3
    SetOutPath "$INSTDIR\data"
    File /r "${FILES_FREECAD}\data\*.*"

  IfFileExists "${FILES_FREECAD}\doc\*.*" 0 +3
    SetOutPath "$INSTDIR\doc"
    File /r "${FILES_FREECAD}\doc\*.*"

  IfFileExists "${FILES_FREECAD}\Ext\*.*" 0 +3
    SetOutPath "$INSTDIR\Ext"
    File /r "${FILES_FREECAD}\Ext\*.*"

  IfFileExists "${FILES_FREECAD}\lib\*.*" 0 +3
    SetOutPath "$INSTDIR\lib"
    File /r /x *.obj /x *.pdb /x *.ilk /x *.exp /x *.lib /x *RelWithDebInfo* /x *Downloader* /x *qml\Assets* "${FILES_FREECAD}\lib\*.*"

  IfFileExists "${FILES_FREECAD}\Mod\*.*" 0 +3
    SetOutPath "$INSTDIR\Mod"
    File /r "${FILES_FREECAD}\Mod\*.*"

  IfFileExists "${FILES_FREECAD}\resources\*.*" 0 +3
    SetOutPath "$INSTDIR\resources"
    File /r "${FILES_FREECAD}\resources\*.*"

  IfFileExists "${FILES_FREECAD}\translations\*.*" 0 +3
    SetOutPath "$INSTDIR\translations"
    File /r "${FILES_FREECAD}\translations\*.*"

  SetOutPath "$INSTDIR"
  ; File /r "${FILES_THUMBS}"  ; disabled because thumbnail source path is missing in this installer setup
    
  # Create uninstaller
  WriteUninstaller "$INSTDIR\${SETUP_UNINSTALLER}"

SectionEnd
