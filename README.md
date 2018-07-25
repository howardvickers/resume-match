# [no-code-ml.com](http://no-code-ml.com)
### Project Introduction
This is a personal project to create a web app that allows someone with no coding experience to run machine learning algorithms on business data.

Machine Learning and Data Science present two main barriers to entry:
* Coding skills (eg python, R, etc)
* Theoretical background (eg statistics, math etc)

This web app explores how the first barrier can be overcome with a point-n-click interface to use machine learning techniques that normally require good knowledge of python, pandas, numpy and similar programming skills.

The second barrier could be addressed with step-by-step guidance and training; this is considered beyond the immediate scope of this project.

Note that the web app is intended as a conceptual project rather than a commercial product. It aims to showcase the programmer's combined skillset of data science and web dev.

### Business Context
This project is guided by a sense of a hyperthetical, yet practical business situation: a startup has sales or other data that is available as a csv file and wishes to gain insights into the data; perhaps a desire to predict future sales and to understand where to employ resources for the best performance.  

### Functionality  
The web app offers the following functionality:
* upload csv files
* view initial rows (equivalent to df.head() in pandas)
* change column names
* select columns for regression analysis
* select columns using jquery (without page refresh)
* compare regressions with different tools (linear, random forest, etc)
* demo mode

### Future Functionality
* save resulting datasets and regression analyses
* manually delete all saved files at end of session
* algorithm tuning: hyperperameters adjusted (via dropdowns/checkboxes) to optimzie models
* predictive analysis: upload unlabeled data and predict dependent variable
* missing data (NaN) handling
* multiple header handling

### Structure
* [app.py](https://github.com/howardvickers/no-code-ml/blob/master/src/app.py) is the server.  
* [index.html](https://github.com/howardvickers/no-code-ml/blob/master/src/templates/index.html) is the initial html page (includes upload function).  
* [ml.html](https://github.com/howardvickers/no-code-ml/blob/master/src/templates/ml.html) is the machine learning html page (main interface).  
* [regressions.py](https://github.com/howardvickers/no-code-ml/blob/master/src/regressions.py) runs regressions according to selected models and returns RMSE and R-Squared stats.   
* [ols_summary.py](https://github.com/howardvickers/no-code-ml/blob/master/src/ols_summary.py) runs initial linear regression and initial random forest to generate coefficients, p-values and feature importances (to assist with feature/variable selection).   
* [global_y.py](https://github.com/howardvickers/no-code-ml/blob/master/src/global_y.py) holds the y variable (for app.py).   

### Technologies Employed
* python
* numpy
* pandas
* flask
* jinja
* javascript
* jquery
* ajax
* bootstrap
* html
* css
# resume-match
