### Usage

__Requirements__:

    mkdir data
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

__Configuration file__:

Copy the config example file :

    cp config/config.yaml.dist config/config.yaml

and modify the variable as you wish :

    velib_files_path: <absolute path to station*.gz files>
    weather_files_path: <absolute path to paris_weather*.gz file>
    logging_level: INFO

To make the import work, you should end your path with a `/` and compressed data in the folders.

__First Launch__

    python run.py

It will create a `training.csv` file, which will be use in future runs to accelerate loading. 

__Modifications__ : I had to modify a bit the weather file to be able to read it easily

### Workflow

The program work this way :

 - Load local challenge data (velib history + weather)
 - Crawl additional data from open data paris (theatre, museum and market locations)
 - Merge data using timestamps or coordinates
 - Split the data into training set and test set (`split_proportion` variable)
 - Fit a Classifier or a Regressor the training set (here `RandomForestRegressor`)
 - Predict on the testset

Then it will print the feature importance and plot the error rate based on the confidence level : the predictions are floats between 0 and 1.  If the confidence level is 0.5, every prediction above 0.5 would mean 'There are some stands left in the station'. We then compare to the actual value.

### Usecase

The use case would be : I know the station near me has bikes. I will arrive to my destination in 1 hour. Would the station I'm targeting have stands left ?

### Results

The testset is a 30% subset of the trainset. We can make multiple run to have more accurate results but with few data a single run gives the same results.

![Prediction Rate over confidence level](https://github.com/tillmd/velib/blob/master/assets/predition_rate.png)


Here the error rate is very low (`assets/prediction_rate.png`) and could be explain by an overfitting. A velib data crawler had been developped but couldn't be used because of missing weather data (even though the first 4 important features are temporal data (see below)).

I used the RandomForestRegressor for :

 - its well know accuracy
 - the feature importance output
 - the oob estimation

__Feature importance__


| feature | importance |
|--------|--------------|
| minute | 4.9833051357 |
| hour | 3.7418882181 |
| day | 1.9510148148 |
| wday | 1.0712071957 |
| tempi | 1.0058053216 |
| number | 1.0014975615 |
| tempm | 0.9662565957 |
| theatre_distance | 0.6568507767 |
| museum_distance | 0.6205061519 |
| bike_stands | 0.6125561546 |
| market_distance | 0.5977898978 |
| month | 0.539800456 |
| conds_Mostly Cloudy | 0.1460951477 |
| icon_mostlycloudy | 0.1424671599 |
| icon_clear | 0.1260777932 |
| conds_Clear | 0.1232655831 |
| conds_Scattered Clouds | 0.109913737 |
| icon_partlycloudy | 0.1092215464 |
| conds_Partly Cloudy | 0.0877612316 |
| conds_Light Rain | 0.0524947526 |
| icon_rain | 0.0461725471 |
| rain | 0.040896624 |
| conds_Overcast | 0.0368349133 |
| icon_cloudy | 0.0362478491 |
| conds_Fog | 0.024847045 |
| fog | 0.0233143817 |
| conds_Light Drizzle | 0.0201011979 |
| icon_fog | 0.0196913614 |
| conds_Rain | 0.017992301 |
| conds_Patches of Fog | 0.0171216008 |
| conds_Shallow Fog | 0.0160653025 |
| conds_Light Rain Showers | 0.0135096732 |
| icon_unknown | 0.0126847769 |
| conds_Unknown | 0.0120640566 |
| conds_Rain Showers | 0.0044508173 |
| icon_hazy | 0.0025105848 |
| conds_Mist | 0.0024687149 |
| conds_Heavy Rain Showers | 0.002114527 |
| conds_Drizzle | 0.0015543805 |
| conds_Light Fog | 0.0011291071 |
| icon_tstorms | 0.0008785905 |
| thunder | 0.0008064289 |
| conds_Light Thunderstorms and Rain | 0.0007679871 |
| precipi | 0 |
| bonus | 0 |
| snow | 0 |
| banking | 0 |
| precipm | 0 |



### Future work

 - Use weather open data
 - Add more relevant features 
     + Minutes from midnight
     + Meeting area
 - Be able to mix contextual predictions with historical data (active learning)
 
### Litterature

These are papers talking about bike sharing in different ways, which could help for future improvements.

 - [Clustering the Velib' origin-destinations ows by means of Poisson mixture models](https://www.elen.ucl.ac.be/Proceedings/esann/esannpdf/es2013-95.pdf)
 - [Analyse de données sur des stations Vélib](http://nicolas.cheifetz.free.fr/academic_work/TADTI/[TADTI]Rapport-Projet_Nicolas-Cheifetz.pdf)
 - [Classification of the vélib stations using Kmeans, Dynamic Time Wraping and DBA averaging method](http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=7008802&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D7008802)
 - [MODELING OF REPOSITIONING ACTIVITIES IN BIKE - SHARING SYSTEMS](http://www.wctrs.leeds.ac.uk/wp/wp-content/uploads/abstracts/lisbon/general/02702.pdf)
 - [Urban cycles and mobility patterns : Exploring and predicting trends in a bicycle-based public transport system](www.dtic.upf.edu/~akalten/kaltenbrunner_etal2010PMC.pdf)
 - [An  Analysis  of  Bike  Sharing  Usage : Explaining  Trip  Generation and Attraction from Observed Demand](nacto.org/wp-content/uploads/2012/02/An-Analysis-of-Bike-Sharing-Usage-Explaining-Trip-Generation-and-Attraction-from-Observed-Demand-Hampshire-et-al-12-2099.pdf)
 - [Modelling the Impact of Weather Conditions on Active Transportation Travel Behaviour](https://tspace.library.utoronto.ca/bitstream/1807/25793/6/Saneinejad_Sheyda_201011_MASc_thesis.pdf)
 - [Model-based count series clustering for Bike Sharing System usage mining, a case study with the Velib system of Paris](https://hal.archives-ouvertes.fr/hal-01052621/file/doc00018491.pdf)
 - [Analyse des trajets de Vélib par clustering](http://www.vincentlemaire-labs.fr/CluCo2014/2014_Atelier_CluClo_ouvrage_EGC.pdf#page=23)
 - [From bicycle sharing system movements to users: a typology of Vélo’v cyclists in Lyon based on large-scale behavioural dataset](http://perso.ens-lyon.fr/pierre.borgnat/Papiers/14_Journal_Transport_Geography_Velov.pdf)
 - [Factorisation de reseaux temporels : etude des rythmes hebdomadaires du systeme Velo'v](https://hal.archives-ouvertes.fr/hal-01199256/document)
 - [Cartographie des pratiques du Vélo’v : le regard de physiciens et d’informaticiens](http://rsl.revues.org/487)
 - [Problème d’optimisation de disponibilité des véhicules partagés](http://conf.laas.fr/roadef2010/actes/resumes/p163.pdf)
 - [Modélisation statistique cyclique des locations de Vélo’v à Lyon](http://documents.irevues.inist.fr/bitstream/handle/2042/29029/borgnat_449.pdf?sequence=1)
 - [Peut-on attraper les utilisateurs de Vélo’v au Lasso](https://www.researchgate.net/profile/Gabriel_Michau/publication/268437756_Peut-on_attraper_les_utilisateurs_de_Vlo'v_au_Lasso_/links/555b1fde08ae980ca6122fbc.pdf)

### External Data

__Used__

 - [Annuaire Immobilier de l'Enseignement Superieur](http://opendata.paris.fr/explore/dataset/annuaire_immobilier_de_l_enseignement_superieur/api/)
 - [Liste des marchés de quartier à Paris](http://opendata.paris.fr/explore/dataset/liste_des_marches_de_quartier_a_paris/)
 - [Salles de cinémas à Paris](http://opendata.paris.fr/explore/dataset/cinemas-a-paris/)
 - [Stations Vélib - Disponibilités en temps réel](http://opendata.paris.fr/explore/dataset/stations-velib-disponibilites-en-temps-reel/)

__Not used__

 - [Etalages et terrasses autorisées à Paris](http://opendata.paris.fr/explore/dataset/etalages_et_terrasses_autorisees_a_paris/map/?location=18,48.86363,2.37143)
 - [Zones de circulation apaisée à Paris](http://opendata.paris.fr/explore/dataset/zones-de-circulation-apaisee-a-paris/)
 - [Liste Musées de France à Paris ](http://opendata.paris.fr/explore/dataset/liste-musees-de-france-a-paris/)
 - [Zones de rencontre](http://opendata.paris.fr/explore/dataset/zones-de-rencontre/information/?location=17,48.85358,2.34415)
 - [Réseau Cyclable ](http://opendata.paris.fr/explore/dataset/reseau-cyclable/?disjunctive.arrdt&disjunctive.statut&disjunctive.typologie&disjunctive.sens_velo)
 - [Stations Vélib - Disponibilités en temps réel](http://opendata.paris.fr/explore/dataset/stations-velib-disponibilites-en-temps-reel/information/)

