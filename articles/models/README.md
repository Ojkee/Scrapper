# Models

### Article

- Tytuł artykułu
```python
title: models.CharField
```

- Oryginalna treść artykułu
```python
raw_text: models.TextField
```

- Treść artykułu jako plain text (bez tagów HTML)
```python
plain_text: models.TextField
```

- URL źródłowy (link do oryginalnego artykułu)
```python
url: models.URLField
```

- Data publikacji - MUSI być znormalizowana do formatu dd.mm.yyyy HH:mm:ss
```python
publish_date: models.DateTimeField
```

---


