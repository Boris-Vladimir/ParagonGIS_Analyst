import psycopg2

try:
    con = psycopg2.connect(database='cgi', user='postgres',
                           password='dapbfgnr', host='localhost')
    cur = con.cursor()

    # CGI TAB #################################################################
    # query por cgi completo --------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE cgi.cgi = (%s);"
    data = ('268-01-51-49762', )
    '''
    # query por operadora -----------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE cgi.operator = (%s);"
    data = ('3', )
    '''
    # query por lac -----------------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE cgi.lac = (%s);"
    data = ('332', )
    '''
    # query por cid -----------------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE cgi.cid = (%s);"
    data = ('57191', )
    '''

    # TECNOLOGIA TAB ##########################################################
    g2 = ("2G", "GSM", )
    g3 = ("3G", "UMTS", "HSDPA", )
    g4 = ("LTE", "FDD_1", "LTE_1800", "LTE_2600", "LTE_800", )
    # query por 2G ------------------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE cgi.technology = (%s) OR cgi.technology = (%s);"
    data = g2
    '''
    # query por 3G ------------------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE cgi.technology = (%s) OR cgi.technology = (%s) OR \
    cgi.technology = (%s);"
    data = g3
    '''
    # query por 4G ------------------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE cgi.technology = (%s) OR cgi.technology = (%s) OR \
    cgi.technology = (%s) OR cgi.technology = (%s) OR cgi.technology = (%s);"
    data = g4
    '''

    # DATA TAB ################################################################
    # query antes de: ... ----------------------------------------------------

    # query depois de: ... ---------------------------------------------------

    # query entre ... e ... --------------------------------------------------

    # query marcar todas -----------------------------------------------------

    # query são mais recentes' -----------------------------------------------

    # LOCALIZAÇÂO ADMINISTRATIVA TAB ##########################################
    # query código postal ----------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE s.codpostal LIKE (%s);"
    data = ("2715%", )
    '''
    # query por localidade ---------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE s.localidade LIKE (%s);"
    data = ("%LISBOA%", )
    '''
    # query por concelho -----------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE s.concelho = (%s);"
    data = ("Praia do Rei", )
    '''
    # query por distrito -----------------------------------------------------
    '''
    sql = "SELECT * FROM cgi JOIN (SELECT * FROM site) AS s ON cgi.sitename = \
    s.sitename WHERE s.distrito = (%s);"
    data = ("LISBOA", )
    '''
    # LOCALIZAÇÃO FÍSICA TAB #################################################
    # query por cí­rculo ------------------------------------------------------
    '''
    kms = '.1'
    cgi = '268-01-51-49762'
    sql = "SELECT * FROM site JOIN (SELECT * FROM cgi) AS s ON site.sitename = \
    s.sitename WHERE ST_Within((SELECT point FROM cgi WHERE cgi = %s), \
    ST_GeomFromText((SELECT ST_AsText(ST_Buffer((SELECT point FROM cgi WHERE \
    cgi = %s), %s)) FROM site JOIN (SELECT * FROM cgi) AS s ON site.sitename =  \
    s.sitename WHERE s.cgi = %s),4326)) AND s.operator = (SELECT operator FROM \
    cgi WHERE cgi = %s);"
    data = (cgi, cgi, kms, cgi, cgi, )
    '''
    # query por quadrado -----------------------------------------------------
    # ( não esquecer de atribuir às variaveis 1 sempre o valor menor!!!!!)
    lat1 = '38.68'
    lat2 = '38.7'
    lon1 = '-9.03'
    lon2 = '-9.05'
    sql = "SELECT * FROM site_cgi WHERE lat > %s AND lat < %s AND lon > %s AND \
    lon < %s;"
    data = (lat1, lat2, lon1, lon2, )


    cur.execute(sql, data)
    ver = cur.fetchall()
    n_results = 0
    for v in ver:
        print(v)
        n_results += 1
    print('\nRESULTADOS: ' + str(n_results))

except psycopg2.DatabaseError as e:
    print('Error %s' % e)
finally:
    if con:
        con.close()
