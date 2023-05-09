# ServiceForFriends
`django` `rest frameword` `social network` `server`

Django-sevice for friends (as test project for VK intership)


## Server can do
- register a new user
- send friend-request from user to another user
- accept/deny friend-request from another user
- show list of user's friends
- show list of incoming friends-requests
- show list of outgoing friends-requests
- check status of relationship between users
  - nothing
  - incoming request
  - outgoing request
  - friendship
- delete user from another user's list of friends (request won't be created)
- auto accept requests if user1 send to user2 and user2 send to user1


## DataBase 
Base on Postgres 13.3

### Model 'User'
Table of user's informations. It can be email/age/birthday and e.t.c
- id: uuid
- name: str

### Model 'Relation'
Table of relations between users if its requested to be friends or friends already
- from_user: User
- to_user: User
- relation: Enum
  - Friend
  - Request

# How to use

Firstly you should up docker (web + postgres)

```commandline
sudo docker-compose up --build
```
Wait for loading and then

You can go to 0.0.0.0:8000 (0.0.0.0:8000/swagger) and check rest api

**Read ```server_for_friend/swagger.yaml```**

## Example

* Get list of all users

  - go to ```http://0.0.0.0:8000/users/```
      ```commandline
      curl -X 'GET' 
      'http://0.0.0.0:8000/users/' 
      -H 'accept: application/json' 
      -H 'X-CSRFToken: HhJLeNJw0Vb3QZgvQl7SHLEx6oknnbQgWpktplVBwxwXWjqTHxQtrUeh1KYPvsvV'
      ```
  - response 200
      ```python
      [
       {
           "id": "1",
           "name": "Ayka"
       },
       {
           "id": "2",
           "name": "Mike"
       },
      ]
     ```

* Create new user (registration)

  - go to ```http://0.0.0.0:8000/users/```
      ```commandline
      curl -X 'GET' 
      'http://0.0.0.0:8000/users/' 
      -H 'accept: application/json' 
      -H 'Content-Type: application/json' 
      -H 'X-CSRFToken: HhJLeNJw0Vb3QZgvQl7SHLEx6oknnbQgWpktplVBwxwXWjqTHxQtrUeh1KYPvsvV'
      -d '{
          "name": "ayka"
      }'
      ```
  - response 200
      ```python
       {
           "id": "1",
           "name": "Ayka"
       }
     ```
    
*  Get all friends of user by user_id

    - go to ```http://0.0.0.0:8000/users/friends```
        ```commandline
       curl -X 'GET' 
      'http://0.0.0.0:8000/users/' 
      -H 'accept: application/json' 
      -H 'id: 1'
      -H 'X-CSRFToken: HhJLeNJw0Vb3QZgvQl7SHLEx6oknnbQgWpktplVBwxwXWjqTHxQtrUeh1KYPvsvV'
      ```
    - response 200
        ```python
      [
         {
           "id": "2",
           "name": "Mike"
         },
      ]
        ```


* Get list of all relations
    - go to ```http://0.0.0.0:8000/relation```
        ```commandline
       curl -X 'GET' 
      'http://0.0.0.0:8000/relations/' 
      -H 'accept: application/json' 
      -H 'X-CSRFToken: HhJLeNJw0Vb3QZgvQl7SHLEx6oknnbQgWpktplVBwxwXWjqTHxQtrUeh1KYPvsvV'
      ```
    - response 200
        ```python
      [
         {
           "from_user": "1",
           "to_user": "2",
           "realtion": "F"
         },
      ]
        ```
* Send request
    - go to ```http://0.0.0.0:8000/relation/send_request```
        ```commandline
       curl -X 'POST' 
       'http://0.0.0.0:8000/relation/send_request/' 
       -H 'accept: application/json' 
       -H 'id: 1' 
       -H 'Content-Type: application/json' 
       -H 'X-CSRFToken: HhJLeNJw0Vb3QZgvQl7SHLEx6oknnbQgWpktplVBwxwXWjqTHxQtrUeh1KYPvsvV' 
       -d '{
       "to_id": "3"
       }'
      ```
    - response 200
        ```python
         {
           "from_user": "1",
           "to_user": "3",
           "realtion": "R"
         }
        ```  



## How to admin
Go to ```0.0.0.0:8000/admin```

To login check environment file ```.env``` with `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`.
You can:
- add User (add relation with another existing user)
- add Relation between existing users 
(Attension: if you create user1->user2 and user2->user1 they won't be friends)
- see all of Users
- see all of Relations
- delete User
- delete Relatine
- update User's fields:
  - name
- update Relation's fields:
  - relation

[//]: # (# to test)

[//]: # ()
[//]: # (```commandline)

[//]: # (python manage.py test)

[//]: # (```)