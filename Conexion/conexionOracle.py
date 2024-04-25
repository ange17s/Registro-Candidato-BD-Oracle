import cx_Oracle


def insertar_datos(usuario,idtipodoc,nombre, apellido, fechanac, ndoc):

    try:
        connection = cx_Oracle.connect(
            user ='BD1',
            password ='BD1',
            dsn= 'localhost:1521/BDIDB',
            encoding ='UTF-8'
        )
        print(connection.version)
        print('Hay conexion')
        try:
            cur =connection.cursor()

            cur.execute("SELECT usuario FROM candidato WHERE usuario = :1", (usuario,))

            res = cur.fetchall()
            print('res', res)
            if res:
                print("El candidato ya esta registrado")
                return True
            else:
                sql_insert = """INSERT INTO CANDIDATO (USUARIO, IDTIPODOC, NOMBRE, APELLIDO, FECHANAC, NDOC) VALUES (:1, :2, :3, :4, TO_DATE(:5, 'DD/MM/YYYY'), :6)"""
                print('Preparando para insertar')
                data =[(usuario,idtipodoc,nombre, apellido, fechanac, ndoc)]
                print('Datos listos')
                cur.executemany(sql_insert, data)
                print('Pasando a insercion')
                print('Insert completo')
                connection.commit()
                print('Commit exitoso')
                return False
        except cx_Oracle.DatabaseError as ex:
            error, = ex.args
            print('Oracle error code ', error.code)
            print('Oracle error message ', error.message)
        except Exception as ex:
            print('Error durante la insercion ', ex)
        finally:
            cur.close()
    except Exception as ex:
        print('Error en la conexion ',ex)
    finally:
        connection.close()
