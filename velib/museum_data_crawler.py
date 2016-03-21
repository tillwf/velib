# encoding: UTF-8

from crawler import Crawler

class MuseumDataCrawler(Crawler):

    geo_attribute='coordonnees_'
    
    """"
    {
        "datasetid":"liste-musees-de-france-a-paris",
        "recordid":"ee62a66f758e76fd1c4e3e1b6f8bd811bd3de9b8",
        "fields":{
            "periode_ouverture":"Ouvert de 10h à 18h du mardi au dimanche",
            "nom_du_musee":"Maison de Victor Hugo",
            "adr":"6, Place des Vosges",
            "ville":"PARIS",
            "nomreg":"ILE-DE-FRANCE",
            "sitweb":"www.musee-hugo.paris.fr",
            "fermeture_annuelle":"Jours fériés",
            "coordonnees_":[
                48.854821,
                2.366126
            ]
            ,
            "ferme":"NON",
            "cp":75004,
            "nomdep":"PARIS"
        }
        ,
        "geometry":{
            "type":"Point",
            "coordinates":[
                2.366126,
                48.854821
            ]
        }
        ,
        "record_timestamp":"2015-02-26T14:17:55+00:00"
    }
    """

    params = {
    	"dataset": "liste-musees-de-france-a-paris",
        "rows": 1000
    }

    def __init__(self, config):
        Crawler.__init__(self, config)



