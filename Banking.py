from flask import Flask,request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)
mydb = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Likhitha@123'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'banking_application'
mydb.init_app(app)
dbConn=mydb.connect()


class UserLogin(Resource):

    #check input from user
    def CheckUserDetails(self,userId,userPass): 
        userValid = False
        cursor = dbConn.cursor()
        selStmt ="SELECT PASSWORD FROM LOGIN WHERE USER_ID=(\'%s\')"%(userId)
        cursor.execute(selStmt)
        result=cursor.fetchone()
        if result is not None:
            print(str(result))
            if result[0] == userPass:
                userValid = True
            
        return userValid
    
    #get input from user
    def get(self):             
        cursor = dbConn.cursor()
        req = request.get_json()
        global userId
        userId = req['userId']
        userPass = req['userPass']
        

        if userId =="":
            errObj = { 'Error' : 'User ID cannot be Empty'}
            return errObj, 422
        if userPass == "":
            errObj = { 'Error' : 'User Password cannot be Empty'}
            return errObj, 422
        if (self.CheckUserDetails(userId,userPass)==True):
            errObj = {'Login':'Succesful'}
            return errObj, 422
        else:
            errObj = { 'Error' : 'Invalid Credentials'}
            return errObj, 422
        return {Flag:'Succesful'}
            
api.add_resource(UserLogin, '/UserLogin')

class AccountValidation(Resource):
    def CheckAcc(self,userAcc):
        accValid = False
        cursor = dbConn.cursor()
        selStmt ="SELECT USER_ID FROM ACCOUNT_DETAILS WHERE ACC_NUM=(\'%s\')"%(userAcc)
        cursor.execute(selStmt)
        result=cursor.fetchone()
        if result is not None:
            print(str(result))
            accValid = True     
        return accValid

    #get input from user
    def post(self):             
        cursor = dbConn.cursor()
        req = request.get_json()
        userAcc = req['userAcc']

        if userAcc == "":
            errObj = { 'Error' : 'Account Number cannot be Empty'}
            return errObj, 422
        if self.CheckAcc(userAcc)==True:
            return {'Success':userAcc}
        if self.CheckAcc(userAcc)==False:
            errObj = { 'Error' : 'Invalid Credentials'}
            return errObj, 422
api.add_resource(AccountValidation, '/AccountValidation')

if __name__ == '__main__':
    app.run(debug=True)


