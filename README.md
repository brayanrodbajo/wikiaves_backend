# Wikiaves backend
Backend in Django for a public repository of birds

You must set environment variables or create .env file with:
* DJANGO_SU_NAME
* DJANGO_SU_EMAIL
* DJANGO_SU_PASSWORD
* POSTGRES_PASSWORD

Bird creation example (go to https://www.notion.so/sebastianrestrepo/Documentaci-n-Backend-95510f10eb12472594c04e8edee20246 for further documentation):
```   
{
    "subspecies":[
        {
            "names": [
                {
                    "name": {
                        "language": "es",
                        "text": "Subspecie numero 1"
                    },
                    "main": true
                }
            ],
            "distribution": {
                "language": "es",
                "text": "Es una subspecie del Pinguino de Magallanes."
            }
        }
    ],
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
        "name":{
            "language": "es",
            "text": "Almost Threatened"
        },
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
        "name": {
            "language": "es",
            "text": "Territorialidad"
        },
        "text":{
            "language": "es",
            "text": "Es un excelente nadador de gran velocidad gracias a sus alas en forma de aletas, a sus músculos pectorales y patas que utiliza como timones. Son aves muy fieles a sus sitios de nacimiento al cual retornan año tras año. Al igual que otras aves marinas beben agua de mar que filtran con glándulas excretoras de sal ubicadas en la cavidad anterior de la cavidad orbital."
        }
    }],
    "migration": {
        "name": {
            "language": "es",
            "text": "Altitudinal"
        },
        "text":{
            "language": "es",
            "text": "Esta especie es altitudinal y no latitudinal."
        }
    },
    "identification": {
        "description": {
            "language": "es",
            "text": "Pinzón pequeño y compacto con cabeza proporcionalmente pequeña y cola corta; pico relativamente pequeño y triangular, con culmen ligeramente curvado. El macho es de color azul pizarroso oscuro por todas partes, más negro en la parte anterior y las partes inferiores, con el borde de las alas blanco. El iris es marrón oscuro; el pico es negro, la mandíbula a veces es gris oscura; y las patas son de gris rojizo a negruzco."
        },
        "plumage":[
            {
                "name": {
                    "language": "es",
                    "text": "Hembra"
                },
                "text": {
                    "language": "es",
                    "text": "La hembra es de color marrón rojizo, ligeramente más pálida en las partes inferiores, con el borde de las alas blanco; el pico negro, la base de la mandíbula de color cuerno, y las patas negras. Juvenil aparentemente no descrito."
                }
            }
        ],
        "lengths": [{
            "name": "length",
            "value": {
                "inferior": 12,
                "superior": 12.5
            },
            "unit": "cm"
        }],
        "weights": [{
            "name": "weight",
            "value": {
                "inferior": 12.5,
                "superior": 14.5
            },
            "unit": "gr"
        }]
    },
    "vocalizations": [{
        "category": "CALL",
        "short_description": {
            "language": "es",
            "text": "hola hola"
        },
        "audio": {
            "url": "https://googles.com",
            "format": "MP3"
        }
    }],
    "similar_species": [
        2, 3, 10
    ]
}
```
