# Transavia
To run app use "docker-compose up --build" command. <br/>
The app hosts on "http://127.0.0.1:1337/". <br/>
Firstly, you need to **store** data, send **GET** request to **"http://127.0.0.1:1337/store/"**. <br/>
1. **GET** "http://127.0.0.1:1337/countries/" returns list of countries. <br/>
2. **GET** "http://127.0.0.1:1337/cities/" returns list of cities. <br/>
3. **GET** "http://127.0.0.1:1337/airports/" returns list of airports. <br/>
4. **POST** {code: "your_search_string"} to "http://127.0.0.1:1337/cities/search" returns list of filtererd cities. <br/>

## Admin dashboard 
**link:** "http://127.0.0.1:1337/admin/" <br/>
**username:** admin <br/>
**password:** pass <br/>
