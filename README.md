# Jobs Portal

<h4>Overview</h4>

The Project titled 'Jobs Portal' aims to create a web application which allows registered users to post job offers and other registered users to apply for those jobs.
The project aims to fill the market gap by allowing people to apply for short-term opportunities.

If a user wants to post a job offer or comment/like other people's job offers, they need to register at the website first.
The user will be required to provide some information when registering and using the website.

The home page of the website provides some general information about the Job Portal and lists the most recently added job offers.

The following page titled 'Потърси Работа' lists all of the job offers that were created by all the users of the application. It allows the users to
filter and browse across the different job categories. Pagination is added below the job boxes to allow users to go to another page of job offers.
Users can click on the job boxes to read more about the job and the details provided by the creator of the offer (Job description, Place of work, Salary).
Users can also give a 'like' to the job or provide a comment in the 'Comments' section. The creator of the given job have 'Edit' and 'Delete' options at the bottom of the 
job page. When a user adds a comment in the 'Comments' section, they can delete the posted comment if they want to do so.

All registered users can apply for all of the jobs posted. The user who created the job will receive an email with all of the information from the applicant
including the the attached CV. Then, the creater of the job post can contact the applicant directly through email or phone (if provided on the CV).

The following page titled 'Контакти' contains form which users can fill in to express their opinion about the application or send questions to the admin.

Registered users have a profile section filled with the information that they have provided. The profile page can be edited and deleted at a later stage if the users
wants so. Users can also change their passwords if they need to do so. There is a separate section in the profile page which contains all the job offers that were
created by the specific user. The users' profile page can be accessed by other users in 'view' mode only.

The navigation bar contains 'Search' engine, which people can use to search key words and phrases within the jobs' title and description.

# Technologies used

<ul>
  <li>Python</li>
  <li>Javascript</li>
  <li>HTML</li>
  <li>CSS</li>
  <li>Cloudinary</li>
  <li>PostrgreSQL</li>
 </ul>

The application was built with Django Framework. The technologies used for building this application are Python, Javascript, HTML, CSS.
The projects uses PostgreSQL as database.

When users upload images they are stored in Cloudinary. If no image is provided by the user, a default image is uploaded for the profile photo and the job photo.


<strong>Prepared By: Boris Garkov</strong>
