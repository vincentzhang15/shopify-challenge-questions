from app import app
import bdi
import dei

if __name__ == '__main__':
    #bdi.app.run(host='localhost', port=443, ssl_context='adhoc', debug=True)    
    bdi.app.run(host='localhost', port=8080, debug=True)    
