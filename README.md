# Potoo

## What is it ?
[Potoo](https://en.wikipedia.org/wiki/Potoo) is a special bird that communicates with VoIP ecosystem and particularly well with Wazo.

The main objective of this project is to quickly (and perhaps badly) provide solutions to missing functionalities in a given ecosystem.

Its best documentation is its source code but some example could be found bellow.

Potoo may be verry insecure use it at your own risk !

## Install potoo on Wazo engine
1. `apt install -y wazo-plugind-cli`
2. `wazo-plugind-cli -c 'install git https://github.com/benasse/potoo'`

## Some interfaces

### Visualise queue from asterisk cli
```
http://myhost:8001/queue?queue=myqueue
http://myhost:8001/queue_pretty?queue=myqueue # less information for less technical people
http://myhost:8001/queue
```
### Originate a call with a GET http
```
http://myhost:8001/originate/v1?dest_exten=1234&dest_context=my-dest-context&src_exten=777&src_context=my-src-context
http://myhost:8001/originate/v1?dest_exten=1234
```
### Sample url
```
http://myhost:8001/hello_ansible # lanch a example playbook
http://myhost:8001/hello_ansible_form # lanch a exampe playbook loading variable from a form
```
### Update system informations
```
http://myhost:8001/update_system_info # form that permit to change system informations that are not availiable on admin interfaces
```
## Setup developement environement
1. `apt-get install python3-venv`
2. `git clone https://github.com/benasse/potoo.git`
3. `cd potoo`
4. `python3 -m venv potoo/venv`
5. `source potoo/venv/bin/activate`
6. `pip install -r requirements.txt`
7. `python app.py`

## Unstall potoo on Wazo engine
`wazo-plugind-cli -c 'uninstall sparrow/potoo'`
