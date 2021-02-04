# Gartico

A gartic clone made with flask + socketio

## Installing modules

Using Python 3.x :

```
$ pip install .
```

## Docker

### Installation

Follow these installation [steps](https://docs.docker.com/engine/install/) on Docker documentation.

If you are an arch-user:

```
# pacman -S docker
```

Do not forget to start docker daemon:

```
# systemctl start docker
```

And install the mysql image:

```
# docker pull mysql
```

### Starting container

```
# docker run --name <container_name> -e MYSQL_ROOT_PASSWORD=<db_password> -p <port>:3306 -d mysql
```

## Windows init

```
set FLASK_APP=server

flask run
```

## Linux/Mac init

```
$ export FLASK_APP=server

$ flask run
```
