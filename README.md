# Backend for bachelor thesis
Does evaluation on images

## Important

**Change `GRISA` server in src/run_grisa.py, depending on your needs**

### Requirements
Install all requirements with `pip install -r requirements.txt`

### Local development
run `python3 app.py`

### API Endpoints
`/ping` [GET]
- test endpoint
- should get `pong`

`/get_images_from_url` [POST]
- get URL and scrape images from it


`/grisa/upload` [POST]
- should get URL to image or image file
- main entry point for backend that does the evaluation 

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


