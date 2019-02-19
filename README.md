# 2333 Project Report

Course Project for CS-C3170 Web Software Development

### Group Members

Hongkuan Wang  723316

Shiting Long  727778

Yuxi Xia  724797

### Implementation

| <center>Requirements | <center>Mandatory/Extra Points | <center>Requesting Points | <center>Reasons & Feedback |
|--------|:--------:|:--------:|----------:|
| Authentication | Mandatory | 200 | <p align="left">2333 supports login, logout and register using Django auth.</p> |
| Basic player functionalities | Mandatory | 300 | <p align="left"> 1. Players can buy and play games on the 2333 platform. <br>   2. Users without logging in and users logged in as a developer cannot buy or play the games.<br> 3. Players can search games by categories using navigation list on the left of the index page, thus preventing potential security problems caused by users’ random input.</p>|
|Basic developer functionalities|Mandatory|200|<p align="left">1. Developers can add, modify and remove games to the 2333 platform.<br>2. Information on a game is displayed on the inventory page as well as the sales number of such game. <br>3. There is a link called `DETAILS` underneath which redirects the developer to sales statistics page. <br>4. Note that developers can only make changes to or obtain detailed information of their own games, i.e., inventory of a developer is highly personal and with great secrecy.|
|Game/service interaction|Mandatory|200|<p align="left">1. We implemented the feature as what is described in the requirements. The game can send the postMessage to the parent window with the current game state and score. We also save the score and check whether the score is in the highest score list. Then, we display the first three highest score list in the parent window of the game. Each user only has one highest score for each game, the highest score displays three different users as well as their highest score.<br>2. We can receive messages from the service in the game page successfully.|
|Quality of Work | Mandatory|100|<p align="left">1. The structure of the application is coherent with a moderate amount of comments. <br>2. Don’t-Repeat-Yourself principle is valued and Model-View-Controller software architecture is used in our application. <br>3. Our application is easy-to-use with a clean style.<br>4. We have tested our application on the mainstream web-browsers such as Chrome, Edge and Firefox. We had an alpha test and a beta test, which means developers and non-developers have tested our application and have provided positive feedback.<br>5. Store sensitive information, such as secret keys as Heroku environment variables. |
|Non-functional requirements|Mandatory|200|<p align="left">1. We discussed the project plan together and wrote nit as clear as we can.<br>2. We documented our tasks as much as possible, we have a clear task distribution for each team member. Frequent meetings promoted the progress of our project. The history from Gitlab demonstrated good collaboration on the project.|
|Save/load and resolution feature|Extra|100|<p align="left">We designed a simple message protocol of resolution, and it worked fine after testing. |
|3rd party login|Extra|100|<p align="left">Users can use Google Login to the 2333 platform. If Google Login is used, the user must choose his/her role on the 2333 platform, namely either player or developer.|
|Own game|Extra|100|<p align="left">1. We implemented our own game with high-score, save, load, start and restart features. After testing it several times, all of above features worked fine in the database which can prove that communications are working well.<br>2. It is a fun Puzzle game, it also depends a little on luck. We believe our game is interesting and commendable.<br>3. The url of our game is: http://stupendous-shake.surge.sh|
|Mobile Friendly|Extra|50|<p align="left">Usability on varying screen width devices is concerned in the application. The application supports almost all mainstream screen width without flaws.|
|Social media sharing |Extra|50|<p align="left">Social media sharing is enabled for Facebook and Twitter. Players can share the game information, note that the game must be bought first. The player needs to log in for Facebook or Twitter before sharing. Game information and profile picture will be automatically loaded to the post by using OpenGraph and Twitter Card.




### Groupwork

Hongkuan Wang: Backend functionalities
<br>Yuxi Xia: Backend development, Game/service interaction, own game.
<br>Shiting Long: Frontend features and UI, documentation, service design


### Instructions to 2333

The online game store 2333 is an application that not only provides a platform for game developers to launch their games on but also supports game lovers to explore and play launched online games. The application is deployed to Heroku, the link is https://game2333.herokuapp.com/.

To use 2333, one can create a new account by setting a username, a role, etc., note that the email verification is enabled but no actual email will be sent due to the fact that this is not a business production. Google Login is also supported by 2333, one can choose his/her role after being authenticated by Google. Such functionalities can be explored by clicking ‘MY ACCOUNT’ on the navigation bar.

As a player, a user can buy games offered by 2333 within their balance. The player can only play the games that he/she has bought. Moreover, the player can save, load and share the purchased games using 2333’s services on the gaming page. Additionally, the player can submit his/her scores to the platform and highest scores are displayed on the gaming page as well.

As a developer, a user can add, modify and remove games on 2333. Such interactions are done on the user’s specific inventory page. Furthermore, the developer can check the sales number of each game on the inventory page and the sales statistics on the statistics page by clicking ‘DETAILS’ link on the inventory page.

As a visitor to the website, a user can view the descriptions of the games offered by 2333. Other options are prohibited if the user is not logged in.

Users can easily log out by clicking the logout button in the dropdown menu of ‘MY ACCOUNT’ section on the navigation bar.

As stated before, the application is a school project and email verification is enabled but not functional (the link sent to an email address can not be accessed without backend privilege), we provide here a developer account: “username: `dev`; password: `123`” , and a player account: “username: `pla`; password: `123`”  for testing purposes. Google Login is also recommended for testing our application.






