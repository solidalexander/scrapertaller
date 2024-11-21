
import pytest
import scraper

def test_scrape_mercado_libre():
    df = scraper.scrape_mercado_libre("playstation")
    assert not df.empty, "El DataFrame no debería estar vacío"
    assert 'title' in df.columns, "El DataFrame debería contener la columna 'title'"
    assert 'price' in df.columns, "El DataFrame debería contener la columna 'price'"
    assert 'link' in df.columns, "El DataFrame debería contener la columna 'link'"
    