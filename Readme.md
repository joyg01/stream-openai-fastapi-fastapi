POC: stream from openai to vsl to vox

### Install needed packages

```
pip install -r requirements.txt
```

### Run

```
hypercorn app --bind 0.0.0.0:9999
```

## API endpoints

### stream from openai directly

```
GET: http://localhost:9999//openai/chat/stream
```

### stream from openai to endpoint 1 to endpoint 2

```
GET: http://localhost:9999/chat/stream
```

### Output

open any of the above api routes in your browser & check the response streamed.
### Reponse content type is
~~~ 
text/event-stream 
~~~
