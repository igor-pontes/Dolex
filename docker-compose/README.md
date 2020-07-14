# Use this project right now with docker!
If you are interested and want to see if this works, I GOTCHA!
## Prerequisites
 - Docker - See how to download & install it right [here](https://docs.docker.com/docker-for-windows/install/).
## How to install
 1. Create a folder
```
    mkdir dolex/
```
2. Open it
```
    cd dolex/
```
3. Download the **dolexdocker.tar.gz** file
```
    wget https://github.com/igor-pontes/Dolex/raw/master/docker-compose/dolexdocker.tar.gz
```
4. Extract the compressed file.
```
    tar -xf dolexdocker.tar.gz
```
5. Remove it so we don't pack this folder with a bunch of useless files.
```
    rm dolexdocker.tar.gz
```
6. From now on it becomes so easy you won't even imagine. Just run this command line and we're done! THAT'S IT.
```
    docker-compose -f "docker-compose.yml" up -d --build 
```
7. Now relax and wait till this process is finished :D
