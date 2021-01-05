# wikiaves_backend
Backend in Django for a public repository of birds

You must set environment variables or create .env file with:
* DJANGO_SU_NAME
* DJANGO_SU_EMAIL
* DJANGO_SU_PASSWORD
* POSTGRES_PASSWORD

Bird creation example:
```   
{
    "family":{
        "scientific_names":[
            {
                "name": "Family2",
                "main": true
            },
            {
                "name": "Family1",
                "main": false
            }
        ],
        "order": {
            "scientific_names":[
                {
                    "name": "Order1",
                    "main": true
                }
            ]
        }
    },
    "scientific_names": [
        {
            "name":"Spheniscus magellanicus",
            "main": true
        }
    ],
    "common_names": [
        {
            "main": true,
            "name":{
                "language": "es",
                "text": "Pinguino de Magallanes"
            }
        },
        {
            "main": false,
            "name":{
                "language": "es",
                "text": "Pinguino de Magallane"
            }
        }
    ],
    "habitat": {
        "language": "es",
        "text": "Es un ave marina y pelágica durante la migración. Anida en playas, colinas de arena y pendientes boscosas o con buena cobertura de pastos."
    },
    "conservation":{
        "type": "Almost Threatened",
        "text":{
            "language": "es",
            "text": "Esta especie se encuentra en estado de Casi Amenazada en al ámbito internacional. Actualmente enfrenta amenazas a causa de la contaminación por derrames de petróleo la cual ha sido responsable de la muerte de una gran cantidad de individuos en las costas Argentina. Estas aves también son cazadas para extraer su cebo y comúnmente son capturadas en redes de pesca en la Patagonia. Otros factores que afectan las poblaciones de esta especie son la depredación por zorros, ratas y gatos en algunas localidades. Actualmente el cambio climático y su efecto en las precipitaciones anuales están generando la muerte de crías por hipotermia y por el colapso de sus madrigueras. "
        }
    },
    "taxonomy": {
        "language": "es",
        "text": "Algunas veces ha sido considerada conespecífica con S. demersus y S. humboldti con las cuales podría formar una superespecie."
    },
    "behavior": [{
        "type": "Territorialidad",
        "text":{
            "language": "es",
            "text": "Es un excelente nadador de gran velocidad gracias a sus alas en forma de aletas, a sus músculos pectorales y patas que utiliza como timones. Son aves muy fieles a sus sitios de nacimiento al cual retornan año tras año. Al igual que otras aves marinas beben agua de mar que filtran con glándulas excretoras de sal ubicadas en la cavidad anterior de la cavidad orbital."
        }
    }],
    "images": [
        {
            "url":"https://www.icesi.edu.co/wiki_aves_colombia/show_image.php?id=25917",
            "category": "BIRD"
        }
    ]
}
```