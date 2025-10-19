# Scrapper

Article Scraper API.

## Functionalities

#### Scraping
- title,
- whole content,
- plain content,
- publish date,
- url

#### REST API:
API is available under `http://localhost:8000/articles/`

- `GET /articles/`
- `GET /articles/{id}` 
- `GET /articles/?source=domain.com`

## Requirements

- **Docker** 
- **Python** >= 3.10  
- **PostgreSQL**  

## Installation
Get the ropository
```bash
git clone https://github.com/Ojkee/Scrapper.git 
cd Scrapper
```

Build and run container
```bash
docker compose up --build
```

```bash
docker compose exec scrapper_web python manage.py migrate
docker compose exec scrapper_web python manage.py makemigrations
```


## Usage 
Scrapping command
```bash
docker compose run --rm scrapper_web python manage.py scrape_articles <ulrs>
```
Parameter: <urls> is optional, if not provided, scraper will handle default urls from `articles/data/urls.txt` file.




