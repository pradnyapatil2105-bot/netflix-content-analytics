create database netflix_analysis;
use netflix_analysis;
select count(*) from netflix_titles;
select min(show_id),max(show_id) from netflix_titles;
show tables;