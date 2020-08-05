# gutenberg-challenge-api
1. [Deployment Guide](#Deployment-Guide)
2. [API Guide](#API-Guide)
___


## Deployment GUIDE
_Created By : Mukunda M Mhasalkar

_Date : 06/08/2020_

___

### Prerequesites
1. Python3
2. Git
3. Virtualenv
4. MySql


### Setting up the environment

clone workspace from git into $PROJECT_DIR.
```
git clone https://github.com/mmhasalkar/gutenberg-challenge-api.git
```
Change directory to cloned directory.
```
cd gutenberg-challenge-api
```
Create python3 virtual environment.
```
virtualenv venv -p python3
```
Activate virtual environment.
```
source venv/bin/activate
```
Install requirements.
```
pip install -r requirements/requirements.txt
```
Login to MySql from command line.
```
mysql -u<username> -p;
```
Create database using MySql.
```
create database gutendex;
```
Exit MySql console.
```
exit;
```
Change directory to requirements and unzip the 'gutendex.sql.zip' file
```
cd requirements/
unzip gutendex.sql.zip
```
Import dump in MySql Database.
```
mysql -u<username> -p gutendex < gutendex.sql
```
Change directory back to the working directory.
```
cd ..
```
Edit ```config.py```.
```
nano gutenberg/config.py
```
Update following line with your username and password.
```
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/gutendex'
```
Install Gunicorn if not installed by requirement file.
```
pip install gunicorn
```

### Start service.
Fire following command
```
./start.sh
```

### Check logs.
```
tail -f logs/service.out
```
Check gunicorn access logs.
```
tail -f logs/access.log
```
Check gunicorn error logs.
```
tail -f logs/error.log
```

### Stop service.
```
./stop.sh
```
___

## API Guide
_Created By: Mukunda M Mhasalkar_

_Date: 06/08/2020_

___

### API List
___

1. Get Data
___

Base URL: [http://178.128.19.154:7000/api/v1](http://178.128.19.154:7000/api/v1)

Request Method: `GET`

#### 1. Get Data

Endpoing: `/gutenberg`

Parameter:

| Parameter | Data Type | Value | Required |
|-----------|-----------|-------|----------|
| offset | integer | offset number to retrive records | False |
| topic | string | comma separated topics to filter records | False |
| language | string | comma separated language codes to filter records | False |
| title | string | comma separated book title to filter records | False |
| author | string | comma separated author name to filter records | False |
| mime_type | string | comma separated mime_type values to filter records | False |

Sample Request:

```
http://178.128.19.154:7000/api/v1/gutenberg?offset=1&title=children&topic=infant&language=en,fr
```

Response:

```
{
    "records": [
        {
            "author": [
                {
                    "birth_year": 1718,
                    "death_year": 1783,
                    "name": "Hunter, William"
                }
            ],
            "bookshelf": [],
            "formats": [
                {
                    "mime_type": "text/html; charset=iso-8859-1",
                    "url": "http://www.gutenberg.org/files/26870/26870-h.zip"
                },
                {
                    "mime_type": "text/plain",
                    "url": "http://www.gutenberg.org/ebooks/26870.txt.utf-8"
                },
                {
                    "mime_type": "application/zip",
                    "url": "http://www.gutenberg.org/files/26870/26870.zip"
                },
                {
                    "mime_type": "application/epub+zip",
                    "url": "http://www.gutenberg.org/ebooks/26870.epub.images"
                },
                {
                    "mime_type": "application/rdf+xml",
                    "url": "http://www.gutenberg.org/ebooks/26870.rdf"
                },
                {
                    "mime_type": "text/plain; charset=us-ascii",
                    "url": "http://www.gutenberg.org/files/26870/26870.txt"
                },
                {
                    "mime_type": "application/x-mobipocket-ebook",
                    "url": "http://www.gutenberg.org/ebooks/26870.kindle.images"
                }
            ],
            "language": [
                {
                    "code": "en"
                }
            ],
            "subject": [
                {
                    "name": "Illegitimacy"
                },
                {
                    "name": "Infanticide"
                }
            ],
            "title": "On the uncertainty of the signs of murder in the case of bastard children"
        }
    ],
    "records_info": {
        "limit": 25,
        "offset": 1,
        "order_by": {
            "download_count": "DESC"
        },
        "selected_records": 3,
        "total_records": 3
    }
}
```
