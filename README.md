# What does this do?

This consists of two scripts: _getThem_ and _summarize_. 
The _getThem_ script downloads the results of an anonymous open-ended survey in Canvas. 
The _summarize_ uses Ollama and an LLM to generate a summary of the student responses for the instructor.

#  To _getThem_:

This uses the [python _canvasapi_ library](https://github.com/ucfopen/canvasapi) and your Canvas API key. At the top of the file, enter your Canvas URL and Canvas API key into the 
_API_URL_ and _API_KEY_ variables. It's setup to use a dictionary of section number -to- Canvas Course ID numbers, so also add that 
data in the _sections_ list and _dictCourseID_ dictionary as indicated in the file. It is currently set to prompt the user for a 
week number, and uses that to determine the name of the Canvas quiz that is being used as the survey. Update that to point instead 
to the name of your survey quiz. It downloads the result (as a csv file that Canvas generates) and writes it to a csv file named
by the section number.

# To _summarize_:

This uses [_Ollama_](https://github.com/ollama/ollama) and the [python _ollama_ library](https://github.com/ollama/ollama-python).  
In _Ollama_, pull the [LLM model](https://ollama.com/search) of your choice. This script is setup to use the 
[gemma3:27b model](https://ollama.com/library/gemma3:27b). Update the _aiModel_ variable to match the LLM you have pulled. 

This is currently setup for surveys of 3 questions. The _q1Col_, _q2Col_, and _q3Col_ variables near the top of the file indicate which column in the csv 
(downloaded from Canvas using _getThem_) correspond to the student responses for the questions. It generates a markdown file with the
results.

* How _summarize_ works:
_summarize_ builds a list of the csv files in the directory. For each of those files, it writes a header with the question students were asked.
Following that, it builds a querystring to send to the ollama chat giving details of the question and all the student responses and asking for
a summary, with some details about how to format it's response. When the response is generated, it gets printed below the question, and _summarize_
moves to the next.

