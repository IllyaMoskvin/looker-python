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
docker run -p 3306:3306 poc2
```




## References

* https://github.com/kelsin/mysql-mimic
* https://wiki.postgresql.org/wiki/Foreign_data_wrappers
* https://multicorn.org/
