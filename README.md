# EC530_pro2
Osama
Yongxin Jiang

                                        Project 2: 
Step 1:
What should api do in machine learning, especially in upload data and training:
1.Safety test: ensure that only authorized users can access the API. Maybe use password and username or face id.

2. Create a project: allow users to create a new machine learning project for image classification or object detection.
3. Permission:ensure that each project is associated with a specific user to manage and access control. Maybe only one person( like privacy),or a number of people.

4. Data Management: provide endpoints for users to upload images and corresponding labels or class data for training.Like analyze data which is Implement functionalities to analyze the uploaded data before training, such as data exploration and visualization. And also allow users to add or remove data points from the training dataset as needed.

5. Training Configuration parameters: enable users to specify training parameters such as size, learning rate.

6.Training run and track iterations management: provide training stats upon completion, including metrics like loss, accuracy, etc.

7.Testing and Evaluation: allow users to test a trained model using a new dataset and retrieve evaluation results. Maybe several times of testing is allowed.


Step 2:
The goal is to create the database schema for the project that I  choose which is about image.But I don’t have to create the database yet, just define what data I am interested in and how they are related and datatypes.

1. So I installed flask and everything related to flask.
   
2. Then, I generated a new app.py about image classification base on the old app.py by using flask.
 
3. Then, I used the new app.py generated the database scheme for image classfication aspect.
 
4. Then I created a log file for this step.

Step 3:
1. I built a queue to process inference requests and built a queue to process training requests.
2. I integrated them into your API which is about DIYML.
3. And I also got the screenshots for docker and the queue unit test.

   
Step 4:
It is data protection. This code utilizes parameterized queries to prevent SQL injection attacks. Specifically, when the server receives a REGISTER command and the message length is 4, the code extracts the username, password, and port from the message and executes two SQL queries using parameterized queries: one to check if the username already exists and another to insert a new user.

When checking if the username exists, the code uses a parameterized query with a ? placeholder, ensuring that the user-provided username does not affect the query itself, thus avoiding the risk of SQL injection.

Similarly, when inserting a new user, parameterized queries are used to ensure that user-provided data such as username, password, IP address, and port are not treated as part of the SQL query, thus mitigating the risk of SQL injection.
