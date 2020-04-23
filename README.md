# skills-graph
  A graphical representation of relations between programming languages, technologies and skills in demand, based on tens of thousands of job postings.\

### Sample
2000 vacancies parced by keyword "Machine Learning" (headhunter.ru)
![Peek 2020-04-24 00-13](https://user-images.githubusercontent.com/47819971/80150148-846a5e80-85c0-11ea-82cc-cff6aef4900c.gif)

We can see, that essential skills for machine learning jobs are Python, SQL, Linux and others

### Structure
  Backend: tags scraper and parser\
  Frontend: graph dynamic visualization 
  
### How to use
TODO

#
### TODO
##### Backend:
* change raw format from pickle (list) to json as \
{'phrase': '', 'vacancies_number': int, items: list}
* preprocess: turn off filtering - return all nodes and links
* how to split job modules?

##### Frontend:
* add buttons with phrase name, parced vacancies number
* mark connected nodes if pushing on one of the nodes

renew JSON interface:\
add phrase and vacancies_number

##### Ideas
* monetization: ads? offers? contacts?
* private domain? + hosting?

##### Data sources
* Used:
  * hh.ru
* To use:
* Not usable:
* To test:
  * Linkedin
  * Stackoverflow jobs
  * Who is hiring hackernews
  * Indeed
  * Glassdoor

![Screenshot from 2020-04-23 22-48-38](https://user-images.githubusercontent.com/47819971/80143242-313ede80-85b5-11ea-8e23-08a3bca81286.png)
