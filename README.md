# annas-py

Anna's Archive unofficial client library based on web scrapping

## Usage

Install by running:

```bash
pip install annas-py
```

Usage example:

```python
import annas_py

results = annas_py.search("python", language=annas_py.models.args.Language.EN)
for r in results:
    print(r.title)

information = annas_py.get_informations(results[0].id)
print("Title:", information.title)
print("Description:", information.description)
print("Links:", information.urls)
```
