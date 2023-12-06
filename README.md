# looker-python

> POCs for making Looker get data from a Python service

For the [Looker Hackathon 2023](https://inthecloud.withgoogle.com/looker-hackathon-2023/register.html). Authored by members of the [Data Science & Analytics Lab, American Family Insurance](https://amfamlabs.com/).

## POC 1

This POC offers a GET API. We parse the query string parameters, run some calculation, and write the results to somewhere (e.g. BigQuery) that is connected to our Looker instance.

```bash
cd poc1-api/
docker build -t poc1 .
docker run -p 8080:80 poc1
```

Visit http://localhost:8080 in your browser.


## POC 2

This POC uses [mysql-mimic](https://github.com/kelsin/mysql-mimic) to imitate a MySQL server. It uses SQL _as_ the API.

Setup a MySQL connection in Looker to point at wherever this script is running.

```bash
cd poc2-mimic/
docker build -t poc2 .
DB_PASS='foobar' docker run -p 3306:3306 -e DB_PASS poc2
```

Then, in a different session, run this to test it:

```bash
cd poc2-mimic-test/
docker build -t poc2-test .
DB_PASS='foobar' DB_HOST='host.docker.internal' docker run -e DB_PASS -e DB_HOST poc2-test 123 ABC

# host.docker.internal is for macOS, see this for details:
# https://stackoverflow.com/questions/17770902/forward-host-port-to-docker-container

# Alternatively... (faster, but messier)
cd poc2-mimic-test/
pip install -r requirements.txt
DB_PASS='foobar' DB_HOST='localhost' python main.py 123 ABC
```

`DB_PASS` must match between the two commands. `DB_HOST` is provided for testing remote server.

When calling the test script, change `123` and `ABC` to change the seed value.


## References

* https://github.com/kelsin/mysql-mimic
* https://wiki.postgresql.org/wiki/Foreign_data_wrappers
* https://multicorn.org/
