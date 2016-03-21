# encoding: UTF-8

from crawler import Crawler

class TheatreDataCrawler(Crawler):

    geo_attribute='coordonnees'

    """"
    {
      "datasetid": "cinemas-a-paris",
      "recordid": "ec38a568be8f46b9024d99778de8d6bbf2b75afa",
      "fields": {
        "ecrans": 2,
        "fauteuils": "210",
        "ndegauto": 8361,
        "arrondissement": 75005,
        "art_et_essai": "A",
        "adresse": "7 PLACE ST MICHEL",
        "nom_etablissement": "ESPACE SAINT MICHEL 1",
        "coordonnees": [
          48.853093,
          2.344228
        ]
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          2.344228,
          48.853093
        ]
      },
      "record_timestamp": "2015-02-24T10:39:07+00:00"
    }
    """

    params = {
    	"dataset": "cinemas-a-paris",
      "rows": 1000
    }

    def __init__(self, config):
        Crawler.__init__(self, config)



