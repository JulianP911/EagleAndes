from EagleAndes import ner_from_str

ner_from_str('Cuatro cosas que debe saber sobre la minería ilegal en la Amazonia\n\nEl informe Amazonia saqueada revela devastación por presencia de minería ilegal en seis países amazónicos: Brasil, Bolivia, Colombia, Ecuador, Perú y Venezuela. Un mapa interactivo muestra más de 2.000 puntos en la región en los que se ha identificado esta práctica', './results.json')
# ner_from_url("https://www.eltiempo.com/vida/amazonia-deforestacion-mineria-agricultura-y-cultivos-ilicitos-577528",'./output.json')
# ner_from_file('./prueba.txt','./output.json')