# Backend for bachelor thesis
Backend for web appliaction, which evaluates advertisemets, and finds fraudulent ones.
Returns back **report**.


## Important
**Change `GRISA` server in src/run_grisa.py, depending on your needs**

### Local development
create virtual enviroment with `python3 -m venv venv`
Activate it with `. venv/bin/activate`
Install all requirements with `pip install -r requirements.txt`
run `python3 app.py`

To deactivate type `deactivate`

### API Endpoints
`/ping` [GET]
- test endpoint
- should get `pong`

`/get_images_from_url` [POST]
- get URL and scrape images from it


`/grisa/upload` [POST]
- should get URL to image or image file
- main entry point for backend that does the evaluation 

`/grisa/set/country` [POST]
- Recive country/countries and report
- do evaluation and send report back

### Hosting
- Hosted on Heroku
- URL: `https://bt-backend-18d86ef18244.herokuapp.com/`
- `runtime.txt` has the required python version


#### Heroku plugins
```
heroku-builds 0.0.29
heroku-fork 4.1.29
heroku-repo 1.0.14
```
#### Heroku Buildpacks
```
1. https://github.com/heroku/heroku-buildpack-apt
2.  heroku/python
```


