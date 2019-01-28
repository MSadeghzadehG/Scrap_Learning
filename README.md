# uni_portal_scraper
python scraper on portal of Amirkabir University of Technology to automating course selection procedure.
### How to use?
1. Download requirements using requirements.txt => `pip install -r requirements.txt`
1. Enter your username and password in `portal_scraper.py` **or** create `account.txt` in the main directory and put your username and password in the first line in this order : `username,password` 
1. find your course code with inspecting portal website **or** use following pattern to set code: `CodeOfCourse_CodeOfGroup__` like `3102013_1__`
1. set a plan like `plan1` inside `portal_scraper.py` **or** create `plan1.txt` in the main directory and put your `CodeOfCourse_CodeOfGroup__,PreferredName` in each line like this : `3102013_1__,riazi1`
1. run the `portal_scraper.py` and enjoy! :)
### Description
##### get_captcha.py
used for collecting images and set their labels to create a dataset of labeled captchas.
##### process_captcha.py
used for pre-processing on dataset images and binarizing them.
##### portal_scraper.py
to scrap portal website and choose courses by plan.
##### model.h5
the weights of traind CNN for bypassing captcha.
##### model.json
the structure of tranind CNN for bypassing captcha.
