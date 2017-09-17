# TEXTDIY

This is our DIY chatbot for the THD codeathlon! The purpose of this chatbot is to provide DIY projects to the masses. It's meant to be able to reach a big audience as possible because 25% of the American population doesn't have a smartphone. It's also meant to be convenient as it doesn't require Wi-Fi and doesn't take up much of your phone's processing power. 

Text 202-TEXTDIY to start chatting!


# TECHNOLOGY

We used Flask, Twilio API, ngrok, Python, MeetUp API, Google APIs, and PostgreSQL for the backend. HTML/CSS and Javascript was used for the landing site.

# Commands

"diy" = "'DIY' sends you five random projects. To pick a project to see the details of, please send back the name of the project. At any point in the conversation, feel free to text a keyword and you will receive 5 projects that contain the keyword."


"filter" = "'Filter <Popularity or Difficulty or Cost> < ,Beginner or Intermediate or Expert, Amount>' allows you to search up projects based on specific properties. Add a cost in dollars to the cost filter to see projects that cost less than that price to build (filter cost 50), and add a difficulty after 'filter difficulty' to get projects with either a beginner, intermediate, or expert level difficulty"


"send assistance to" = "'Send Assistance To' followed by the location you are at will send a text message to Home Depot workers working in your store. They will come and help you with your project!"


"closest" = "'Closest <zipcode>' gives you the Home Depot store closest to you!" 


"add project" = "'Add Project <Project URL>' lets us know you want a specific project to be added to the database. We will look over it and add it so that other people can also see it!"


"feedback" = "'Feedback <number of stars> <review>' leaves feedback for us so we can improve our product. We would love to hear what you guys think about it!" 


"commands" = "'Commands' will give you a list of commands you can run in this chatbot. The commands are not case-sensitive, but make sure you dont have anything before the command!"
