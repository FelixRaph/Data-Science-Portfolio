## Welcome to my Data Science Portfolio!

In this read me file, you can explore the reasoning behind my projects and dive into some explanations and reflections that are meant to make my code more accessible. Enjoy!

In case you have any questions and criticism, please contact me via email to felix-raphael@outlook.com .


## Table of Contents

1. [Disclaimer](##Disclaimer)
2. [Airbnb Project: Data Analysis using Python & SQL](#airbnb-project)
3. [Leveraging a ML classifier to detect a biomedical condition](#leveraging-a-ml-classifier-to-detect-a-biomedical-condition)
4. [Hub and Spoke System with Gurobi Optimization using Python](#hub-and-spoke-system-with-gurobi-optimization-using-python)


## Disclaimer

The contents in this Portfolio should be embedded and read within a context, which I will elaborate on in the following.

I am currently finishing my Master's degree in Business Analytics & Management at Rotterdam School of Management. As I have a background in Business, I still consider myself at the beginning of my journey in the field of Data Science. Hence, my projects uploaded here do not aim to be overly complex, but reflect my interest and eagerness to learn and practice on rather simple use cases. 

During my academic journey, I found the fields of Machine Learning and Operations Research to be particularly interesting. Apart from that, I will try to incorporate simple Data Analysis and Visualization projects as well on this repository.


## Airbnb Project


## Leveraging a ML Classifier to detect a Biomedical Condition

Click here to see the notebook:
[BioMed ML Model Notebook](html_files/BioMed_Case_ML_Model_hmtlfile.html)

In this project, I made use of a Kaggle dataset ( [Biomechanic Features of Orthopedic Patients](https://www.kaggle.com/datasets/uciml/biomechanical-features-of-orthopedic-patients) ) to build a Machine Learning Classification model. More particularly, I aimed to predict whether a patient has abnormal patterns, in which case they would suffer from either Disk Hernia or Spondylolisthesis. In this project, I did not differentiate between the two conditions and simply classified the subjects as abnormal for both.

To do so, I compared the performance of three different Machine Learning Models: KNN, Lasso and Random Forest.

The dataset consists of 310 observations, 210 of which are labeled "abnormal". After cleaning and exploring the data, I prepared dataframes as input to the models. Furthermore, I applied a 60/20/20 training/validation/test split to all models.

Due to the small sample size and class imbalances, keeping the same stratification of normal to abnormal labels was only possible to some extent throughout the different sets (training/validation/set).

As we work with class imbalances, it is useful to consider the True Positive and True Negative rates (TPR / TNR), as these metrics normalize by measuring the performance relative to the class size respectively.

The results show that Random Forest manages to strike a great balance between the performances metrices "Accuracy", "ROC_AUC", "Sensitivity" (TPR) and "Specificity" (TNR). For this project, Sensitivity seems to be an especially important metric, as it expresses how many abnormal patients we were able to identify correctly. Considering the priority of the TPR, we would then prefer KNN as a model, which also strikes a good metrics balance, but has the highest Sensitivity out of the three models, with 75.00%, compared to 70.83% for the Random Forest model.


## Hub and Spoke System with Gurobi Optimization using Python
