# 2333 Project Plan

Course Project for CS-C3170 Web Software Development

### Group Members

Hongkuan Wang  723316
Shiting Long  727778
Yuxi Xia  724797

### Design Overview

The online game store 2333 is an application that not only provides a platform for game developers to launch their games on but also supports game lovers to explore and play launched online games. In addition, game developers must set a price for their intellectual properties and thus the players can only play purchased games. Note that the application is a third-party service provider for building connections between developers and players, hence it does not concern matters associated with retailing prices of games or transaction details. Specifically, the store will redirect the user to the Simple Payment Service when transactions are needed.

### Features of the Application

#### 1. Registration and Authentication

The users of 2333 game store contain both players and developers. Note that a user cannot be both player and developer. Any user should log in before using services of 2333 and is able to log out. A user account can be created through registration, note the registration process needs to verify the email address provided by the user. For security reasons, a registered account detail cannot be used to register again. Visitors will not be granted access to services but can view the general website (game list and game display).

Here we plan to use Django auth for authentication. The credentials of a user to log in are username and password, which are default attributes of the User model in Django auth. The email attribute is essential to our application as well because we need to verify the email address before registration completed. If authentication fails, the visitor cannot access services of 2333.
