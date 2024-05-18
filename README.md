# Mazingira Backend

## STARTING MAZINGIRA

- Clone the repository
- Change the directory `cd Mazingira_backend` and run the following commands
1. `pipenv install && pipenv  shell`
2. `cd server`
3. `export DATABASE_URI=postgresql://mazingira_database_wh0g_user:5GOoLvoe35AT7FjoRiviUUvG72uIpeUc@dpg-cp1oatmct0pc73d59v00-a.frankfurt-postgres.render.com/mazingira_db`
4. `python app.py`

## ENDPOINTS

### POST /register
Creates a new donor and logs them in.
#### Request
`POST /register`
#### JSON format
```json
{
    "first_name":"Enoch",
    "last_name": "Kibet",
    "email": "enoch@example.com",
    "password": "enoch"
}
```

### POST /register
Creates a new organization and logs them in.
#### Request
`POST /org/register`
#### JSON format
```json
{
    "name":"Mazingira's Organization",
    "email": "mazingira@example.com",
    "password": "organization"
}
```

### POST /login
Authenticates & Authorizes a donor/admin.
#### Request
`POST /login`
#### JSON format
```json
{
    "email":"enoch@example.com",
    "password":"enoch"
}
```

### POST /org/login
Authenticates & Authorizes an oorganization.
#### Request
`POST /org/login`
#### JSON format
```json
{
    "email":"mazingira@example.com",
    "password":"organization"
}
```
### GET /checksession
Checks for the current session
#### Request
`GET /checksession`
#### response
```json
{
    "message": "Log In To Access Resource or Contact Mazingira"
}
```
#### or

```json
{
    "email": "enoch@example.com",
    "first_name": "Enoch",
    "id": 125,
    "last_name": "Kibet",
    "role": "donor"
}
```

## ADMIN ENDPOINTS

### GET /admin
Returns a list of all the approved and unapproved organizations 
#### Request
`GET /admin`
#### Response
```json
[
    {
        "approval_status": true,
        "description": null,
        "email": "broberts@christian.com",
        "id": 23,
        "image_url": null,
        "name": "Howell, White and Murphy"
    },
    {
        "approval_status": false,
        "description": null,
        "email": "mariah00@wheeler.com",
        "id": 31,
        "image_url": null,
        "name": "Martin-Day"
    },
    {
        "approval_status": true,
        "description": null,
        "email": "ydorsey@butler-underwood.org",
        "id": 32,
        "image_url": null,
        "name": "White, Wilson and Roberts"
    },
    {
        "approval_status": true,
        "description": null,
        "email": "org@mazingira.com",
        "id": 33,
        "image_url": null,
        "name": "Just An Organization"
    },
    {
        "approval_status": false,
        "description": null,
        "email": "mazingira@example.com",
        "id": 34,
        "image_url": null,
        "name": "Mazingira's Organization"
    }
]
```


### GET /admin/23
Returns one organization whether approved or unapproved 
#### Request
`GET /admin/23`
#### Response
```json
{
    "approval_status": true,
    "description": null,
    "email": "broberts@christian.com",
    "id": 23,
    "image_url": null,
    "name": "Howell, White and Murphy"
}
```

### PATCH /admin/23
Approves or rejects an organization application 
#### Request
`PATCH /admin/23`
#### Request format
```json
{
    "approval_status": true
}
```

#### Response
```json
{
    "message": "Organization Updated Successfully",
    "organization": {
        "id": 23,
        "name": "Howell, White and Murphy",
        "email": "broberts@christian.com",
        "image_url": null,
        "approval_status": true,
        "description": null
    }
}
```
### DELETE /admin/23
Deletes one organization whether approved or unapproved 
#### Request
`DELETE /admin/23`
#### Response
```json
{
    "message": "Organization deleted successfully"
}
```
#### Or

```json
{
    "message": "Organization not found"
}
```


## DONOR ENDPOINTS

### GET /donor/organization
Returns a list of all the approved organizations 
#### Request
`GET /donor/organization`
#### response
```json
[
    {
        "approval_status": true,
        "description": null,
        "email": "broberts@christian.com",
        "id": 23,
        "image_url": null,
        "name": "Howell, White and Murphy"
    }
]
```
### GET /donor/organization/1
Returns one approved organizations
#### Request
`GET /donor/organization/1`
#### response
```json
{
    "approval_status": true,
    "description": null,
    "email": "broberts@christian.com",
    "id": 23,
    "image_url": null,
    "name": "Howell, White and Murphy"
}
```

### POST /donate
Creates a donation for an organization
#### Request
`POST /donate`
#### Request format
```json
{
    "amount": 400,
    "anonymous": true,
    "organization_id": 23
}
```
#### Response
```json
{
    "amount": 400.0,
    "anonymous": true,
    "donor_id": 125,
    "id": 55,
    "organization_id": 23
}
```
### GET /donor/stories
Returns stories about beneficiaries of your donations
#### Request
`GET /donor/stories`
#### response
```json
{
    "message": "No Stories Found. Make A Donation First"
}
```
#### or
```json
[
    {
      "content": "Street hair first significant skin play go. Tell stand light general treat walk I try. Population it eye necessary establish star. Professional child young certain move. Ball shake choice address another thing figure pull. Growth arm manager.",
      "created_at": "Sat, 11 May 2024 11:04:37 GMT",
      "id": 1,
      "image_url": "https://pbs.twimg.com/media/FpmD9sMXEAA4Mb7.jpg",
      "organization_id": 10,
      "title": "Kristine Peters"
    },
    {
      "content": "Not low agent guess toward control tell. Time include use price kid guy. Feeling instead free indicate recently player bit.",
      "created_at": "Sat, 11 May 2024 11:04:37 GMT",
      "id": 3,
      "image_url": "https://pbs.twimg.com/media/FpmD9sMXEAA4Mb7.jpg",
      "organization_id": 10,
      "title": "Austin Moore"
    }
]
```

## ORGANIZATION ENDPOINTS

### GET /organization
Returns the details of the organization and approval status 
#### Request
`GET /organization`
#### Response
```json
{
    "application_reviewed_on": null,
    "approval_status": false,
    "description": null,
    "email": "mazingira@example.com",
    "id": 34,
    "image_url": null,
    "name": "Mazingira's Organization",
    "registered_on": "Tue, 14 May 2024 16:42:01 GMT"
}
```

### GET /organization/donations
Returns donations made to an organization 
#### Request
`GET /organization/donations`
#### Response
```json
[
    {
      "amount": 400.0,
      "anonymous_status": true,
      "donated_on": "Sat, 11 May 2024 11:51:45 GMT",
      "id": 57,
      "organization_id": 9
    },
    {
      "amount": 400.0,
      "anonymous_status": true,
      "donated_on": "Sat, 11 May 2024 11:51:50 GMT",
      "id": 58,
      "organization_id": 10
    },
    {
      "amount": 400.0,
      "anonymous_status": true,
      "donated_on": "Sat, 11 May 2024 11:51:53 GMT",
      "id": 59,
      "organization_id": 11
    }
]
```
#### Or
```json
    {
        "message": "No Donations Found"
    }
```

### PATCH /org/edit
An organization can edit their details
#### Request
`PATCH /org/edit`
#### Request format
```json
{
    "image_url":"example image",
    "description":"example description"
}
```
#### response
```json
{
    "message": "Organization Updated Successfully",
    "organization": {
        "id": 34,
        "name": "Mazingira's Organization",
        "email": "mazingira@example.com",
        "image_url": "example image",
        "approval_status": false,
        "description": "example description"
    }
}
```

### POST /beneficiary
An organization can create a beneficiary
#### Request
`POST /beneficiary`
#### Request format
```json
{
    "name": "Beneficiary 2",
    "recieved_amount": 600,
    "image_url": "https://i.pinimg.com/originals/63/f9/d5/63f9d5fd5f34c8544a31c22c3e909cec.jpg"
}
```
#### response
```json
{
    "id": 59,
    "image_url": "https://i.pinimg.com/originals/63/f9/d5/63f9d5fd5f34c8544a31c22c3e909cec.jpg",
    "name": "Beneficiary 2",
    "organization_id": 34,
    "recieved_amount": 600.0
}
```

### POST /createpost
An organization can create a beneficiary story
#### Request
`POST /createpost`
#### Request format
```json
{
    "title": "John Kimani",
    "content": "A full stack software engineer. Collaborating with other 4 Engineers to build a donation website.",
    "image_url": "https://something.com/asadsa.jpg"
}
```
#### response
```json
{
      "content": "Street hair first significant skin play go. Tell stand light general treat walk I try. Population it eye necessary establish star. Professional child young certain move. Ball shake choice address another thing figure pull. Growth arm manager.",
      "created_at": "Sat, 11 May 2024 11:04:37 GMT",
      "id": 1,
      "image_url": "https://pbs.twimg.com/media/FpmD9sMXEAA4Mb7.jpg",
      "organization_id": 10,
      "title": "Kristine Peters"
    }
```

### GET /beneficiary
Returns a list of beneficiaries as well as inventory sent to the beneficiaries 
#### Request
`GET /beneficiary`
#### Response
```json
[
        {
            "id": 59,
            "image_url": "https://i.pinimg.com/originals/63/f9/d5/63f9d5fd5f34c8544a31c22c3e909cec.jpg",
            "name": "Beneficiary 2",
            "organization_id": 34,
            "recieved_amount": 600.0
        }
    ]
```

