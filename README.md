# skills-graph
  A graphical representation of relations between programming languages, technologies and skills in demand, based on tens of thousands of job postings.\
  Backend: tags scraper and parser\
  Frontend: graph dynamic visualization 

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
