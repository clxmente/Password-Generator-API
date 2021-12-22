# Password-Generator-API
A password generation api built with FastAPI.
## Setup
### Using a virtual environment
Create the virtual environment:
`python3 -m venv venv-folder-name`

Then activate the virtual environment:
- On Windows:
`venv-folder-name\Scripts\activate.bat`
- On unix or MacOS:
`source venv-folder-name/bin/activate`

And finally, install the requirements:
`pip install -r requirements.txt`

### Run the API on Uvicorn:
You can run the API locally using Uvicorn by executing the following command:
`python3 -m uvicorn gen:app`

Now the API can be accessed at `http://127.0.0.1:8000`, however there is no default path so nothing will be returned.

# Usage
## Endpoints
| Endpoint | Parameters |
|----------|------------|
| /password | length (optional) |
## /password
You can generate a password using the `/password` path. Addionally, you can specify a length with the `length` query parameter.
If no length is specified, the default password length is 10.

For example, to generate a password of length 16, you can use the `length` query parameter like so:

`http://127.0.0.1:8000/password?length=16`

The JSON response for a query like the one above:
```JSON
{
  "length":16,
  "password":"RP8*&**Z_ab$m#Jf"
}
```
