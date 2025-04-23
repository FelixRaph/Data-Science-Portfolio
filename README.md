## Welcome to my Data Science Portfolio!

I have created this portfolio to store some of my data science projects, which reflect both my progress over the years and also my curiosity towards different topics, such as optimization methods, machine learning, statistics, and many more. I have started this journey with first online courses and an internship project at L'Oréal in 2023 and have been learning ever since. I am eager to add many more projects in the future, stay tuned!

In this read me file, you can explore the reasoning behind my projects and dive into some explanations and reflections that are meant to make my projects in code more accessible.

In case you have any questions and criticism, please contact me via email to felix-raphael@outlook.com .

Certificates & Online Courses: [Certificates](html_files/index.html)

Github repository: [Github](https://github.com/FelixRaph/Data-Science-Portfolio)

## Table of Contents

1. [Airbnb Project: Data Analysis using Python and SQL](#airbnb-project-data-analysis-using-python-and-sql)  
2. [Leveraging a ML classifier to detect a biomedical condition](#leveraging-a-ml-classifier-to-detect-a-biomedical-condition)  
3. [Hub and Spoke System with Gurobi Optimization using Python](#hub-and-spoke-system-with-gurobi-optimization-using-python)  
4. [Time Series Analysis - Predicting Walmart Sales](#time-series-analysis---predicting-walmart-sales)  
5. [Master Thesis: Optimizing Routes in Attended Home Services: Balancing Efficiency, Complexity, and Customer Service](#master-thesis-optimizing-routes-in-attended-home-services-balancing-efficiency-complexity-and-customer-service)





## Airbnb Project: Data Analysis using Python and SQL

Click here to read the report: [Airbnb Project Report](Airbnb%20Project/Project%20Report.pdf) \
Click here to see the SQL queries: [SQL queries](Airbnb%20Project/SQL%20queries.txt) \
Click here for the Python Cleaning Notebook: [Data Cleaning](Airbnb%20Project/Data%20Cleaning.ipynb) 

This project was part of my studies at RSM. The goal was to analyze and leverage publicly available Airbnb Data to draw insights and implications about Airbnb's impact on the respective city. 

For my analysis, I chose the city of Paris. I investigate 3 major research questions:

1. Which neighbourhoods display the highest listing density?
2. Professionalization \
         2.1 What is the distribution of the number of listings per host in Paris overall? \
         2.2 Which neighbourhoods are most popular among professional hosts? 
3. Host type characteristics \
         3.1 How do hosts of different types of professionalization set their prices? \
         3.2 How does professionalization relate to the type of listing? 

I based my research questions and assumptions on various sources from literature and articles. 

For data cleaning and data preparation, I used Python as a primary tool. Further database and table creation as well as subsequent analysis was done with SQL.

In the last section, I summarize my findings and evaluate them in the light of socio-economic aspects such as gentrification.

## Leveraging a ML Classifier to detect a Biomedical Condition

Click here to see the notebook:
[BioMed ML Model Notebook](html_files/BioMed_Case_ML_Model_hmtlfile.html)

In this project, I made use of a Kaggle dataset ( [Biomechanic Features of Orthopedic Patients](https://www.kaggle.com/datasets/uciml/biomechanical-features-of-orthopedic-patients) ) to build a Machine Learning Classification model. More particularly, I aimed to predict whether a patient has abnormal patterns, in which case they would suffer from either Disk Hernia or Spondylolisthesis. In this project, I did not differentiate between the two conditions and simply classified the subjects as abnormal for both.

To do so, I compared the performance of three different Machine Learning Models: KNN, Lasso and Random Forest.

The dataset consists of 310 observations, 210 of which are labeled "abnormal". After cleaning and exploring the data, I prepared dataframes as input to the models. Furthermore, I applied a 60/20/20 training/validation/test split to all models.

Due to the small sample size and class imbalances, keeping the same stratification of normal to abnormal labels was only possible to some extent throughout the different sets (training/validation/set).

As we work with class imbalances, it is useful to consider the True Positive and True Negative rates (TPR / TNR), as these metrics normalize by measuring the performance relative to the class size respectively.

The results show that Random Forest manages to strike a great balance between the performances metrices "Accuracy", "ROC_AUC", "Sensitivity" (TPR) and "Specificity" (TNR). For this project, Sensitivity seems to be an especially important metric, as it expresses how many abnormal patients we were able to identify correctly. Considering the priority of the TPR, we would then prefer KNN as a model, which also strikes a good metrics balance, but has the highest Sensitivity out of the three models, with 75.00%, compared to 70.83% for the Random Forest model.

As a consideration for future modeling approaches, it might be worthwile decreasing the threshold of the classifier. That way, the classifier would tend to overestimate abnormal patterns, which, given the context, would be preferrable to underestimating. For example, in the case of Random Forest, the model detected 34 out of 38 abnormal cases correctly. By lowering the threshold, the model would classify more easily as abnormal, decreasing the risk of misclassifying abnormal cases.


## Hub and Spoke System with Gurobi Optimization using Python

For this project, I tried to employ some of the methods used to tackle a group project of my Master's at RSM. In that, I used a dataset from Kaggle ( [Logitstics truck trips data](https://www.kaggle.com/datasets/ramakrishnanthiyagu/delivery-truck-trips-data) ) to have data on deliveries in India. I leveraged this data to then imagine the following case:

For all origin to destination routes in the dataset, I want to determine an optimal hub location that would reduce the travelled distances, as hubs, i.e. depots, often allow dispatching companies to pool orders together and to reduce distances in general. 

The results show that out of several potential hubs, the optimal hub location is located in the south-eastern part of India, in which a high concentration of shorter truck deliveries occur.

Click here to see the notebook:
[Hub and Spoke System with Gurobi Optimization using Python](html_files/Gurobi_Optimization_Model.html)


## Predicting Walmart Sales

In this project, I wanted to showcase my knowledge and experience taught during my Master's in Time Series Analysis and different Time Series Forecasting methods. 

Herefore, I analyzed a dataset of Walmart sales data for different stores over a time period of 2010-2021, i.e. around 2 years. This dataset had multiple other interesting features such as the Consumer Price Index (CPI) or the unemployement rate. Based on these features, it was imaginable to enhance the predictive models and boost their performance with exogenous variables.

The method was kept simple. This project was conducted as a simple, yet insightful, comparative analysis between:
         - Linear Regression
         - Holt Winters Exponential Smoothing
         - (S)ARIMA(X)

For the assessment of each model's performance a 80/20 train/test split was applied. In other words, the models were fitted on 80% of the data (in chronological order of the time series data) and their performance was then tested on the remaining 20%. The model performances were measured and compared by the RMSE and MAPE metrics. RMSE is a good choice due to its wide usage as a standard metric, its good interpretability and its sensitivity to large errors, thereby penalizing large deviations in predictions, which should be avoided. MAPE is a good choice because the metric it provides a intuitive understanding, is very useful in a business context and moreover is independent of different scales, which is particularly beneficial when there are varying dimensions in the data, i.e. here is the amount of sales.

One of the interesting insights gained from this is that adding exogenous variables to a model can quickly result in a overfitting or simply create misleading noise for the prediction model. 

You can find out which of the models performed best for predicting Walmart sales in this notebook:
[Predicting Walmart Store Sales](html_files/Time_Series_Forecasting.html)


## Master Thesis: Optimizing Routes in Attended Home Services: Balancing Efficiency, Complexity, and Customer Service

Executive Summary:
Companies operating in the sector of Attended Home Deliveries and -Services face the challenge
of planning efficient routes to deliver to their customers while maintaining high customer service
levels. Numerous companies such as the Dutch e-grocer Picnic already tackle this challenge by
leveraging extensively studied, sophisticated methods such as a priori optimization.
This thesis investigates how companies can balance planning complexity, route efficiency and
customer service levels by leveraging optimized appointment-day offerings and a priori routes to
minimize their total travel distance in delivery operations. For this, four different strategies are
explored in a comparative analysis on synthetic data from 2,500 delivery instances across three
Dutch provinces.
In a first stage, the strategies partition customers into groups, for each of which routes are
pre-planned and different appointment-day choices are assigned. After customer preferences are
incorporated, the strategies, in a second stage, finalize daily routes to visit each customer. This is
either done by adhering to the initial visiting order from the pre-planned routes or by reoptimizing
each daily route.
The study provides support for several findings from academic literature. Further, the results
highlight the importance of companies selecting the best grouping method in the first stage of
their strategy. In contrast, reoptimizing routes is found to only add a marginal improvement to the
efficiency of routes. Overall, the study demonstrates that optimizing appointment-day offerings can
yield substantial benefits to the efficiency of routes, thereby contributing to the overall profitability
of a company.

Find my thesis report [here](MasterThesis.html)

Find an excerpt of my code [here](MasterThesisCode_example.html)

If you are interested in this work, please feel free to reach out to me! I am happy to engage in a discussion.


