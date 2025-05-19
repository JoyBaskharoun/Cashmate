# CashMate
  CashMate is a personal finance tracker web app.

- What does it do:
  It lets users register, log in, and track their income and spending. It supports filtering transactions by date, and displays summaries like total, current, and recent incomes or spending.
  
- A new feature:
  Chart graph for user data (transactions).

## Prerequisites
- Python 3.x
- Flask (`pip install flask`)
- No additional non-standard modules required (uses Python's built-in `json`).

## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.  
  - Module name: `json`, 
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app. Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.  
  - File name for the class definition: `transactions.py`
  - Line number(s) for the class definition: `6`
  - Name of two properties:  `email, amount`
  - Name of two methods: `is_income(), formatted_date()`
  - File name and line numbers where the methods are used: `summary.py -> 14,19  | dashboard.py -> 41`
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const rather than var).
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements.  
  Please provide below the file name and the line number(s) of at least one example of a conditional statement in your code.  
  - File name: `summary.py`
  - Line number(s): `9, 14, 19`
- [x] It contains loops.  
  Please provide below the file name and the line number(s) of at least one example of a loop in your code.  
  - File name: `edits.py`
  - Line number(s): `11, 41`
- [x] It lets the user enter a value in a text box at some point. This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using your own CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.