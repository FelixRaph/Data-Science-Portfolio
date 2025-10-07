<!-- Header section with background and profile image -->
<div style="position: relative; height: 280px; background-image: url('html_files/ML_wallpaper.jpg'); background-size: cover; border-radius: 12px; margin-bottom: 20px;">

  <div style="position: absolute; bottom: -50px; left: 20px;">
    <img src="html_files/20250410_105955000_iOS.png" alt="Profile Image" width="75" height="100" style="border-radius: 50%; border: 4px solid white; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
  </div>
</div>

<br><br>

# **Welcome to My Data Science Portfolio!** 🎉

Welcome! This is where I showcase my **data science journey**, documenting projects that highlight my growth and curiosity in diverse fields like optimization methods, machine learning, statistics, and more. My adventure started in 2023 with online courses, an internship project at **L'Oréal**, and an Analytics Master's degree at Erasmus University Rotterdam. I've been learning and evolving ever since!

In this portfolio, you'll find a curated selection of my projects, with explanations of my approach, key insights, and reflections. Whether you're here for inspiration, feedback, or collaboration, I hope you find these projects insightful. 

💌 **Feel free to reach out** with any questions or feedback via email: [felix-raphael@outlook.com](mailto:felix-raphael@outlook.com).

### 🌟 **Certificates & Online Courses**:
[Explore my Certifications](html_files/index.html)

### 📂 **Github Repository**:  
[Check out my GitHub](https://github.com/FelixRaph/Data-Science-Portfolio)

---

## 📑 **Table of Contents**

1. [A/B Testing: Does a New Website Feature Affect Customer Behavior](#-ab-testing-does-a-new-website-feature-affect-customer-behavior)
2. [Udemy: 100 Days of Code: The Complete Python Pro Bootcamp](#-udemy-100-days-of-code-the-complete-python-pro-bootcamp)
3. [What Drives Hotel Popularity on TripAdvisor? A Causal Discovery Project](#-what-drives-hotel-popularity-on-tripadvisor-a-causal-discovery-project)
4. [Master Thesis: Optimizing Routes in Attended Home Services](#-master-thesis-optimizing-routes-in-attended-home-services)
5. [Predicting Walmart Sales with Time Series Analysis](#-predicting-walmart-sales-with-time-series-analysis)
6. [Hub and Spoke System with Gurobi Optimization using Python](#-hub-and-spoke-system-with-gurobi-optimization-using-python)
7. [Leveraging a ML Classifier to detect a Biomedical condition](#-leveraging-a-ml-classifier-to-detect-a-biomedical-condition)
8. [Airbnb Project: Data Analysis using Python and SQL](#%EF%B8%8F-airbnb-project-data-analysis-using-python-and-sql)

---

## **From Data to Harvest: Smart Solutions for Farming Challenges**

I started this project for several reasons. On the one hand, I had read something about use cases of data science in farming, and I was fascinated by the practical side of the solutions, and by the deep purpose it serves. Applications of data science in farming do not only make the lives of farmers easier, but also, by extension, helps secure the livelihood of us as a society. 
On the other hand, I was also for longer already curious about building pipelines and working with an orchastration engine. In this case, I decided to work with Airflow because of its popularity and ease of implementation.

Enhancing farming by data science applications offers a wide range of opportunities. The main areas it can improve, in my opinion, revolve around enhanced planning capabilities, yield optimization, risk mitigation (environmental events), and profitability improvement.

Here is what I did:

The idea was to build a simple overview as a dashboard for a farmer to use for his field. In this overview, the farmer could look at historical and forecasted data for weather and soil conditions. This is meant to be a very simplified MVP. However, this dashboard already offers the opportunity to have a cockpit which gives you insight on what's coming, and whether there is for instance a risk for drought or frost, which would prompt a farmer to take protective measures, to ensure his crops are not endangered.

In practice, here is what this simple MVP solution looks like for my example:

<img src="html_files/Dashboard image.png" width="400">

Now to how this dashboard was generated.

It all starts in the setup of the DAG (or pipeline) with Python and Airflow. In the Graph below, you can find this DAG which consists of different elements. I first created two empty tables in a postgres database, which are supposed to accomodate historical and forecasted data. Then, as a next step, the std_agri_flow pulls two different datasets from APIs, which are then processed and finally merged to a daily, historical, dataset of the previous 7 days. In parallel, another forecasted flow takes place, for which no processing is needed. I here simply pull data from a forecast API and export it to my table in the database. At the same time, the combined historical dataset is also exported to the respective table in my database.
This pipeline can be scheduled in different ways. Most sense would make either a daily or a weekly frequency, depending on how often the farmer requires information, or on which precision level.
From here, I can check whether the entries have been pushed successfully in my postgres database.

Last, I have created a connection to the dashboard shown above



## 🧪 **A/B Testing: Does a New Website Feature Affect Customer Behavior?**

[Explore the full notebook here](html_files/AB_Testing.html)

In this project, I explored the impact of a **new website feature** rolled out by an online shopping platform through a controlled **A/B experiment**. Visitors were randomly assigned to one of two groups:  
- The **treatment group**, which interacted with the **updated website** containing the new feature  
- The **control group**, which continued to see the **standard version** without any changes

🔍 **Exploratory Analysis**  
I began with an **exploratory data analysis** to investigate potential differences between the two groups. Using **visualizations**, summary statistics, and a **correlation matrix**, I uncovered early signs that the treatment might be influencing user behavior. For instance:
- The new feature seemed to **moderate the relationship between spending and search activity**
- There were **small but positive shifts** in **conversion-related metrics**

📊 **Statistical Hypothesis Testing**  
To go beyond observation and assess whether these patterns were **statistically significant**, I performed **hypothesis testing** on key performance indicators (KPIs). This allowed me to distinguish between **real treatment effects** and random noise.

✅ **Key Finding:**  
The **completion rate** — the proportion of items added to cart that were ultimately purchased — was **significantly higher** in the treatment group, providing strong evidence that the new feature improved this aspect of the customer journey.

❌ **No Significant Effects Found:**  
- **Conversion rate** (searches → purchases)  
- **Total number of purchases**

These results indicate that while the feature may not drive more overall purchases, it can help **improve follow-through** once users have shown interest in products.

This project highlights my ability to combine **exploratory analysis**, **data visualization**, and **robust statistical testing** to evaluate the real-world impact of product changes in an experimental setting.


## 🎓 **Udemy: 100 Days of Code: The Complete Python Pro Bootcamp**

Currently working through the 100 Days of Code Python course on Udemy, learning through daily coding projects and challenges.

### Example Projects:
- Simple games (Snake, Pong, Blackjack)
- Web scraping and automation scripts
- Basic Flask web applications
- Data analysis with Pandas
- GUI applications with Tkinter

### Learning Focus:
- Python fundamentals and OOP
- Web development basics (HTML, CSS, Flask)
- Working with APIs and databases
- Data manipulation and visualization
- Automation and scripting

Building practical coding skills one day at a time!

Check out the course here: [Course details on udemy](https://www.udemy.com/course/100-days-of-code/?couponCode=PLOYALTY0923)

Follow some of the projects I am building along the way in [this notebook](html_files/100DaysofCode_Projects.html)

---

## 🏨 **What Drives Hotel Popularity on TripAdvisor? A Causal Discovery Project**

🔗 [Explore the full Jupyter Notebook](html_files/TripAdvisor_CausalDiscovery_Notebook.html) 

This project explores what makes hotels in Rome more popular on TripAdvisor, using a dataset of **4,599 hotels** and **272 features** including amenities, image counts, and web traffic data. Popularity is measured by the number of clicks each hotel receives.

💡 Project Goals:
- Identify the most important hotel features associated with high user engagement (views on trip advisor).
- Attempt to quantify the causal relationship between the most important user engagement features 

🔧 Tools & Libraries:
`pandas`, `scikit-learn`, `XGBoost`, `matplotlib`, `seaborn`, `DirectLiNGAM`, `imblearn`

🧠 Methodology:
- **Data Preparation**: Cleaned the data, identified and removed outliers, handled missing values, removed redundant or flawed columns and handled severe class imbalance by randomly over- and undersampling in preparation of applying ML Classifiers.
- **Feature Selection**: Trained ensemble models (Random Forest, XGBoost) and used **feature importance** to reduce dimensionality and highlight key drivers of engagement.
- **Causal Discovery**: Applied the **DirectLiNGAM** algorithm to uncover and quantify possible cause-effect relationships between selected features and views.

✅ Key Takeaways:
- Photos strongly impact the number of reviews, with an effect of 0.877.
- The number of reviews has a moderate, direct effect onto the binary target variable `views`, with a causal effect of 0.459.
- Photos have a very weak effect on views and on the adjusted score given.

This project reflects my growing interest in **interpretable machine learning**, and it helped me learn how to move from **correlation to causation** using real-world data. While this is a beginner's step into the challenging domain of Causal Inference, it shows how Machine Learning and Causal Discovery/Inference can be used hand in hand, in order to untangle large amounts of data into a simple overview of causal relationships. 

---

## 🎓 **Master Thesis: Optimizing Routes in Attended Home Services** 

🔗 [Read the full Master Thesis](html_files/MasterThesis.html)  
🔗 [Explore the Solution Code](html_files/Solution_Code_stage2_final.py)

My **Master’s thesis** focused on improving route optimization for **attended home deliveries and services**. Companies like **Picnic** already use sophisticated **a priori optimization** methods to plan efficient delivery routes. 

In my study, I explored strategies to balance **efficiency**, **complexity**, and **customer service**. After partitioning customers into groups and assigning appointment days, I optimized daily delivery routes to minimize travel distance. The study found that optimizing **appointment-day offerings** had significant impacts on route efficiency and profitability.

---

## 📈 **Predicting Walmart Sales with Time Series Analysis** 

🔗 [View the Time Series Forecasting Notebook](html_files/Time_Series_Forecasting.html)

In this project, I used **Walmart sales data** from 2010-2021 to explore various **time series forecasting** methods. I compared:

- **Linear Regression**
- **Holt Winters Exponential Smoothing**
- **(S)ARIMA(X)**

I employed **exogenous variables** (like CPI and unemployment rate) to see if they improved predictive accuracy. Results showed that while these variables may boost performance, they can also lead to **overfitting** if not handled carefully.

Performance was measured using **RMSE** and **MAPE**, providing actionable insights into sales forecasting.

---

## 🚚 **Hub and Spoke System with Gurobi Optimization using Python** 

🔗 [Check out the notebook](html_files/Gurobi_Optimization_Model.html)

For this project, I worked on optimizing **delivery routes** using a **Hub and Spoke** system. By applying optimization techniques with the **Gurobi** solver, I identified the most efficient hub location for deliveries across India, minimizing travel distance and improving logistics. 

The dataset provided insights into **delivery patterns**, helping me propose the optimal location for a logistics hub in India, located in the **south-eastern region**, where shorter deliveries are more frequent.

---

## 🧬 **Leveraging a ML Classifier to detect a Biomedical condition** 

🔗 [Explore the ML Model Notebook](html_files/BioMed_Case_ML_Model_hmtlfile.html)

In this project, I used a **Kaggle dataset** to predict whether a patient has abnormal biomechanical patterns indicative of conditions like **Disk Hernia** or **Spondylolisthesis**. I compared three ML models: **KNN**, **Lasso**, and **Random Forest**.

I dealt with small sample sizes and class imbalances, and evaluated each model based on key performance metrics like **Sensitivity (True Positive Rate)** and **Specificity (True Negative Rate)**. Ultimately, the **Random Forest** performed best in identifying abnormal patients with a **89.47% Sensitivity**, meaning that the model was able to detect almost 9 out of 10 patients with abnormal patterns!

---

## 🏙️ **Airbnb Project: Data Analysis using Python and SQL** 

🔗 [Read the full report](Airbnb%20Project/Project%20Report.pdf)  
🔗 [Explore the SQL Queries](Airbnb%20Project/SQL%20queries.txt)  
🔗 [View the Python Data Cleaning Notebook](Airbnb%20Project/Data%20Cleaning.ipynb)

As part of my studies at **RSM**, I tackled a comprehensive analysis of Airbnb data to explore its impact on the city of Paris. The focus was on:

1. **Neighbourhood Listing Density**: Identifying areas with the most listings.
2. **Host Professionalization**: Understanding the relationship between host type and pricing.
3. **Host Type Characteristics**: Investigating how different host types influence the pricing strategies and listing types.

I used Python for data cleaning and preparation, then transitioned to SQL for database management and further analysis. My findings highlight important socio-economic considerations, including the impact of gentrification.

---

I hope you enjoy exploring these projects and insights! Stay tuned for more exciting additions in the future. 🚀
