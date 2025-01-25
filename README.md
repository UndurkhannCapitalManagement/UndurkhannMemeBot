# RandomMemeBot

## Description

A bot that gives random Bobo meme

Also:

 * How to use [GitHub Actions](https://github.com/features/actions)


## Requirements

 * `Python 3.11`
 * `Pip`


## Installation


```sh
$ pip install -r requirements.txt
```

## Configuration

Create .env file under the application home folder

```
API_TOKEN={Your Telegram Bot API TOKEN}
```

## Running tests (TODO)

Run:

```sh
$ python -m unittest discover
```

## Running the application

### Install Dependencies

```sh
$ pip install -r requirements-server.txt
```


## Running on Docker

Run:

```
$ docker build -t memebot:latest .
$ docker run -d  memebot:latest
```
