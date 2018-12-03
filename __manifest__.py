{
	
	"name": "Car Rental",
	"version": "0.1",
	"installable": True,
	"auto_install": False,
	"application": False,
	'sequence': 1,
    'author': 'AZIRAR Imane, JABBAR Hanane, EL FILALI Alaa, KARJOUH Youness',
    'summary': 'gerer votre agence de location',
    'description': """
Logiciel de gestion de location de véhicules.
===============================

Développez vos ventes grâce à Logiciel Location véhicules! Le logiciel location véhicules combine fiabilité et fonctionnalité.
    """,
     'depends':['base', 'mail','product','account','sale','purchase'],

	"data": [
	"data/view.xml",
	"data/prix_view.xml",
	],
	'css': [
        'static/src/css/CSS.css',
    ],
}