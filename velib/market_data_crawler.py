# encoding: UTF-8

from crawler import Crawler

class MarketDataCrawler(Crawler):

    geo_attribute='geo_coordinates'

    """
    {
      "datasetid": "liste_des_marches_de_quartier_a_paris",
      "recordid": "26be87a87a5bf45898a2c8e3055a91cb7217cbdb",
      "fields": {
        "marche": "BASTILLE",
        "samedi": "09h00 à 19h30",
        "arrondissement": 75011,
        "adresse_complete_poi_approchant": "boulevard Richard Lenoir 75011 Paris, France",
        "localisation": "Sur le terre plein central du boulevard Richard Lenoir",
        "societe_gestionnaire": "SOMAREP",
        "geo_coordinates": [
          48.860321,
          2.372673
        ],
        "type": "Création"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          2.372673,
          48.860321
        ]
      },
      "record_timestamp": "2014-08-13T20:25:53+00:00"
    }
    """

    params = {
    	"dataset": "liste_des_marches_de_quartier_a_paris",
        "rows": 1000
    }

    def __init__(self, config):
        Crawler.__init__(self, config)



