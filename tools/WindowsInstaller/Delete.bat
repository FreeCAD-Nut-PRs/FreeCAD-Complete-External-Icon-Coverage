@echo off
setlocal EnableExtensions

rem Hardened installer prune script for FreeCAD staged install tree
rem Intended to be run from the install root, e.g. %INSTALL_DIR%

cd /d "%~dp0"

echo [Delete.bat] Pruning staged install tree in "%CD%"

call :DeletePatternRecursive "*.pyc"
call :DeletePatternRecursive "*.pdb"
call :DeletePatternRecursive "*.obj"
call :DeletePatternRecursive "*.ilk"
call :DeletePatternRecursive "*.exp"
call :DeletePatternRecursive "*.lib"
call :DeletePatternRecursive "*.qmlc"
call :DeletePatternRecursive "*.jsc"

rem Remove common development-only executables and debug DLLs from bin
if exist "bin\" (
  pushd "bin"
  call :DeleteIfExists "assistant.exe"
  call :DeleteIfExists "designer.exe"
  call :DeleteIfExists "linguist.exe"
  call :DeleteIfExists "QtWebEngineProcessd.exe"

  call :DeleteIfExists "Qt5Cored.dll"
  call :DeleteIfExists "Qt5Guid.dll"
  call :DeleteIfExists "Qt5Networkd.dll"
  call :DeleteIfExists "Qt5OpenGLd.dll"
  call :DeleteIfExists "Qt5PrintSupportd.dll"
  call :DeleteIfExists "Qt5Qmld.dll"
  call :DeleteIfExists "Qt5QmlModelsd.dll"
  call :DeleteIfExists "Qt5Quickd.dll"
  call :DeleteIfExists "Qt5QuickControls2d.dll"
  call :DeleteIfExists "Qt5QuickTemplates2d.dll"
  call :DeleteIfExists "Qt5Scriptd.dll"
  call :DeleteIfExists "Qt5Sqld.dll"
  call :DeleteIfExists "Qt5Svgd.dll"
  call :DeleteIfExists "Qt5Testd.dll"
  call :DeleteIfExists "Qt5WebChanneld.dll"
  call :DeleteIfExists "Qt5WebEngineCored.dll"
  call :DeleteIfExists "Qt5WebEngineWidgetsd.dll"
  call :DeleteIfExists "Qt5Widgetsd.dll"
  call :DeleteIfExists "Qt5Xmld.dll"

  call :DeleteIfExists "Qt6Cored.dll"
  call :DeleteIfExists "Qt6Guid.dll"
  call :DeleteIfExists "Qt6Networkd.dll"
  call :DeleteIfExists "Qt6OpenGLd.dll"
  call :DeleteIfExists "Qt6OpenGLWidgetsd.dll"
  call :DeleteIfExists "Qt6PrintSupportd.dll"
  call :DeleteIfExists "Qt6Qmld.dll"
  call :DeleteIfExists "Qt6QmlModelsd.dll"
  call :DeleteIfExists "Qt6Quickd.dll"
  call :DeleteIfExists "Qt6QuickControls2d.dll"
  call :DeleteIfExists "Qt6QuickTemplates2d.dll"
  call :DeleteIfExists "Qt6Svgd.dll"
  call :DeleteIfExists "Qt6SvgWidgetsd.dll"
  call :DeleteIfExists "Qt6Testd.dll"
  call :DeleteIfExists "Qt6WebChanneld.dll"
  call :DeleteIfExists "Qt6WebEngineCored.dll"
  call :DeleteIfExists "Qt6WebEngineQuickd.dll"
  call :DeleteIfExists "Qt6WebEngineWidgetsd.dll"
  call :DeleteIfExists "Qt6Widgetsd.dll"
  call :DeleteIfExists "Qt6Xmld.dll"
  popd
) else (
  echo [Delete.bat] NOTE: "bin" folder not found, skipping bin-specific cleanup.
)

rem Trim optional PySide6 QML content when present
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick\LocalStorage"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick\Timeline"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick\Tooling"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick\Effects"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick\ParticleSystem"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick3D\Helpers"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick3D\Assets"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick3D\Effects"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick3D\Helpers\impl"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick\Controls\Imagine"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick\Controls\Material"
call :RemoveDirIfExists "Lib\site-packages\PySide6\qml\QtQuick\Controls\Universal"

rem Legacy path variants sometimes appear depending on build layout
call :RemoveDirIfExists "lib\site-packages\PySide6\qml\QtQuick\LocalStorage"
call :RemoveDirIfExists "lib\site-packages\PySide6\qml\QtQuick\Timeline"
call :RemoveDirIfExists "lib\site-packages\PySide6\qml\QtQuick\Tooling"
call :RemoveDirIfExists "lib\site-packages\PySide6\qml\QtQuick3D\Assets"
call :RemoveDirIfExists "lib\site-packages\PySide6\qml\QtQuick3D\Effects"

echo [Delete.bat] Done.
exit /b 0

:DeletePatternRecursive
set "PATTERN=%~1"
for /r %%F in (%PATTERN%) do (
  if exist "%%~fF" del /f /q "%%~fF" >nul 2>nul
)
exit /b 0

:DeleteIfExists
if exist "%~1" (
  del /f /q "%~1" >nul 2>nul
)
exit /b 0

:RemoveDirIfExists
if exist "%~1\" (
  rmdir /s /q "%~1" >nul 2>nul
)
exit /b 0
