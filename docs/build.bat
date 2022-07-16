:: Remove Previous Build Remnants
rmdir /s /q _build
rmdir /s /q ..\html

:: Build the html
sphinx-build -M html "." "_build"

:: Move the html
Xcopy .\_build\html ..\html /E /H /C /I
rmdir /s /q ..\html\_sources