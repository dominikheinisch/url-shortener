# url-shortener

Simple REST API for shortening URLs, written in Django REST Framework with Postgres as database.

## How it works

- every URL is saved in the table with auto-increment id
- id is encoded to base64url (`A-Z a-z 0-9 - _`)
- id is shifted with offset, so each code has always 6 characters, for e.g. id `1` gives `BAAAAB`
- if url was already shortened, the same link is returned
- maximum is 67,645,734,911 urls, after that API returns `503`

## How to run

```sh
make build
make migrate
make up        # http://localhost:8000
```

Other commands: for `make test`, `make lint`, `make fmt`, `make shell` and `make lock`.

## API

### Create short URL

```sh
curl -i -X POST http://localhost:8000/shrt/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/some/very/long/path"}'
```

```
HTTP/1.1 201 Created

{"short_url":"http://localhost:8000/shrt/BAAAAB"}
```

Errors:

- `400` url is missing, is not http or is longer than 2048 characters
- `415` body is not JSON
- `503` there are no free codes anymore

### Get original URL

```sh
curl -i http://localhost:8000/shrt/BAAAAB
```

```
HTTP/1.1 200 OK

{"url":"https://example.com/some/very/long/path"}
```

For unknown or wrong code API returns `404`.
