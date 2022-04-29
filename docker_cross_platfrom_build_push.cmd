@ECHO OFF
IF "%1" == "" (
    echo "Version parameter is mandatory!"
    goto :exit
)
echo [%1]|findstr /i /r "[v][.][0-9][.][0-9].[0-9]" > nul
IF "%errorlevel%" == "1" (
    echo "Version %1 is not in v.X.X.X format!"
    goto :exit
)

echo "Creating docker images version %1...."
docker buildx create --name miproxybuilder
docker buildx use miproxybuilder

@ECHO ON
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t skser/miproxytranslator:%1 --push .
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t skser/miproxytranslator:latest --push .
exit /B 0

:exit
echo "Usage: docker_cross_platfrom_build_push.cmd v.X.X.X"
exit /B 1