# JT-VAE

## How to run
Switch to python 2.7 environment (mentioned in `guide.txt`)
### Local server Flask server
As fastapi supports python3, we have choosen flask 
```
    > cd ./model
    > python app.py 
```
will run on port 5000

### Pytest
```
    > cd model/pytests
    > pytest
```
### Streamlit frontend
```
    > streamlit run frontend.py
```
### Docker for FastAPI server
```
    > ./docker.sh
```

READMEs are mentioned in respective directories.

pylint score is less as there are less formatters supporting for python 2.7 </br>
Change in pylint score after modification is 7 on average </br>
Current pylint score is around 5 averaging over all files. </br>

## File structure
```
.
├── Dockerfile
├── Readme.md
├── guide.txt
|---Model
│   ├── app.py  --> Backend
│   ├── bo --> Bayesian Optimisation 
│   ├── molvae --> sampling and reconstruction 
│   ├── molopt --> molecular optimization
│   ├── data --> zinc and moses dataset
│   ├── pytests
│   ├── fastmolvae --> cuda support for sampling
│   ├── fastjtnn --> support files with cuda support
│   └── jtnn --> support files for junction tree etc
├── Frontend.py  -> Frontend file
