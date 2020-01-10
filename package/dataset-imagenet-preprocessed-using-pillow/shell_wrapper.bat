rem
rem CK wrapper for preprocessing the ImageNet dataset using Pillow.
rem
rem See CK LICENSE.txt for licensing details.
rem rem See CK COPYRIGHT.txt for copyright details.
rem rem
rem rem Developer(s):
rem rem - Anton Lokhmotov, anton@dividiti.com, 2020
rem

echo Preprocessing ImageNet using Pillow ...

"%CK_ENV_COMPILER_PYTHON_FILE%" "%PACKAGE_DIR%/preprocess_image_dataset.py" "%CK_ENV_DATASET_IMAGENET_VAL%" "%INSTALL_DIR%"

if %errorlevel% neq 0 (
  echo.
  echo Error: Failed preprocessing ImageNet using Pillow ...
  goto err
)

exit /b 0

:err
exit /b 1
