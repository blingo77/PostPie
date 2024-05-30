# PostPie
Python Toolkit / Object Relational Mapper (ORM) for PostgreSQL

## Introduction
PostPie is a lightweight Python Toolkit or Object-Relational Mapper (ORM) for PostgreSQL. PostPie makes communicating and querying to a PostgreSQL database easy and very simple. PostPie aims to take the complexity and learning curve away from other ORM's by utilizing an intuitive
interface. PostPie is designed for small to medium level projects and is aimed at developers who are begginers to working with database's. PostPie is powered by the psycopg2 driver.

## Instillation

  **Open up your terminal or command line and enter:**
* ```pip install postpie```

## Get Started

**Simply import postpie at the top of your python file:** ``` import PostPie ``` <br> <br>
 Next you will need to connect your PostgreSQL database to PostPie. This step is also very easy, make sure you have the following:
 * Host Name
 * Database Name
 * Database Username
 * Database Password
 * Database Port Number

Next you will need to create an instance of the PostPie class (all PostPie functions can be found in this class) Ex: ``` py = PostPie() ``` <br>
Enter in database credientals the following way into the PostPie class: <br><br> * ``` py = PostPie(host_name='HOST NAME', db_name='DB NAME', user='DB USERNAME', password='PASSWORD', port='PORT NUMBER``` <br><br>
Now you should be connected to your database and can start using the PostPie ORM!

## License
PostPie is distributed under the [MIT license](https://opensource.org/license/mit)
